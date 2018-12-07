from time import sleep
from openhab.rules import rule
from openhab.triggers import when

@rule("GreenlinePumpStates")
@when("Item Test2 changed")
@when("Item ivtHeatPumpLamp changed")
@when("Item ivtHotWaterLamp changed")

def execute(event, log):
    sleep(1)
    pump_lamp = str(ir.getItem("ivtHeatPumpLamp").state)
    water_lamp = str(ir.getItem("ivtHotWaterLamp").state)
    pump_state = str(ir.getItem("IvtPumpState").state)

    if pump_lamp == "1" and water_lamp == "0":
	    if pump_state != "Kiertovesi":
		    events.postUpdate("IvtPumpState", "Kiertovesi")
		    log.debug("Pump is heating floor")

    elif pump_lamp == "1" and water_lamp == "1":
	    if pump_state != "Käyttövesi":
		    events.postUpdate("IvtPumpState", "Käyttövesi")
		    log.debug("Pump is heating water")

    elif pump_lamp == "0":
        if pump_state != "Lepo":
		    events.postUpdate("IvtPumpState", "Lepo")
		    log.debug("Heatpump off")
    else:
        log.debug("Error getting pump state")
