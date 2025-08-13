import requests

class HomeAssistantTool:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def turn_on(self, entity_id):
        url = f"{self.base_url}/api/services/homeassistant/turn_on"
        resp = requests.post(url, headers=self.headers, json={"entity_id": entity_id})
        return "Device turned on." if resp.status_code == 200 else "Failed to turn on device."

    def turn_off(self, entity_id):
        url = f"{self.base_url}/api/services/homeassistant/turn_off"
        resp = requests.post(url, headers=self.headers, json={"entity_id": entity_id})
        return "Device turned off." if resp.status_code == 200 else "Failed to turn off device."
