from unittest import TestCase, mock
import json
from metrics import mesos
import requests
import tests

class MesosTest(TestCase):


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
