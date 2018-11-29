from time import sleep
import org.joda.time.DateTime as DateTime
from openhab.rules import rule
from openhab.triggers import when

@rule("SolarTime")
@when("Item Test2 changed")
@when("Item StartTrigger changed")
@when("Channel astro:sun:ketola:rise#event triggered START")
@when("Channel astro:sun:ketola:set#event triggered START")
@when("Channel astro:sun:ketola:civilDawn#event triggered START")
@when("Channel astro:sun:ketola:civilDusk#event triggered START")
@when("Channel astro:sun:ketola:civilDusk#event triggered END")

def execute(event, log):
    log.info("Calculating solartime")

    dawn_start = ir.getItem("Astro_CivilDawnStart").getState().calendar.timeInMillis
    day_start = ir.getItem("Astro_Sunrise").getState().calendar.timeInMillis
    dusk_start = ir.getItem("Astro_CivilDuskStart").getState().calendar.timeInMillis
    night_start = ir.getItem("Astro_CivilDuskEnd").getState().calendar.timeInMillis
    curr = None

    sleep(2) # We seem to need this
    now = DateTime().getMillis()

    if now >= dawn_start and now < day_start:
        curr = "DAWN"
    elif now >= day_start and now < dusk_start:
        curr = "DAY"
    elif now >= dusk_start and now < night_start:
        curr = "DUSK"
    else:
        curr = "NIGHT"
    log.info("Solar time is now: {}".format(curr))
    events.sendCommand("SolarTime", curr)