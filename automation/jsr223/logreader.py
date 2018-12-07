from time import sleep
from openhab.rules import rule
from openhab.triggers import when
from openhab.actions import Telegram

error_list = []

@rule("SendLogReaderMessage")
@when("Time cron 0 0/15 * * * ?")

def execute(event, log):
	global error_list
	global message
	if len(error_list) != 0:
		message = "Errors in log: {}\n\n".format(len(error_list))
		for index, msg in enumerate(error_list):
			message += "[{}/{}]\n {}\n\n".format(index + 1, len(error_list), msg.replace("[ERROR]", ""))
		Telegram.sendTelegram("LanteeBot", message)
		error_list = []
		events.sendCommand("LogReaderErrors", "0")


@rule("LogReader")
@when("Channel logreader:reader:openhablog:newErrorEvent triggered")

def execute(event, log):
	global error_list
	error_list.append(event.getEvent())


@rule("LogReaderTest")
@when("Item Test2 changed")

def execute(event, log):
	log.error("Test error")
