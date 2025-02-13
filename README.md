# Vehicle Detection and Counting using YOLOv8 and SORT

This project demonstrates real-time vehicle detection and counting using YOLOv8 (You Only Look Once) for object detection and SORT (Simple Online and Realtime Tracking) for tracking vehicles. The system counts vehicles crossing a predefined line in a video and displays the count on the screen.
<video controls width="640">
  <source src="Results/Res_video.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


## Features
- **Real-time vehicle detection**: Uses YOLOv8 to detect vehicles such as cars, trucks, buses, and motorbikes.
- **Vehicle tracking**: Implements SORT to track detected vehicles across frames.
- **Counting mechanism**: Counts vehicles that cross a predefined line in the video.
- **GPU support**: Utilizes GPU acceleration if available for faster processing.

## Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
3. Download the YOLOv8 weights file (yolov8l.pt) and place it in the Yolo_Weights directory.

4. Prepare your input video and mask image:

  * Place your video file in the Videos directory (e.g., cars.mp4).
  
  * Create a mask image (mask.png) to define the region of interest (ROI) for vehicle detection
    
5. Run the script:
   ```bash
   python Car_Counter.py


## How It Works
  1. The script initializes the YOLOv8 model and checks if a GPU is available for faster processing.
  
  2. It reads the input video and applies a mask to focus on the ROI.
  
  3. YOLOv8 detects vehicles in the masked region, and SORT tracks them across frames.
  
  4. A predefined line is drawn on the video. When a vehicle's center crosses this line, it is counted.
  
  5. The total count of vehicles is displayed on the screen.

## Code Overview
  * YOLOv8 Model: Used for detecting vehicles in the video.

  * SORT Tracker: Tracks detected vehicles across frames.
  
  * Masking: A mask is applied to focus on the ROI.
  
  * Counting Logic: Vehicles are counted when their center crosses a predefined line.

## Acknowledgments
  * [Ultralytics YOLOv8](https://www.ultralytics.com/ar/yolo) for the object detection model.

  * [SORT](https://github.com/abewley/sort) for the tracking algorithm.

  * OpenCV for video processing.
