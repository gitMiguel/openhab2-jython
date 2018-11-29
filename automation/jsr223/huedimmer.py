from time import sleep
from openhab.rules import rule
from openhab.triggers import when

'''
Hue dimmer switch button states

Button 1 (ON)
INITIAL_PRESSED	1000
HOLD	        1001
SHORT RELEASED	1002
LONG RELEASED	1003

Button 2 (DIM UP)
INITIAL_PRESSED	2000
HOLD	        2001
SHORT RELEASED	2002
LONG RELEASED	2003

Button 3 (DIM DOWN)
INITIAL_PRESSED	3000
HOLD	        3001
SHORT RELEASED	3002
LONG RELEASED	3003

Button 4 (OFF)
INITIAL_PRESSED	4000
HOLD	        4001
SHORT RELEASED	4002
LONG RELEASED	4003
'''

@rule("HueDimmerSwitch")
@when("Item hueDimmerSwitchButton changed")

def execute(event, log):
  
    state = str(event.itemState)
    #log.info("Buttonevent \"{}\"".format(state))

    if state == "4000.0":
        if ir.getItem("SonySimpleIP_Power").state == ON:
            events.sendCommand("SonySimpleIP_Power", "OFF")
            log.info("Turning Tv OFF")
        else:
            log.info("Tv already OFF")
    
    elif state == "1002.0":
        if ir.getItem("SonySimpleIP_Power").state == OFF:
            events.sendCommand("SonySimpleIP_Power", "ON")
            log.info("Turning Tv ON")
        else:
            log.info("Tv already ON")   

    elif state == "1003.0":
        if ir.getItem("SonySimpleIP_Power").state == OFF:
            events.sendCommand("SonySimpleIP_Power", "ON")
            sleep(10)
            events.sendCommand("SonySimpleIP_Input", "TV")
            sleep(10)
            events.sendCommand("SonySimpleIP_Channel", "2.0")
        else:
            events.sendCommand("SonySimpleIP_Input", "TV")
            sleep(10)
            events.sendCommand("SonySimpleIP_Channel", "2.0")

    elif state == "2002.0":
        events.sendCommand("SonySimpleIP_IR", "Channel-Up")
    elif state == "3002.0":
        events.sendCommand("SonySimpleIP_IR", "Channel-Down")
    
    else:
        #log.info("Unsupported buttonevent")
        pass