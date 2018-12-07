import sys

from threading import Timer
from openhab.jsr223.scope import events
from openhab.jsr223.scope import itemRegistry 

import org.eclipse.smarthome.core.items.GroupItem

#reload(sys.modules['openhab.jsr223'])
#from openhab.jsr223.scope import events
#from openhab.jsr223.scope import itemRegistry

from openhab.log import add_logger, log_traceback
from local import config

"""
Timer classes for openHAB jython rules
"""

@add_logger
class BaseTimer(object):
    """ Base class for timers"""
    def __init__(self, interval, function, args=[], kwargs={}):
        self.timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.stop()
        self.timer = None

    def start(self):
        if not self.timer or str(self.timer.getState()) == "TERMINATED":
            self.timer = Timer(self.interval, self.function, self.args, self.kwargs)
            self.timer.start()
        elif self.timer and str(self.timer.getState()) == "TIMED_WAITING":
            self.timer.stop()
            self.timer = Timer(self.interval, self.function, self.args, self.kwargs)
            self.timer.start()

    def stop(self):
        """ Stop the timer and run function"""
        if self.timer:
            self.timer.cancel()
            self.run(self.args, self.kwargs)
            self.timer = None

    def setFunction(self, function, args=[], kwargs={}):
        """Set function that runs when timer ends or is stopped"""
        pass

@add_logger
class OffTimer(BaseTimer):
    """ Off timer """
    def __init__(self, interval, items):
        BaseTimer.__init__(self, interval, self.runnable)
        self.items = items

    @log_traceback
    def runnable(self):
        if isinstance(self.items, list):
            for item in self.items:
                events.sendCommand(item, "OFF")
        elif isinstance(self.items, GroupItem):
            group_members = itemRegistry.getItem(self.items.name).members
            for member in group_members:
                events.sendCommand(member, "OFF")
        else:
            events.sendCommand(self.items, "OFF")

@add_logger
class DimmerTimer(BaseTimer):
    def __init__(self, interval, items):
        BaseTimer.__init__(self, interval, items, "25", "0")
