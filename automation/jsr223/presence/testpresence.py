import sys
from time import sleep
from openhab.rules import rule
from openhab.triggers import when
from local import config
from local.timer import OnOffTimer, DimmerTimer


@rule("Presence_test")
@when("Item Test changed")
@when("Member of GrMotion changed to ON")

def execute(event, log):
    reload(sys.modules['local.timer'])
    from local.timer import OnOffTimer, DimmerTimer

    if event.itemName == "Test":
        room = "Fireplace"
        group = "GrMotion_Fireplace"
    else:
        parts = event.itemName.split('_')
        room = parts[1]
        group = event.itemName

    log.info("Presence detected in room: {}".format(room))
    illumination = filter(lambda item: item.name.find(room), ir.getItem("GrIllumination").members)[0]    
    log.info("Illumination: {}".format(illumination.state))

    if illumination.state.intValue() <= config.illumination_states[str(ir.getItem("SolarTime").state)] or event.itemName == "Test":

        #lights = filter(lambda item: item.name.find(room), ir.getItem("GrLights").allMembers)
        #for item in lights:
        #    events.sendCommand(item, config.dimmer_values[str(ir.getItem("SolarTime").state)])

        lights = ir.getItem("GrLights_" + room)  

        x = OnOffTimer(60, lights)
        x.start()
        #sleep(2)
        #x.stop()
