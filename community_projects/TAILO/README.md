# TAILO - The Smart Companion for Your Dog

![TAILO_logo_sm](https://github.com/user-attachments/assets/49dd031c-6538-48e3-9aa8-d09c8ff93dc2)

## Overview 
TAILO is a cutting-edge AI-powered device designed to enhance the lives of pets and their owners. By combining advanced artificial intelligence with playful and practical features, TAILO ensures your dog stays happy, active, and monitored while you’re away. Whether it’s reinforcing good behavior, tracking daily activities, or providing interactive play, TAILO is the ultimate companion for your furry friend.

## Key Features

### 1. Reinforcement with Treats
- **Behavioral Reinforcement:** Dispense treats to reward pre-defined specific activities or good behavior, promoting a well-trained and happy dog.
  
### 2. Customized Voice Commands
- **Action-Based Prompts:** Configure personalized voice commands to play when specific actions are detected, such as encouraging your dog to sit, stay, or leave restricted areas.

### 3. Pet Tracking
- **Smart Camera Functionality:** Follows your dog’s movement and activities in defined areas. This allows focused tracking, such as observing time spent on the couch, near the door, or in a designated play zone.

### 4. Smart Monitoring - Roadmap Feature
TAILO provides a comprehensive overview of your dog’s daily activities, offering valuable insights to enhance their care and well-being:

- **Total Playtime:** Tracks the duration your dog spent playing with the ball or engaging with interactive features.
- **Steps Taken:** Estimates the total movement your dog achieved throughout the day.
- **Rest Periods:** Monitors total sleep or rest time, broken down into individual nap durations.
- **Activity Peaks:** Highlights the times of day when your dog was most active.
- **Positive Reinforcement:** Records the number of times treats were dispensed to encourage specific behaviors or commands.
- **Training Progress:** Tracks success in behavioral training, such as responsiveness to commands (e.g., “sit”) or avoiding restricted areas.
- **Bathroom Breaks:** Counts indoor accidents, such as the number of times your puppy peed or pooped.
- **Feeding Patterns:** Logs how often your dog accessed food or water, if integrated into the system.

### 5. Interactive Play - Roadmap Feature
- **Fetch with a Ball:** TAILO automatically engages your dog by tossing a ball upon a pre-defined trigger, keeping your pet entertained and active.

### 6. Screenshot Requests - Roadmap Feature
- **Activity Snapshots:** Users can request screenshots of specific activities, such as eating, sleeping, or playing, to stay visually informed about their dog’s day.

---

## Why TAILO?

- **Low Cost of Ownership:** Enjoy the benefits of TAILO without any monthly subscription fees.
- **Connectivity:** Always operational, independent of internet connectivity.
- **Privacy First:** Operates in a closed circle with no data transmitted to the cloud, ensuring your privacy.
- **Customizable:** TAILO is built for Makers. It allows users to define actionable events with free text, tailoring the experience to your needs.
  
---

## Who Is TAILO For?

- **Busy Pet Owners:** Perfect for those who want to ensure their dog is happy and engaged while they’re at work or away.
- **Training Enthusiasts:** Ideal for reinforcing positive behavior and maintaining a structured training routine.
- **Data-Driven Pet Parents:** Provides valuable insights into your dog’s habits and activities.


## Video
Here's a video submitted by TAILO's team at the HAILO 2024 MAD Hackathon

[![Watch the demo on YouTube](https://img.youtube.com/vi/XXizBHtCLew/0.jpg)](https://youtu.be/dAok4_63W8E)

## Setup Instructions
Enable Serial Port for the [Servo SG90](http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf) of the cannon.  
For the camera angular movment we are using [XL-320](https://emanual.robotis.com/docs/en/dxl/x/xl320/).  
For the 3D printed module to hold the camera we used [Poppy-Project](https://github.com/poppy-project/poppy-ergo-jr).  
For the camera we used the rpi camera module v2.   
And of course for the AI we used the [Hailo AI HAT](https://www.raspberrypi.com/products/ai-hat/).  
### Schematics
Raspberry pi GPIOs connections:  
GPIO 14 - UART TX connected to Robotics XR-320 servo motor.    
GPIO 15 - UART RX connected to Robotics XR-320 servo motor.  
GPIO 18 - PWM to trigger the treat launching with the SG90 servo.  

### Installation
### Navigate to the repository directory:
```bash
cd hailo-rpi5-puppy
```

### Environment Configuration  (Required for Each New Terminal Session)
Ensure your environment is set up correctly by sourcing the provided script. This script sets the required environment variables and activates the Hailo virtual environment. If the virtual environment does not exist, it will be created automatically.
```bash
source setup_env.sh
```
### Navigate to the example directory:
```bash
cd community_projects/TAILO/
```
### Requirements Installation
Within the activated virtual environment, install the necessary Python packages:
```bash
pip install -r requirements.txt
./download_resources.sh
```

## Usage
```bash
cd community_projects/TAILO
python main.py -i rpi
```
- To close the application, press `Ctrl+C`.
