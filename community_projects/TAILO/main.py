import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo
from enum import Enum

class Pet_State(Enum):
    PET_HOMING = 1
    PET_NOT_CENTERED = 2
    PET_ON_COUCH = 3
    PET_LOCKED = 3

from hailo_rpi_common import (
    get_caps_from_pad,
    get_numpy_from_buffer,
    app_callback_class,
)
from detection_pipeline import GStreamerDetectionApp


# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
class user_app_callback_class(app_callback_class):
    def __init__(self):
        super().__init__()
        self.new_variable = 42  # New variable example

    def new_function(self):  # New function example
        return "The meaning of life is: "

# -----------------------------------------------------------------------------------------------
# User-defined callback function
# -----------------------------------------------------------------------------------------------

# This is the callback function that will be called when data is available from the pipeline
def app_callback(pad, info, user_data):
    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK

    # Using the user_data to count the number of frames
    user_data.increment()
    if (user_data.get_count() == 1):
        string_to_print = "-= Tailo =-"

    # Get the caps from the pad
    format, width, height = get_caps_from_pad(pad)

    # If the user_data.use_frame is set to True, we can get the video frame from the buffer
    frame = None
    if user_data.use_frame and format is not None and width is not None and height is not None:
        # Get video frame
        frame = get_numpy_from_buffer(buffer, format, width, height)

    # Get the detections from the buffer
    roi = hailo.get_roi_from_buffer(buffer)
    detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

    # Parse the detections
    detection_count = 0
    for detection in detections:
        label = detection.get_label()
        bbox = detection.get_bbox()
        # confidence = detection.get_confidence()
        if label == "person":
            # string_to_print += 
            detection_count += 1
    if user_data.use_frame:
        # Note: using imshow will not work here, as the callback function is not running in the main thread
        # Let's print the detection count to the frame
        cv2.putText(frame, f"Detections: {detection_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Example of how to use the new_variable and new_function from the user_data
        # Let's print the new_variable and the result of the new_function to the frame
        cv2.putText(frame, f"{user_data.new_function()} {user_data.new_variable}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Convert the frame to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        user_data.set_frame(frame)

    if string_to_print is not None:
        print(string_to_print)

    return Gst.PadProbeReturn.OK

if __name__ == "__main__":
    # Create an instance of the user app callback class
    user_data = user_app_callback_class()
    app = GStreamerDetectionApp(app_callback, user_data)
    app.run()


# Pseudo Code:

# # Start Homing
# if dog not in frame:
#     add_event(pet_homing)    
# else #dog in frame:
#     if dog not in middle of frame:
#         add_event(pet_not_centered)        
#     else # Locked                
#         if dog on couch:
#             add_event(pet_on_couch)
#         else if .... (near the door? barking?)
#         else 
#             add_event(pet_locked)
            
# prev_event = cur_event
# cur_event = max(events) #most common event

# cooldown_period = 30
# if not cooldown_period:
#     switch (cur_event)
#         missing_dog: scan_dog, cooldown_period = 30
#         dog_not_centered: move arm, cooldown_period = 50
#         dog_on_couch: 
#             if dog_on_couch_cnt > 100: warn_dog, cooldown_period = 200
#             if dog_on_couch_cnt > 500: shoot_dog, cooldown_period = 200
#         dog_in_frame:
#             if prev_event is dog_on_couch give treat