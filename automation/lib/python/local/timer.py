import sys

from threading import Timer
from openhab.jsr223.scope import events
from openhab.jsr223.scope import itemRegistry 
#reload(sys.modules['openhab.jsr223'])
#from openhab.jsr223.scope import events
#from openhab.jsr223.scope import itemRegistry


import org.eclipse.smarthome.core.items.GroupItem as GroupItem

from openhab.log import add_logger, log_traceback
from local import config

"""
Timer classes for openHAB jython rules
"""

@add_logger
class BaseTimer(object):
    """ Base class for timers"""

    _timers={}

    def __init__(self, function=None, args=[], kwargs={}):
        self.setFunction(function, args, kwargs)

    def __del__(self):
        self.stop()
        self.timer = None

    def start(self, name=None, interval=60, items=None):
        if name not in self._timers:
            self._timers[name] = None
        self.log.debug(self._timers)

        self.interval = interval
        self.items = items
        self.startTimer(name)

    def startTimer(self, name):
        """ Start or reschedule timer """
        timer = self._timers[name]
        if not timer or str(timer.getState()) == "TERMINATED":
            timer = Timer(self.interval, self.function, self.args, self.kwargs)
            timer.start()
        elif timer and str(timer.getState()) == "TIMED_WAITING":
            timer.stop()
            timer = Timer(self.interval, self.function, self.args, self.kwargs)
            timer.start()

    def run(self):
        """ function that runs when timer expires or is stopped """ 
        pass

    def stop(self):
        """ Stop the timer and run function"""
        if self.timer:
            self.timer.cancel()
            self.timer = None
            self.run()

    def setFunction(self, function, args=[], kwargs={}):
        """Set function that runs when timer expires or is stopped"""
        self.function = function
        self.args = args
        self.kwargs = kwargs
        pass

@add_logger
class OffTimer(BaseTimer):
    """ Off timer """
    def __init__(self):
        BaseTimer.__init__(self, self.run)

    @log_traceback
    def run(self):
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
