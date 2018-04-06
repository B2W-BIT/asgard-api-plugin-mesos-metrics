from os import getenv
import logging

MESOS_URL = getenv('ASGARD_MESOS_METRICS_URL')

logger = logging.getLogger()
