from mycroft.skills.core import MycroftSkill
from mycroft.skills.audioservice import AudioService

import requests
import fuzzywuzzy

class HAUtils(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(HAUtils, self).__init__(name="HomeAssistantUtils")

    def initialize(self):
        self.audio_service = AudioService(self.bus)

        self.host_address = self.settings.get('host_address')
        self.llat = self.settings.get('llat')
        self.lightEntity = self.settings.get('light_entity')

        self.register_intent_file('lights.intent', self.handle_lights)

    def handle_lights(self, message):
        state = message.data.get('state')

        method = "http"
        if self.settings.get('ssl'):
            method = "https"
        
        url = f"{method}://{self.settings.get('host_address')}:{self.settings.get('port')}/api/states/{self.settings.get('light_entity')}"
        payload = {"state": state}

        requests.post(url, data = payload, headers = {"Authorization": "Bearer " + self.settings.get('llat')})
        
        self.speak("the lights have been turned " + state)

    def stop(self):
        pass

def create_skill():
    return HAUtils()