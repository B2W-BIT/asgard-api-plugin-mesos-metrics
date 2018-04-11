from os import getenv
import logging
from asgard.sdk.options import get_option

MESOS_URL = getenv('ASGARD_MESOS_METRICS_URL')

MESOS_ADDRESSES = get_option("MESOS", "ADDRESS")

logger = logging.getLogger()
