#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io

CONFIG_INI = "config.ini"

# If this skill is supposed to run on the satellite,
# please get this mqtt connection info from <config.ini>
# Hint: MQTT server is always running on the master device
MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

class VoiceKit(object):
    """Class used to wrap action code with mqtt connection
        
        Please change the name refering to your application
    """

    def __init__(self):
        # get the configuration if needed
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
            self.mqtt_address = self.config.get("secret").get("mqtt").encode()
        except :
            self.config = None
            self.mqtt_address = MQTT_ADDR

        # start listening to MQTT
        self.start_blocking()
        
    def Query_SalesAmount(self, hermes, intent_message):
        # terminate the session first if not continue
        hermes.publish_end_session(intent_message.session_id, "")
        
        # action code goes here...
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)

        money = "2300"
        # if need to speak the execution result by tts
        hermes.publish_start_session_notification(intent_message.site_id, "OK, " + money , "")

    # --> Master callback function, triggered everytime an intent is recognized
    def master_intent_callback(self,hermes, intent_message):
        coming_intent = intent_message.intent.intent_name

        if coming_intent == 'DanielSky:querysalesamount':
            self.Query_SalesAmount(hermes, intent_message)

    # --> Register callback function and start MQTT
    def start_blocking(self):
        with Hermes(self.mqtt_address) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    VoiceKit()
