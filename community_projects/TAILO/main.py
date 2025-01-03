import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import numpy as np
import cv2
import hailo
from enum import Enum
from playsound import playsound
import time
from treat_control import treat_control
from arm_control import arm_control
from collections import Counter


class Pet_State(Enum):    
    PET_IDLE = 0
    PET_HOMING = 1
    PET_NOT_CENTERED = 2
    PET_ON_COUCH = 3
    PET_LOCKED = 4

SEC = 30 #FPS
WARN_DURATION = 0
SHOOT_DURATION = 10
EVENTS_SIZE = 60 # "remember" 60 events for getting current event calc

events = []
cooldown_period = 0

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

def get_timestamp():
    return (round(time.time()))

def shoot_pet():
    print ("Shooting dog")
    #TODO: move treat to treat events

import threading
from playsound import playsound
import random

def play_sound_in_background(file_path):
    """
    Plays an audio file in the background using playsound.
    
    Args:
        file_path (str): Path to the audio file to play.
    """
    threading.Thread(target=playsound, args=(file_path,), daemon=True).start()

def treat_pet():
    print ("Treat dog")
    files = [
        'Tovaaaaa.mp3'
    ]
    random_file = random.choice(files)
    print(random_file)
    play_sound_in_background(f"./resources/{random_file}")
    treat_control.perform_treat_throw()


angle = 90
sign = 1
def scan_pet():
    global angle
    global sign
    print ("Scanning dog")
    step = sign * 1
    angle += step
    arm_control.set_arm_horizontal_angle(angle)
    # cur_angle = arm_control.read_arm_horizontal_angle()
    print(angle)
    if  angle>= 150 or angle <=30:
        sign *=-1

def warn_pet():
    print ("Warning dog")
    files = [
        'No.mp3',
        'brandyyyyyy.mp3',
        'foya.mp3'
        'mosko_barking.mp3'
    ]
    random_file = random.choice(files)
    print(random_file)
    play_sound_in_background(f"./resources/{random_file}")

def add_event(event):
    global events
    timestamp = get_timestamp()
    events.append((timestamp, event))
    if (len(events) > EVENTS_SIZE):
        events = events[1:]
    # print(f"Adding event {event} at {timestamp}")
    # print(f"events len {len(events)}")

def get_event_duration(event):
    flag=True
    events_list = reversed(events)
    for ev in events_list:
        if ev[1] == event and flag:
            stop_time = ev[0]
            start_time = ev[0]
            flag=False
        elif ev[1] == event and not flag:
            start_time = ev[0]
        elif ev[1] != event:
            return (stop_time - start_time)
    return 

def find_event_duration(target_event):
    """
    Finds the duration of a given event in a list of (timestamp, event) tuples.
    
    Args:
        events (list of tuples): List of (timestamp, event) tuples sorted by timestamp.
        target_event (str): The event for which the duration is to be calculated.
    
    Returns:
        int or float: The duration of the event in the same units as the timestamps, or 0 if not found.
    """
    # Filter timestamps for the target event
    timestamps = [timestamp for timestamp, event in events if event == target_event]
    
    # If no timestamps are found, return 0
    if not timestamps:
        return 0
    
    # Calculate the duration
    duration = max(timestamps) - min(timestamps)
    return duration

def left_or_right(dog_bbox):
     # Compute x_max and y_max for the dog's bounding box
    try:
        dog_x_min = dog_bbox.xmin()
        dog_y_min = dog_bbox.ymin()
        dog_height = dog_bbox.height()
        dog_width = dog_bbox.width()
    except:
        return
    dog_x_middle  = dog_x_min + (dog_width/2)
    local_sign = (dog_x_middle - 0.5)*-1 
    local_sign = local_sign/abs(local_sign)
    global angle
    print ("Centering dog")
    step = local_sign * 1
    angle += step
    if  angle>= 150 or angle <=30:
        return
    arm_control.set_arm_horizontal_angle(angle)
    # cur_angle = arm_control.read_arm_horizontal_angle()
    print(angle)
    return 


def is_pet_centered(dog_bbox):
     # Compute x_max and y_max for the dog's bounding box
    dog_x_min = dog_bbox.xmin()
    dog_y_min = dog_bbox.ymin()
    dog_height = dog_bbox.height()
    dog_width = dog_bbox.width()
    dog_x_middle  = dog_x_min + (dog_width/2)
    threshold = 0.1
    return  0.3 < dog_x_middle < 0.7


def is_pet_on_couch(dog_bbox, couch_bbox):
    """
    Determines if the dog's bounding box is fully contained within any of the couch bounding boxes.

    Args:
        dog_bbox (object): Bounding box of the dog with methods xmin(), ymin(), height(), and width().
        couch_bbox (list): List of bounding box objects of couches, each with methods xmin(), ymin(), height(), and width().

    Returns:
        bool: True if the dog's bounding box is fully contained within any couch's bounding box, False otherwise.
    """
    # Compute x_max and y_max for the dog's bounding box
    dog_x_min = dog_bbox.xmin()
    dog_y_min = dog_bbox.ymin()
    dog_height = dog_bbox.height()
    dog_width = dog_bbox.width()
    dog_x_max = dog_x_min + dog_width
    dog_y_max = dog_y_min + dog_height

    # Check against each couch bounding box
    for couch in couch_bbox:
        couch_x_min = couch.xmin()
        couch_y_min = couch.ymin()
        couch_height = couch.height()
        couch_width = couch.width()
        couch_x_max = couch_x_min + couch_width
        couch_y_max = couch_y_min + couch_height

        # Check if the dog's bounding box is fully contained within the current couch bounding box
        is_fully_within_x = dog_x_min >= couch_x_min and dog_x_max <= couch_x_max
        is_fully_within_y = dog_y_min >= couch_y_min and dog_y_max <= couch_y_max

        if is_fully_within_x and is_fully_within_y:
            return True

    return False


def get_current_event():
    event_names = [event for _, event in events]
    event_counter = Counter(event_names)
    event_to_reduce = Pet_State.PET_HOMING
    new_count = event_counter[event_to_reduce] // 3
    # Create a new list with the reduced occurrences
    reduced_events = []
    for event in events:
        if event == event_to_reduce and event_counter[event_to_reduce] > new_count:
            event_counter[event_to_reduce] -= 1  # Skip occurrences to reduce count
        else:
            reduced_events.append(event)
    most_common_event, occurrences = event_counter.most_common(1)[0]
    print(f"The most popular event is '{most_common_event}' with {occurrences} occurrences.")

    return most_common_event
    # rev_events = reversed(events)
    # occurances = []
    # cnt = 0
    # for ev in Pet_State:
    #     occurances[ev] = 0
    # for event, timestamp in rev_events:        
    #     cnt += 1
    #     occurances[event] += 1
    #     if cnt >= EVENTS_SIZE:
    #         return occurances.index(max(occurances))

# This is the callback function that will be called when data is available from the pipeline
cur_event = None
def app_callback(pad, info, user_data):
    global cur_event
    global cooldown_period
    # Get the GstBuffer from the probe info
    buffer = info.get_buffer()
    # Check if the buffer is valid
    if buffer is None:
        return Gst.PadProbeReturn.OK

    # Using the user_data to count the number of frames
    user_data.increment()
    string_to_print = ""
    
    if (user_data.get_count() == 1):    
        string_to_print = """

      T A I L O 
           __
      (___()'`;
      /,    /`
      \\"--\\
    
    """

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
    pet_found = False
    chair_or_couch_bbox_list = []
    # print (detection.values())
    for detection in detections:
        if detection.get_label() in ["chair", "couch"]:
            chair_or_couch_bbox_list.append(detection.get_bbox())
    detection_map = {det.get_label(): det.get_bbox() for det in detections}
    dog_bbox = (detection_map.get("dog", None))

    if dog_bbox is None:
        add_event(Pet_State.PET_HOMING)
    else:
        if not is_pet_centered(dog_bbox):
            add_event(Pet_State.PET_NOT_CENTERED)
        else:
            if len(chair_or_couch_bbox_list) == 0:
                add_event (Pet_State.PET_LOCKED)
            else:
                if is_pet_on_couch(dog_bbox, chair_or_couch_bbox_list):
                    add_event(Pet_State.PET_ON_COUCH)
                #else if... (dog at the door? dog barking?)
                else:
                    add_event(Pet_State.PET_LOCKED)
    if cur_event is None:
        cur_event = Pet_State.PET_IDLE
    if cooldown_period < 1:
        prev_event = cur_event
        cur_event = get_current_event()
        print (f'{prev_event} --> {cur_event}')
        match(cur_event):
            case Pet_State.PET_HOMING:
                if prev_event == Pet_State.PET_ON_COUCH:
                    treat_pet()
                scan_pet() #Alon
                cooldown_period = 3

            case Pet_State.PET_NOT_CENTERED:
                print("track_pet")
                left_or_right(dog_bbox)
                cooldown_period = 3
            case Pet_State.PET_ON_COUCH:
                duration = find_event_duration(Pet_State.PET_ON_COUCH)
                if WARN_DURATION < duration < SHOOT_DURATION:
                    warn_pet()
                    cooldown_period = 5 * SEC
                elif duration >= SHOOT_DURATION:
                    shoot_pet() #shoot to kill
                    cooldown_period = 3 * SEC
                else: #less than warn duration, grace
                    cooldown_period = 1 * SEC
            case Pet_State.PET_LOCKED:
                if prev_event == Pet_State.PET_ON_COUCH:
                    treat_pet()

    cooldown_period -= 1

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

    if string_to_print != "":
        print(string_to_print)

    return Gst.PadProbeReturn.OK

if __name__ == "__main__":
    # Create an instance of the user app callback class
    user_data = user_app_callback_class()
    arm_control.enable_arm()
    arm_control.set_arm_horizontal_angle(90)
    treat_control.init_treat_control()
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
