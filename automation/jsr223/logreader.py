from time import sleep
from openhab.rules import rule
from openhab.triggers import when
from openhab.actions import Telegram

@rule("LogReader Alarm")
@when("Channel logreader:reader:openhablog:newErrorEvent triggered")

def execute(event, log):
	pass
    #Telegram.sendTelegram("LanteeBot", message)

	#when
    #	Item logwatcherLastRead changed
	#then
	#	Thread::sleep(2000)
    #	if (logwatcherErrors.state > 0) {
	#		sendTelegram("LanteeBot", "LogReader alarm!\n\n" + logwatcherErrors.state.toString + " Errors in log! Heres the last one:\n\n" + logwatcherLastEline.state.toString)
	#	}
  	#end