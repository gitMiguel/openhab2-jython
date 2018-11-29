#from org.slf4j import Logger, LoggerFactory
from openhab.rules import rule
from openhab.triggers import when
from openhab.actions import Telegram

#log = LoggerFactory.getLogger("org.eclipse.smarthome.model.script.Startup")

isRunning = False

@rule("System started")
@when("Item StartTrigger received command ON")

def execute(event, log):
    global isRunning
    if not isRunning:
        log.info("System started")
        Telegram.sendTelegram("LanteeBot", "System started")

        events.postUpdate("CoolingState", "Ei")
        events.postUpdate("IvtPumpState", "Lepo")
        events.postUpdate("Takkakytkin", "0")
        events.postUpdate("Tehostuskytkin", "0")
        isRunning = True
    else:
        log.info("\"System\" started trigger passed")