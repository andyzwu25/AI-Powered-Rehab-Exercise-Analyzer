import cv2
import os
import csv
import mediapipe as mp

# Standard initialization
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

print("SUCCESS: MediaPipe is working in the Virtual Environment!")
# 2. Define your folder paths
base_path = "data/raw/clamshell"
folders = ["good", "bad"]
output_base = "data/processed/clamshell"

# Create output directories if they don't exist
for folder in folders:
    os.makedirs(os.path.join(output_base, folder), exist_ok=True)

def process_video(video_path, csv_path):
    cap = cv2.VideoCapture(video_path)
    data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 3. Convert frame to RGB for MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            # 4. Extract all 33 landmarks (x, y, z, visibility)
            landmarks = []
            for lm in results.pose_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z, lm.visibility])
            data.append(landmarks)

    cap.release()

    # 5. Save landmarks to CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

# 6. Bulk Process Loop
for folder in folders:
    current_folder = os.path.join(base_path, folder)
    for filename in os.listdir(current_folder):
        if filename.endswith((".mp4", ".mov", ".webm")):
            video_input = os.path.join(current_folder, filename)
            csv_output = os.path.join(output_base, folder, filename.replace(os.path.splitext(filename)[1], ".csv"))
            
            print(f"Extracting landmarks from: {filename}...")
            process_video(video_input, csv_output)

print("All 102 videos processed! Your CSV data is ready in 'data/processed/'.")