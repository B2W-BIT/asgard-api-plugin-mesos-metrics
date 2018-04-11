from os import getenv
import logging
from asgard.sdk.options import get_option

MESOS_ADDRESSES = get_option("MESOS", "ADDRESS")

logger = logging.getLogger()
