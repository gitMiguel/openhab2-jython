import sys
from openhab.rules import rule
from openhab.triggers import when
from openhab.jsr223 import scope
#from openhab import test

#from openhab.jsr223 import scope
#scope.scriptExtension.importPreset("RuleSimple")
#scope.scriptExtension.importPreset("RuleSupport")
#scope.scriptExtension.importPreset("RuleFactories")

#from org.slf4j import Logger, LoggerFactory

#log = LoggerFactory.getLogger("org.eclipse.smarthome.automation.core.internal.Test")

#log.warn(str(type(sys._getframe(1).f_globals)))

@rule("Globals_test")
@when("Item Test3 changed")


def execute(event, log):
    log.info(str(type(sys._getframe(1).f_globals)))
    log.info(str(scope.ir.getItem("SolarTime")))