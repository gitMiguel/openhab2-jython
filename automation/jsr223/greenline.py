from time import sleep
from openhab.rules import rule
from openhab.triggers import when

@rule("GreenlinePumpStates")
@when("Item Test2 changed")
@when("Item ivtHeatPumpLamp changed")
@when("Item ivtHotWaterLamp changed")

def execute(event, log):
    sleep(1)
    pump_lamp = unicode(ir.getItem("ivtHeatPumpLamp").state)
    water_lamp = unicode(ir.getItem("ivtHotWaterLamp").state)
    pump_state = unicode(ir.getItem("IvtPumpState").state)

    if pump_lamp == "1" and water_lamp == "0":
	    if pump_state != u"Kiertovesi":
		    events.postUpdate("IvtPumpState", u"Kiertovesi")
		    log.debug("Pump is heating floor")

    elif pump_lamp == "1" and water_lamp == "1":
	    if pump_state != u"Käyttövesi":
		    events.postUpdate("IvtPumpState", u"Käyttövesi")
		    log.debug("Pump is heating water")

    elif pump_lamp == "0":
        if pump_state != u"Lepo":
		    events.postUpdate("IvtPumpState", u"Lepo")
		    log.debug("Heatpump off")
    else:
        log.debug("Error getting pump state")
