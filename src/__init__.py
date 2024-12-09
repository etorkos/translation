"""
This file registers the model with the Python SDK.
"""

from viam.components.sensor import Sensor
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .occupied_state import occupied_state

Registry.register_resource_creator(Sensor.SUBTYPE, occupied_state.MODEL, ResourceCreatorRegistration(occupied_state.new, occupied_state.validate))
