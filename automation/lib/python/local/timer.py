import sys

from threading import Timer
from openhab.jsr223.scope import events
from openhab.jsr223.scope import itemRegistry 

from org.eclipse.smarthome.core.items import GroupItem

#reload(sys.modules['openhab.jsr223'])
#from openhab.jsr223.scope import events
#from openhab.jsr223.scope import itemRegistry

from openhab.log import add_logger, log_traceback
from local import config

timer = None




"""
Timer classes for openHAB jython rules
"""

@add_logger
class BaseTimer(object):
    """ Base class for timers"""
    def __init__(self, interval, items, start_command, stop_command):
        self.timer = None
        self.interval = interval
        self.items = items
        self.start_command = start_command
        self.stop_command = stop_command

    def __del__(self):
        self.stop()
        self.timer = None

    @log_traceback
    def start(self):
        self.runnable(self.start_command)
        if not self.timer or str(self.timer.getState()) == "TERMINATED":
            self.timer = Timer(self.interval, self.runnable, [self.stop_command])
            self.timer.start()
        elif self.timer and str(self.timer.getState()) == "TIMED_WAITING":
            self.timer.stop()
            self.timer = Timer(self.interval, self.runnable, [self.stop_command])
            self.timer.start()

    @log_traceback
    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.runnable(self.stop_command)

    @log_traceback
    def runnable(self, command):
        self.log.info(type(self.items))
        if isinstance(self.items, list):
            for item in self.items:
                events.sendCommand(item, command)

        elif isinstance(self.items, type(GroupItem)):
            group_members = itemRegistry.getItem(self.items).allMembers
            for member in group_members:
                events.sendCommand(member, command)

        else:
            events.sendCommand(self.items, command)

@add_logger
class OnOffTimer(BaseTimer):
    """ OnOff timer """
    def __init__(self, interval, items):
        BaseTimer.__init__(self, interval, items, "ON", "OFF")

@add_logger
class DimmerTimer(BaseTimer):
    def __init__(self, interval, items):
        #self.start_command = config.dimmer_values[str(itemRegistry.getItem("SolarTime").state)]
        BaseTimer.__init__(self, interval, items, "25", "0")
