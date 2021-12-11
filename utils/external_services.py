import json
import time
from typing import Any

import requests
from logzero import logger as log

from config.cf import CONFIG
from utils.funcs import get_path, safe_capture_error


def send_postman(payload: Any) -> dict:
    try:
        headers = {
            'finizi-api-key': CONFIG.POSTMAN_API_KEY
        }
        start_time = time.time()
        log.info(f'start send to {payload.url} with body {payload.json()}')
        response = requests.request("POST", payload.url, headers=headers, data=payload.json())
        end_time = time.time() - start_time
        res = json.loads(response.text)
        log.info(f"this is time {end_time} res from postman {res}")
        if response.status_code == 200:
            return res
    except Exception as e:
        safe_capture_error(e)
        raise e

