import logging
import requests 
import json

DOMAIN = "webhook_service"
_LOGGER = logging.getLogger(__name__)


SERVICE_SEND = "basic_webhook"

def setup(hass, config):
    def send_basic_webhook(call):
        data = call.data.copy()
        # if exists json, send json string
        if "json" in data:
            jsondata = json.loads(data["json"])
        # if exists jsonObj, stringify jsonObj then send it
        elif "jsonObj" in data:
            jsondata = data["jsonObj"]
        else:
            jsondata = {}
        # BASIC authenticate
        auth = None
        if "username" in data and "password" in data:
            auth = (data["username"], data["password"])
        result = requests.post(data["webhook"], json = jsondata, auth = auth)
        _LOGGER.warn('Received data', data["webhook"])

    hass.services.register(DOMAIN, SERVICE_SEND, send_basic_webhook)

    return True
