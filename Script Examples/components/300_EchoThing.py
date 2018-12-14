"""
This is a very experimental Thing implementation. It writes values from its input channel
to the state of the items linked to the output channel. It requires several other components:

    * JythonThingTypeProvider
    * JythonBindingInfoProvider
    
Note: there are load ordering issues that will need to be resolved.
"""
from org.eclipse.smarthome.core.thing import ThingTypeUID, ChannelUID
from org.eclipse.smarthome.core.thing.type import ThingType, ChannelTypeUID, ChannelType, ChannelDefinition
from org.eclipse.smarthome.core.thing.binding import ThingFactory, ThingHandlerFactory, BaseThingHandlerFactory, BaseThingHandler, ThingTypeProvider
from org.eclipse.smarthome.core.binding import BindingInfo, BindingInfoProvider

import core
from core.osgi import register_service, unregister_service, get_service

BINDING_ID = "jython"
INPUT_CHANNEL_NAME = "input"
OUTPUT_CHANNEL_NAME = "output"

THING_NAME = "echo"
THING_TYPE_UID = ThingTypeUID(BINDING_ID, THING_NAME)

config_description_registry = get_service("org.eclipse.smarthome.config.core.ConfigDescriptionRegistry")
thing_type_registry = get_service("org.eclipse.smarthome.core.thing.type.ThingTypeRegistry")

log = core.log.logging.getLogger("{}.{}".format(BINDING_ID, THING_NAME))

class EchoThingHandler(BaseThingHandler):
    def __init__(self, thing):
        BaseThingHandler.__init__(self, thing)
        self.input_channel_id = ChannelUID(thing.getUID(), INPUT_CHANNEL_NAME)
        self.output_channel_id = ChannelUID(thing.getUID(), OUTPUT_CHANNEL_NAME)
        log.debug('output_channel_id: %s', self.output_channel_id)

    def handleCommand(self, channelUID, command):
        log.debug('handleCommand: %s %s', channelUID, command)

    def handleUpdate(self, channelUID, newState):
        log.debug('handleUpdate %s %s', channelUID, newState)
        self.updateState(self.output_channel_id, newState)

class EchoThingHandlerFactory(ThingHandlerFactory):
    def supportsThingType(self, thingTypeUID):
        log.debug('supportsThingType: %s', thingTypeUID)
        return thingTypeUID == THING_TYPE_UID

    def createHandler(self, thing):
        try:
            log.debug('createHandler: %s', thing)
            if thing.getThingTypeUID() == THING_TYPE_UID:
                return EchoThingHandler(thing)
        except:
            import traceback
            print traceback.format_exc()

    def createThing(self, thingTypeUID, configuration, thingUID, bridgeUID):
        try:
            log.debug('createThing: %s %s %s %s', thingTypeUID, configuration, thingUID, bridgeUID)
            thing_type = thing_type_registry.getThingType(thingTypeUID)
            log.debug('thing_type: %s', thing_type)
            thing = ThingFactory.createThing(
                thing_type, thingUID, configuration,
                bridgeUID, config_description_registry)
            log.debug('thing: %s', thing)
            return thing
        except:
            import traceback
            print traceback.format_exc()
    
    def registerHandler(self, thing):
        log.debug('registerHandler: %s', thing)
        return self.createHandler(thing)
    
    def unregisterHandler(self, thing):
        log.debug('unregisterHandler: %s', thing)
    
    def removeThing(self, thingUID):
        log.debug('removeThing: %s', thingUID)

# NOTE: Required mod to Bundle veto component

#
# ThingType
#

#input_channel_type = ChannelType(
#    input_channel_type_uid, False,  "String",  "Echo Input Item", 
#    "Input item who's value will be echoed", None, None, None, None)
 
#output_channel_type = ChannelType(
#    output_channel_type_uid, False,  "String",  "Echo Output Item", 
#    "Output item to receive echoed", None, None, None, None)

core.JythonThingTypeProvider.add(
    ThingType(
        THING_TYPE_UID, [], "Jython Echo", "Echos input channel to output channel", True, 
        [
            ChannelDefinition(INPUT_CHANNEL_NAME, ChannelTypeUID(BINDING_ID, INPUT_CHANNEL_NAME), None, None, None), 
            ChannelDefinition(OUTPUT_CHANNEL_NAME, ChannelTypeUID(BINDING_ID, OUTPUT_CHANNEL_NAME), None, None, None)
        ], [], {}, None
    )
)

#
# Binding Info
#

core.JythonBindingInfoProvider.add(
    BindingInfo(
        BINDING_ID, "Jython Binding", "Experimental binding written in Jython", 
        None, None, None
    )
)

service = EchoThingHandlerFactory()

def scriptLoaded(id):
    register_service(service, ["org.eclipse.smarthome.core.thing.binding.ThingHandlerFactory"])

def scriptUnloaded():
    unregister_service(service)