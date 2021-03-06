import base64

import prometheus_client
from flask_api import status
from prometheus_flask_exporter import PrometheusMetrics

from tests.base_admin_test_case import BaseAdminTestCase
from tests.base_test_case import BaseTestCase
from tests.test_utils.mocking import mock_user


class BaseMetricsTestCase(BaseTestCase):
    """
    Base Test class for metrics route.
    """

    def setUp(self):
        super().setUp()
        # reset the underlying Prometheus registry
        prometheus_client.REGISTRY = prometheus_client.CollectorRegistry(auto_describe=True)

    def metrics(self, **kwargs):
        """
        Set ups the prometheus for testing.
        :param kwargs: registries arguments
        :return: prometheus client
        """
        return PrometheusMetrics(self.app, registry=kwargs.pop('registry', None), **kwargs)


class AdminMetricsTestCase(BaseMetricsTestCase, BaseAdminTestCase):
    """
    Tests the route behind /metrics with admin user.
    """

    def test_metrics_route(self):
        """
        Tests if the admin has access on /metrics.
        """
        username = 'admin'
        password = '1234'
        headers = {
            'Authorization': 'Basic {0}'.format(base64.b64encode(bytes(
                f"{username}:{password}", 'utf-8')).decode('utf-8'))
        }
        response = self.client.get('/metrics', headers=headers)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class UserMetricsTestCase(BaseMetricsTestCase):
    """
    Tests the route behind /metrics with user.
    """

    def setUp(self):
        super().setUp()
        mock_user(self, 'user', 'user')

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_metrics_route(self):
        """
        Tests if a normal user can't reach /metrics.
        """
        response = self.client.get('/metrics')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class AnonymousMetricsTestCase(BaseMetricsTestCase):
    """
    Tests the route behind /metrics with anonymous.
    """

    def test_metrics_route(self):
        """
        Tests if an anonymous can't reach /metrics.
        """
        response = self.client.get('/metrics')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
