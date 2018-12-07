from time import sleep
from openhab.rules import rule
from openhab.triggers import when
from openhab.actions import Telegram

#Network
@rule("NetworkCheck")
@when("Time cron 0 0 21 * * ?")
@when("Time cron 0 0 12 * * ?")
@when("Member of GrNetwork changed")

def execute(event, log):
    if ir.getItem("GrNetwork").state == ON:
        if event:
            message = "Network fully online"
            Telegram.sendTelegram("LanteeBot", message)
            log.info(message)    
    else:
        sleep(1)
        offlineMembers = sorted(member for member in ir.getItem("GrNetwork").getMembers() if member.state == OnOffType.OFF, key = lambda member: member.state)
        message = "Network devices offline:\n\n{}".format("\n".join(item.label for item in offlineMembers))
        Telegram.sendTelegram("LanteeBot", message)
        log.info(message)

#Generic
@rule("GenericAlarm")
@when("Time cron 0 0 21 * * ?")
@when("Time cron 0 0 12 * * ?")
@when("Member of GrAlarm changed")

def execute(event, log):
    if ir.getItem("GrAlarm").state == ON:   
        alarmMembers = sorted(member for member in ir.getItem("GrAlarm").getMembers() if member.state == OnOffType.ON, key = lambda member: member.state)
        message = "Alarm item: {}".format(", ".join(item.label for item in alarmMembers))
        Telegram.sendTelegram("LanteeBot", message)
        log.info(message)
    else:
        if event:
            message = "No active alarms"
            Telegram.sendTelegram("LanteeBot", message)
            log.info(message)