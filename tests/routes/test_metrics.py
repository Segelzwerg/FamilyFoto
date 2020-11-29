import prometheus_client
from flask_api import status
from prometheus_flask_exporter import PrometheusMetrics

from tests.base_test_case import BaseTestCase
from tests.test_utils.mocking import mock_user


class AdminMetricsTestCase(BaseTestCase):
    """
    Tests the route behind /metrics with admin user.
    """

    def setUp(self):
        super().setUp()
        mock_user(self, 'admin', 'admin')
        # reset the underlying Prometheus registry
        prometheus_client.REGISTRY = prometheus_client.CollectorRegistry(auto_describe=True)

    def metrics(self, **kwargs):
        return PrometheusMetrics(self.app, registry=kwargs.pop('registry', None), **kwargs)

    def tearDown(self):
        self.patcher.stop()
        super().tearDown()

    def test_metrics_route(self):
        response = self.client.get('/metrics')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
