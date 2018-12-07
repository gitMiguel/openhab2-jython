import sys, os

from time import sleep
from openhab.rules import rule
reload(sys.modules['openhab.rules'])
from openhab.rules import rule

from openhab.triggers import when
from local import config
from local.timer import OffTimer

@rule("Presence_test")
@when("Item Test changed")
@when("Member of GrMotion changed to ON")

def execute(event, log):
    reload(sys.modules['local.timer'])
    from local.timer import OffTimer

    if event.itemName == "Test":
        room = "Fireplace"
        group = "GrMotion_Fireplace"
    else:
        group,room = event.itemName.split('_')
        #room = parts[1]
        #group = event.itemName

    log.debug("Presence detected in room: {}".format(room))
    illumination = filter(lambda item: item.name.find(room), ir.getItem("GrIllumination").members)[0]    
    log.debug("Illumination: {}".format(illumination.state))

    if illumination.state.intValue() <= config.illumination_states[str(ir.getItem("SolarTime").state)] or event.itemName == "Test":

        light_group =  "GrLights_" + str(room)
        item2 = ir.getItem(light_group)
        lights = filter(lambda item: item.name.find(room), ir.getItem(light_group).members)
        for item in lights:
            events.sendCommand(item, config.dimmer_values[str(ir.getItem("SolarTime").state)])        

        x = OffTimer(60, item2)
        x.start()
