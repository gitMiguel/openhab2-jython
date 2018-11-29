from openhab.rules import rule
from openhab.triggers import when


@rule("TimeOfDay")
#@when("Item Test changed")
@when("Time cron 0 1 0 * * ?")
@when("Time cron 0 0 6 * * ?")
@when("Time cron 0 0 23 * * ?")

def execute(event, log):
    log.info("Calculating time of day")