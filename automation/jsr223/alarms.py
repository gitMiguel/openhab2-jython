#from org.slf4j import Logger, LoggerFactory
from time import sleep
from openhab.rules import rule
from openhab.triggers import when
from openhab.actions import Telegram

#log = LoggerFactory.getLogger("org.eclipse.smarthome.model.script.Alarm")

#Send one telegram
def sendNotification(message):
    Telegram.sendTelegram("LanteeBot", message)
    log.info(message)

#Network
@rule("Network check")
@when("Member of GrNetwork changed")

def execute(event, log):
    if ir.getItem("GrNetwork").state == ON:
        message = "Network fully online"
        Telegram.sendTelegram("LanteeBot", message)
        log.info(message)      
    else:
        sleep(5)
        offlineMembers = sorted(member for member in ir.getItem("GrNetwork").getMembers() if member.state == OnOffType.OFF, key = lambda member: member.state)
        message = "Network devices offline:\n\n{}".format("\n".join(item.label for item in offlineMembers))
        Telegram.sendTelegram("LanteeBot", message)
        log.info(message)

#Vallox
@rule("Generic alarm")
@when("Member of GrAlarm changed to ON")

def execute(event, log):
    alarmMembers = sorted(member for member in ir.getItem("GrAlarm").getMembers() if member.state == OnOffType.ON, key = lambda member: member.state)
    message = "Alarm item: {}".format(", ".join(item.label for item in alarmMembers))
    Telegram.sendTelegram("LanteeBot", message)
    log.info(message)