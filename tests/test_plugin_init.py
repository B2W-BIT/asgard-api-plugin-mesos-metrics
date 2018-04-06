import unittest
import logging

from metrics import asgard_api_plugin_init, config


class TestPluginInit(unittest.TestCase):

    def test_read_logger_if_passed(self):
        logger = logging.getLogger("logger.test")
        asgard_api_plugin_init(logger=logger)
        self.assertTrue(logger is config.logger)

    def test_default_logger_is_not_none(self):
        asgard_api_plugin_init()
        self.assertTrue(config.logger is not None)
