# Copyright 2022 iiPython

# Modules
import os
import json
import logging
import requests

# Initialization
log, upstream_url = logging.getLogger("rich"), os.getenv("STREAMX_UPSTREAM", "")
def e(message: str) -> None:
    log.critical(message)
    exit(1)

if not upstream_url.strip():
    e("Missing upstream configuration URL!")

# Load configuration
if upstream_url != "file":
    try:
        config = requests.get(f"http://{upstream_url}:4070", timeout = 3).json()

    except requests.exceptions.Timeout:
        e("Timed out while connecting to config server!")

    except Exception:
        e("Configuration server is offline!")

else:
    fp = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    if not os.path.isfile(fp):
        e("Config upstream set to file but no configuration file exists!")

    with open(fp, "r") as fh:
        config = json.loads(fh.read())
