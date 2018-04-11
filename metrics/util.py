
import requests


from metrics import config


def get_mesos_leader_address():
    for mesos_address in config.MESOS_ADDRESSES:
        try:
            response = requests.get(f"{mesos_address}/redirect", timeout=2, allow_redirects=False)
            if response.headers.get("Location"):
                leader_ip = response.headers.get("Location").split("//")[1]
                return f"http://{leader_ip}"
        except requests.exceptions.ConnectionError as ConErr:
            pass

def get_mesos_slaves():
    leader_address = get_mesos_leader_address()
    url = f"{leader_address}/slaves"
    config.logger.debug({"action": "pre-fetch", "fetch-url": url})
    response = requests.get(url, timeout=2)
    config.logger.debug({"action": "post-fetch", "fetch-url": url, "fetch-status": response.status_code})
    return response.json()
