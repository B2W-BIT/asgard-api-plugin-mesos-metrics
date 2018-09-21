from unittest import TestCase, mock
import os
import importlib

from flask import Flask
from responses import RequestsMock
import json
import requests

from metrics import mesos, mesos_metrics_blueprint, config
import tests
from tests import with_json_fixture
import metrics

class MesosTest(TestCase):

    def setUp(self):
        self.application = Flask(__name__)
        self.application.register_blueprint(mesos_metrics_blueprint, url_prefix="/metrics")
        self.get_mesos_leader_address_patcher = mock.patch('asgard.sdk.mesos.get_mesos_leader_address', return_value="http://10.0.0.1:5050")
        self.get_mesos_leader_addres_mock = self.get_mesos_leader_address_patcher.start()

    def tearDown(self):
        self.get_mesos_leader_address_patcher.stop()

    def test_get_slaves_attr(self):
        attrs = mesos.get_slaves_attr(tests.SLAVES_STATE)
        self.assertEqual(
            set(attrs['server']),
            set(['slave0', 'slave1'])
        )
        self.assertEqual(
            set(attrs['dc']),
            set(['bit'])
        )

    def test_get_slaves_with_attr(self):
        result = mesos.get_slaves_with_attr(tests.SLAVES_STATE, {"dc": "bit"})
        self.assertEqual(len(result), 2)

    def test_get_slaves_with_attr_empty_result(self):
        result = mesos.get_slaves_with_attr(tests.SLAVES_STATE, {"foo": "bar"})
        self.assertEqual(result, [])

    def test_get_slaves_with_attr_filtered(self):
        result = mesos.get_slaves_with_attr(tests.SLAVES_STATE, {"server": "slave0"})
        self.assertEqual(result[0]['attributes']['server'], 'slave0')

    def test_attr_usage(self):
        with mock.patch('metrics.mesos.get_slaves_with_attr') as mocked:
            mocked.return_value = tests.SLAVES_STATE['slaves']
            result = mesos.get_attr_usage(tests.SLAVES_STATE, {"dc": "bit"})

            self.assertDictEqual(
                result,
                {
                    'cpu_used': 6.0,
                    'ram_used': 16,
                    'ram_total': 24,
                    'cpu_total': 12.0,
                    'ram_pct': 66.7,
                    'cpu_pct': 50.0
                }
            )

    @with_json_fixture("fixtures/master-slave-data.json")
    def test_attr_usage_no_usage(self, mesos_slaves_data):
        """
        Certificamos que conseguimos retonar um valor zero, ou seja,
        caso não exista nenhum slave usando a tag escolhida no filtro.
        """
        client = self.application.test_client()
        with RequestsMock() as rsps:

            rsps.add(method='GET', url="http://10.0.0.1:5050/slaves", body=json.dumps(mesos_slaves_data), status=200)
            response = client.get("/metrics/attr-usage?no-usage=none")
            self.assertEqual(200, response.status_code)

            self.assertDictEqual(
                json.loads(response.data),
                {
                    'cpu_used': 0.0,
                    'ram_used': 0,
                    'ram_total': 0,
                    'cpu_total': 0.0,
                    'ram_pct': 0.0,
                    'cpu_pct': 0.0
                }
            )

    def test_get_masters_alive_all_ok(self):
        meso_master_addresses = ["http://10.0.0.1:5050", "http://10.0.0.2:5050", "http://10.0.0.3:5050"]
        client = self.application.test_client()
        with RequestsMock() as rsps, \
                mock.patch('asgard.sdk.options', get_option=mock.MagicMock(return_value=meso_master_addresses)):
            importlib.reload(metrics)
            rsps.add(method='GET', url="http://10.0.0.1:5050/health", body="", status=200)
            rsps.add(method='GET', url="http://10.0.0.2:5050/health", body="", status=200)
            rsps.add(method='GET', url="http://10.0.0.3:5050/health", body="", status=200)
            response = client.get("/metrics/masters/alive")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(1, response_data['http://10.0.0.1:5050'])
            self.assertEqual(1, response_data['http://10.0.0.2:5050'])
            self.assertEqual(1, response_data['http://10.0.0.3:5050'])
            self.assertEqual(1, response_data['all_ok'])
            self.assertEqual(0, response_data['masters_down'])

    def test_get_masters_alive_one_down(self):
        meso_master_addresses = ["http://10.0.0.1:5050", "http://10.0.0.2:5050", "http://10.0.0.3:5050"]
        client = self.application.test_client()
        with RequestsMock() as rsps, \
                mock.patch('asgard.sdk.options', get_option=mock.MagicMock(return_value=meso_master_addresses)):
            importlib.reload(metrics)
            rsps.add(method='GET', url="http://10.0.0.1:5050/health", body="", status=200)
            rsps.add(method='GET', url="http://10.0.0.2:5050/health", body=requests.exceptions.ConnectionError())
            rsps.add(method='GET', url="http://10.0.0.3:5050/health", body="", status=200)
            response = client.get("/metrics/masters/alive")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(1, response_data['http://10.0.0.1:5050'])
            self.assertEqual(0, response_data['http://10.0.0.2:5050'])
            self.assertEqual(1, response_data['http://10.0.0.3:5050'])
            self.assertEqual(0, response_data['all_ok'])
            self.assertEqual(1, response_data['masters_down'])

    def test_get_masters_alive_all_down(self):
        meso_master_addresses = ["http://10.0.0.1:5050", "http://10.0.0.2:5050", "http://10.0.0.3:5050"]
        client = self.application.test_client()
        with RequestsMock() as rsps, \
                mock.patch('asgard.sdk.options', get_option=mock.MagicMock(return_value=meso_master_addresses)):
            importlib.reload(metrics)
            rsps.add(method='GET', url="http://10.0.0.1:5050/health", body=requests.exceptions.ConnectionError())
            rsps.add(method='GET', url="http://10.0.0.2:5050/health", body=requests.exceptions.ConnectionError())
            rsps.add(method='GET', url="http://10.0.0.3:5050/health", body=requests.exceptions.ConnectionError())
            response = client.get("/metrics/masters/alive")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(0, response_data['http://10.0.0.1:5050'])
            self.assertEqual(0, response_data['http://10.0.0.2:5050'])
            self.assertEqual(0, response_data['http://10.0.0.3:5050'])
            self.assertEqual(0, response_data['all_ok'])
            self.assertEqual(3, response_data['masters_down'])

    @with_json_fixture("fixtures/master-slave-data.json")
    def test_get_slaves_with_attrs_count_endpoint(self, master_state_fixture):
        client = self.application.test_client()
        with RequestsMock() as rsps:
            rsps.add(method='GET', url="http://10.0.0.1:5050/slaves", body=json.dumps(master_state_fixture), status=200)
            response = client.get("/metrics/slaves-with-attrs/count?dc=bit")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(6, response_data['total_slaves'])

    @with_json_fixture("fixtures/master-tasks.json")
    def test_get_tasks_count_endpoint(self, master_tasks_fixture):
        client = self.application.test_client()
        with RequestsMock() as rsps:
            rsps.add(method='GET', url="http://10.0.0.1:5050/tasks?limit=-1", body=json.dumps(master_tasks_fixture), status=200, match_querystring=True)
            response = client.get("/metrics/tasks/count")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(2, response_data['task_running'])
            self.assertEqual(1, response_data['task_failed'])
            self.assertEqual(2, response_data['task_finished'])
            self.assertEqual(1, response_data['task_killed'])
            self.assertEqual(6, response_data['total'])


    def test_get_task_namespace_prefix(self):
        self.assertEqual("sieve_", mesos._get_task_namespace("sieve_app_other_name.UUID"))
        self.assertEqual("infra_", mesos._get_task_namespace("infra_app_other_name.UUID"))
        self.assertEqual("other_", mesos._get_task_namespace("ct:1528217280003:0:afiliados-sleep-10:"))


    @with_json_fixture("fixtures/master-tasks-multiple-namespaces.json")
    def test_get_tasks_count_endpoint_separate_namespaces(self, master_tasks_fixture):
        """
        Confirmamos que fazemos a contagem por namespace também
        """
        client = self.application.test_client()
        with RequestsMock() as rsps:
            rsps.add(method='GET', url="http://10.0.0.1:5050/tasks?limit=-1", body=json.dumps(master_tasks_fixture), status=200, match_querystring=True)
            response = client.get("/metrics/tasks/count")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(2, response_data['task_running'])
            self.assertEqual(3, response_data['task_failed'])
            self.assertEqual(2, response_data['task_finished'])
            self.assertEqual(2, response_data['task_killed'])
            self.assertEqual(9, response_data['total'])

            # Namespace sieve
            self.assertEqual(1, response_data['sieve_task_running'])

            # Namespace infra
            self.assertEqual(0, response_data['infra_task_running'])

            # Chronos (que por enquanto não pertence a nehum namespace)
            self.assertEqual(1, response_data['other_task_running'])

    @with_json_fixture("fixtures/master-slave-data.json")
    def test_attrs_endpoint(self, master_state_fixture):
        client = self.application.test_client()
        with RequestsMock() as rsps:
            rsps.add(method='GET', url="http://10.0.0.1:5050/slaves", body=json.dumps(master_state_fixture), status=200)
            response = client.get("/metrics/attrs")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(4, len(response_data))
            self.assertEqual(["dc", "mesos", "owner", "workload"], sorted(response_data.keys()))

    @with_json_fixture("fixtures/master-slave-data.json")
    def test_attrs_endpoint_count(self, master_state_fixture):
        client = self.application.test_client()
        with RequestsMock() as rsps:
            rsps.add(method='GET', url="http://10.0.0.1:5050/slaves", body=json.dumps(master_state_fixture), status=200)
            response = client.get("/metrics/attrs/count")
            self.assertEqual(200, response.status_code)
            response_data = json.loads(response.data)
            self.assertEqual(1, len(response_data))
            self.assertEqual(4, response_data['total_attrs'])

    @with_json_fixture("fixtures/master-metrics.json")
    def test_get_metrics_from_current_leader(self, leader_metrics_fixture):
        with self.application.test_client() as client:
            with RequestsMock() as rsps:
                rsps.add(method='GET', url="http://10.0.0.1:5050/metrics/snapshot", body=json.dumps(leader_metrics_fixture), status=200)
                response = client.get("/metrics/leader?prefix=sys")
                self.get_mesos_leader_addres_mock.assert_called()
                self.assertEqual(200, response.status_code)
                metrics_data = json.loads(response.data)
                self.assertEqual(6, len(metrics_data.keys()))
                self.assertEqual(8, metrics_data["system/cpus_total"])
                self.assertEqual(0.1, metrics_data["system/load_15min"])
                self.assertEqual(0.21, metrics_data["system/load_1min"])
                self.assertEqual(0.14, metrics_data["system/load_5min"])
                self.assertEqual(269631488, metrics_data["system/mem_free_bytes"])
                self.assertEqual(20935741440, metrics_data["system/mem_total_bytes"])

    @with_json_fixture("fixtures/master-metrics.json")
    def test_get_metrics_master_with_prefix(self, master_metrics_fixture):
        with self.application.test_client() as client:
            with RequestsMock() as rsps:
                rsps.add(method='GET', url="http://10.0.0.1:5050/metrics/snapshot", body=json.dumps(master_metrics_fixture), status=200)
                response = client.get("/metrics/master/10.0.0.1?prefix=sys")
                self.assertEqual(200, response.status_code)
                metrics_data = json.loads(response.data)
                self.assertEqual(6, len(metrics_data.keys()))
                self.assertEqual(8, metrics_data["system/cpus_total"])
                self.assertEqual(0.1, metrics_data["system/load_15min"])
                self.assertEqual(0.21, metrics_data["system/load_1min"])
                self.assertEqual(0.14, metrics_data["system/load_5min"])
                self.assertEqual(269631488, metrics_data["system/mem_free_bytes"])
                self.assertEqual(20935741440, metrics_data["system/mem_total_bytes"])

    @with_json_fixture("fixtures/master-metrics.json")
    def test_get_metrics_master_no_prefix(self, master_metrics_fixture):
        with self.application.test_client() as client:
            with RequestsMock() as rsps:
                rsps.add(method='GET', url="http://10.0.0.1:5050/metrics/snapshot", body=json.dumps(master_metrics_fixture), status=200)
                response = client.get("/metrics/master/10.0.0.1")
                self.assertEqual(200, response.status_code)
                metrics_data = json.loads(response.data)
                self.assertEqual(len(master_metrics_fixture.keys()), len(metrics_data.keys()))

    @with_json_fixture("fixtures/slave-metrics.json")
    def test_get_metrics_slave_no_prefix(self, slave_metrics_fixture):
        with self.application.test_client() as client:
            with RequestsMock() as rsps:
                rsps.add(method='GET', url="http://10.0.0.1:5051/metrics/snapshot", body=json.dumps(slave_metrics_fixture), status=200)
                response = client.get("/metrics/slave/10.0.0.1")
                self.assertEqual(200, response.status_code)
                metrics_data = json.loads(response.data)
                self.assertEqual(len(slave_metrics_fixture.keys()), len(metrics_data.keys()))

    @with_json_fixture("fixtures/slave-metrics.json")
    def test_get_metrics_slave_with_prefix(self, slave_metrics_fixture):
        with self.application.test_client() as client:
            with RequestsMock() as rsps:
                rsps.add(method='GET', url="http://10.0.0.1:5050/metrics/snapshot", body=json.dumps(slave_metrics_fixture), status=200)
                response = client.get("/metrics/leader?prefix=containerizer/mesos/provisioner/")
                self.assertEqual(200, response.status_code)
                metrics_data = json.loads(response.data)
                self.assertEqual(2, len(metrics_data.keys()))
                self.assertEqual(0, metrics_data["containerizer/mesos/provisioner/bind/remove_rootfs_errors"])
                self.assertEqual(0, metrics_data["containerizer/mesos/provisioner/remove_container_errors"])

