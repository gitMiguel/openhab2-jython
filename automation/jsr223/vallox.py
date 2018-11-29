#from org.slf4j import Logger, LoggerFactory
from openhab.rules import rule
from openhab.triggers import when
from threading import Timer

#log = LoggerFactory.getLogger("org.eclipse.smarthome.model.script.Vallox")

firePlaceTimer = None
lastDCFanOutputSpeed = 0

def timerStopped():
    events.postUpdate("Takkakytkin", "0")
    events.sendCommand("DCFanOutputAdjustment", "100")

@rule("Vallox fire place timer")
@when("Item Takkakytkin received command")

def execute(event, log):
    global firePlaceTimer
    global lastDCFanOutputSpeed
    command = int(str(event.itemCommand.intValue()))
    time = command * 360
    if command == 0:
        if not firePlaceTimer or str(firePlaceTimer.getState()) == "TERMINATED":
            log.info("Fire place timer already deactivated")
        else:
            firePlaceTimer.stop()
            timerStopped()
            log.info("Fire place timer stopped")
    if command >= 1 and command <= 3:
        if not firePlaceTimer or str(firePlaceTimer.getState()) == "TERMINATED":
            firePlaceTimer = Timer(time, timerStopped)
            firePlaceTimer.start()
            events.sendCommand("DCFanOutputAdjustment", "30")
            log.info("Fire place timer activated for {} hours".format(command))
        elif firePlaceTimer or str(firePlaceTimer.getState()) == "TIMED_WAITING":
            firePlaceTimer.stop()
            firePlaceTimer = Timer(time, timerStopped)
            firePlaceTimer.start()
            events.sendCommand("DCFanOutputAdjustment", "30")
            log.info("Fire place timer rescheduled for {} hours".format(command))