# occupied_state modular service

This module implements the [rdk sensor API](https://github.com/rdk/sensor-api) in a etorkos:translation:occupied_state model.
With this model, you receive detections from a ML detection model and convert said detections into binary sensor output. You can find this model in the Viam Registry.

## Build and Run

To use this module, follow these instructions to [add a module from the Viam Registry](https://docs.viam.com/registry/configure/#add-a-modular-resource-from-the-viam-registry) and select the `rdk:sensor:etorkos:translation:occupied_state` model from the [`etorkos:translation:occupied_state` module](https://app.viam.com/module/rdk/etorkos:translation:occupied_state).

## Configure your sensor

> [!NOTE]  
> Before configuring your sensor, you must [create a machine](https://docs.viam.com/manage/fleet/machines/#add-a-new-machine).

Navigate to the **Config** tab of your robot’s page in [the Viam app](https://app.viam.com/).
Click on the **Components** subtab and click **Create component**.
Select the `sensor` type, then select the `etorkos:translation:occupied_state` model. 
Enter a name for your sensor and click **Create**.

On the new component panel, copy and paste the following attribute template into your sensor’s **Attributes** box:

```json
  {
    "confidence_threshold": 0.8,
    "detector_name": "person_detection_service",
    "vision_label": "person",
    "camera_name": "camera-1"
  }
```

Notes: 
For this service to work correctly you will need to set the "Depends on" field to the same as the detector name in the json above.
To see readings populate you will need to enable the data capture service on the sensor.

> [!NOTE]  
> For more information, see [Configure a Robot](https://docs.viam.com/manage/configuration/).

### Attributes

The following attributes are available for `rdk:sensor:etorkos:translation:occupied_state` sensors:

| Name | Type | Inclusion | Description |
| ---- | ---- | --------- | ----------- |
| `camera_name` | string | **Required** |  The name of the camera supplying the video feed |
| `confidence_threshold` | float | **Required** |  The threshold between 0 and 1 for which a matched image will successfully classify |
| `detector_name` | string | **Required** |  The name of the ML detection service |
| `vision_label` | string | **Required** |  The label that the detection service will match |

### Example Configuration

```json
  {
    "confidence_threshold": 0.8,
    "detector_name": "person_detection_service_name",
    "vision_label": "person",
    "camera_name": "camera-1"
  }
```

### Next Steps

Todos: 
- It shouldn't be necessary to have the detector name as and threshold as inputs if the service with those settings is a dependency. 
- Investigate how to remove them.


## Troubleshooting

