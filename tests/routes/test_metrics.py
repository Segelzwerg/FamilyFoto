import prometheus_client
from flask_api import status
from prometheus_flask_exporter import PrometheusMetrics

from tests.base_test_case import BaseTestCase
from tests.test_utils.mocking import mock_user


class BaseMetricsTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        # reset the underlying Prometheus registry
        prometheus_client.REGISTRY = prometheus_client.CollectorRegistry(auto_describe=True)

    def tearDown(self):
        super().tearDown()

    def metrics(self, **kwargs):
        return PrometheusMetrics(self.app, registry=kwargs.pop('registry', None), **kwargs)


class AdminMetricsTestCase(BaseMetricsTestCase):
    """
    Tests the route behind /metrics with admin user.
    """

    def setUp(self):
        super().setUp()
        mock_user(self, 'admin', 'admin')

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_metrics_route(self):
        response = self.client.get('/metrics')
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

    def metrics(self, **kwargs):
        return PrometheusMetrics(self.app, registry=kwargs.pop('registry', None), **kwargs)

    def test_metrics_route(self):
        response = self.client.get('/metrics')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)


class AnonymousMetricsTestCase(BaseMetricsTestCase):
    """
    Tests the route behind /metrics with anonymous.
    """

    def setUp(self):
        super().setUp()

    def test_metrics_route(self):
        response = self.client.get('/metrics')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
