from typing import ClassVar, Mapping, Sequence, Any, Dict, Optional, Tuple, Final, List, cast
from typing_extensions import Self

from typing import Any, Final, Mapping, Optional

from viam.utils import SensorReading
from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName, Vector3
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from viam.services.vision import VisionClient
from viam.components.camera import Camera

from viam.components.sensor import *
from viam.app.viam_client import ViamClient
from viam.rpc.dial import DialOptions

#from sensor_python import Sensor
from viam.logging import getLogger

import time
import asyncio

LOGGER = getLogger(__name__)

class occupied_state(Sensor, Reconfigurable):
    
    """
    Sensor represents a physical sensing device that can provide measurement readings.
    """

    MODEL: ClassVar[Model] = Model(ModelFamily("etorkos", "translation"), "occupied_state")
    
    # create any class parameters here, 'some_pin' is used as an example (change/add as needed)
    detector_name: VisionClient
    camera_name: str
    vision_label: str
    confidence_threshold: float

    # Constructor
    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        # here we validate config, the following is just an example and should be updated as needed
        camera_name = config.attributes.fields["camera_name"].string_value
        if camera_name == "":
            raise Exception("camera_name attribute is required")
        vision_label = config.attributes.fields["vision_label"].string_value
        if vision_label == "":
            raise Exception("vision_label attribute is required")
        detector_name = config.attributes.fields["detector_name"].string_value
        if detector_name == "":
            raise Exception("detector_name attribute is required")
        confidence_threshold = config.attributes.fields["confidence_threshold"].number_value
        if confidence_threshold == "":
            raise Exception("confidence_threshold attribute is required")
        if confidence_threshold < 0 or confidence_threshold > 1:
            raise Exception("confidence_threshold attribute must be between 0 and 1")

    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        # here we initialize the resource instance, the following is just an example and should be updated as needed

        detector= config.attributes.fields["detector_name"].string_value
        actual_detector = dependencies[VisionClient.get_resource_name(detector)]
        self.detector = cast(VisionClient, actual_detector)

        self.camera = config.attributes.fields["camera_name"].string_value
        self.vision_label = config.attributes.fields["vision_label"].string_value
        self.confidence_threshold = config.attributes.fields["confidence_threshold"].number_value
        return

    """ Implement the methods the Viam RDK defines for the Sensor API (rdk:component:sensor) """

    async def get_readings(
        self, *, extra: Optional[Mapping[str, Any]] = None, timeout: Optional[float] = None, **kwargs
    ) -> Mapping[str, SensorReading]:
        
        detected = 0
        detections = await self.detector.get_detections_from_camera(self.camera)

        for d in detections:
            if d.class_name.lower() == self.vision_label and d.confidence >= self.confidence_threshold:
                detected = 1
                break

        return {
            "person_detected": detected
        }
    

