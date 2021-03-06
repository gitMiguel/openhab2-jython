from time import sleep

from core.log import logging, LOG_PREFIX, log_traceback

log = logging.getLogger(LOG_PREFIX + ".startup_delay")

log.info("Checking for initialized context")

while True:
    try:
        scriptExtension.importPreset("RuleSupport")
        if automationManager is not None:
            break
    except:
        log.info("Context not initialized yet... waiting 10s before checking again")
        sleep(10)

log.info("Context initialized... waiting 30s before allowing scripts to load")
sleep(30)
log.info("Complete")