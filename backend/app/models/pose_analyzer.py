import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional
import math
from .exercises.pull_up_analyzer import PullUpAnalyzer
from .exercises.push_up_analyzer import PushUpAnalyzer
from .exercises.squat_analyzer import SquatAnalyzer

class PoseAnalyzer:
    def __init__(self):
        """Initialize the pose analyzer (MediaPipe not available)"""
        # MediaPipe is not available, so we'll provide a mock implementation
        self.mediapipe_available = False
        try:
            import mediapipe as mp
            self.mp_pose = mp.solutions.pose
            self.mp_drawing = mp.solutions.drawing_utils
            self.pose = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=2,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            self.mediapipe_available = True
        except ImportError:
            print("MediaPipe not available. Running in demo mode.")
            self.mediapipe_available = False
        
        # Define key pose landmarks
        self.landmarks = {
            'nose': 0,
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28
        }
        
        # Exercise detection thresholds
        self.exercise_analyzers = {
            'pull_up': PullUpAnalyzer,
            'push_up': PushUpAnalyzer,
            'squat': SquatAnalyzer
        }

    def analyze_exercise(self, file_path: str, exercise_type: str) -> Dict:
        """Analyze exercise form from video or image file"""
        try:
            if exercise_type not in self.exercise_analyzers:
                raise ValueError(f"Unsupported exercise type: {exercise_type}")

            if not self.mediapipe_available:
                return self._demo_analysis(file_path, exercise_type)
            
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension in ['mp4', 'avi', 'mov']:
                return self._analyze_video(file_path, exercise_type)
            elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
                return self._analyze_image(file_path, exercise_type)
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis': None
            }

    def _analyze_video(self, video_path: str, exercise_type: str) -> Dict:
        """Analyze exercise form from video file"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError("Could not open video file")
        
        frame_count = 0
        pose_data = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % 5 == 0:
                frame_analysis = self._analyze_frame(frame)
                if frame_analysis['pose_detected']:
                    pose_data.append(frame_analysis)
            
            frame_count += 1
        
        cap.release()
        
        if not pose_data:
            return {
                'success': False,
                'error': 'No pose detected in video',
                'analysis': None
            }
        
        # Analyze form quality
        form_analysis = self._analyze_form_quality(pose_data, exercise_type)
        
        return {
            'success': True,
            'exercise_type': exercise_type,
            'analysis': form_analysis,
            'frame_count': len(pose_data)
        }

    def _analyze_image(self, image_path: str, exercise_type: str) -> Dict:
        """Analyze exercise form from image file"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image file")
        
        frame_analysis = self._analyze_frame(image)
        
        if not frame_analysis['pose_detected']:
            return {
                'success': False,
                'error': 'No pose detected in image',
                'analysis': None
            }
        
        form_analysis = self._analyze_form_quality([frame_analysis], exercise_type)
        
        return {
            'success': True,
            'exercise_type': exercise_type,
            'analysis': form_analysis,
            'frame_count': 1
        }

    def _analyze_frame(self, frame) -> Dict:
        """Analyze a single frame for pose detection"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        if not results.pose_landmarks:
            return {
                'pose_detected': False,
                'landmarks': None,
                'angles': None
            }
        
        # Extract landmarks
        landmarks = []
        for landmark in results.pose_landmarks.landmark:
            landmarks.append([landmark.x, landmark.y, landmark.z])
        
        # Calculate key angles
        angles = self._calculate_angles(landmarks)
        
        return {
            'pose_detected': True,
            'landmarks': landmarks,
            'angles': angles
        }

    def _calculate_angles(self, landmarks: List[List[float]]) -> Dict[str, float]:
        """Calculate key joint angles from landmarks"""
        angles = {}
        
        # Calculate shoulder angle (left)
        if all(landmarks[i] for i in [self.landmarks['left_hip'],
                                     self.landmarks['left_shoulder'],
                                     self.landmarks['left_elbow']]):
            angles['left_shoulder'] = self._calculate_angle(
                landmarks[self.landmarks['left_hip']],
                landmarks[self.landmarks['left_shoulder']],
                landmarks[self.landmarks['left_elbow']]
            )
        
        # Calculate elbow angle (left)
        if all(landmarks[i] for i in [self.landmarks['left_shoulder'], 
                                     self.landmarks['left_elbow'], 
                                     self.landmarks['left_wrist']]):
            angles['left_elbow'] = self._calculate_angle(
                landmarks[self.landmarks['left_shoulder']],
                landmarks[self.landmarks['left_elbow']],
                landmarks[self.landmarks['left_wrist']]
            )
        
        # Calculate hip angle (left)
        if all(landmarks[i] for i in [self.landmarks['left_shoulder'], 
                                     self.landmarks['left_hip'], 
                                     self.landmarks['left_knee']]):
            angles['left_hip'] = self._calculate_angle(
                landmarks[self.landmarks['left_shoulder']],
                landmarks[self.landmarks['left_hip']],
                landmarks[self.landmarks['left_knee']]
            )
        
        # Calculate knee angle (left)
        if all(landmarks[i] for i in [self.landmarks['left_hip'], 
                                     self.landmarks['left_knee'], 
                                     self.landmarks['left_ankle']]):
            angles['left_knee'] = self._calculate_angle(
                landmarks[self.landmarks['left_hip']],
                landmarks[self.landmarks['left_knee']],
                landmarks[self.landmarks['left_ankle']]
            )
        
        # Right side angles (similar calculations)
        if all(landmarks[i] for i in [self.landmarks['right_hip'],
                                     self.landmarks['right_shoulder'],
                                     self.landmarks['right_elbow']]):
            angles['right_shoulder'] = self._calculate_angle(
                landmarks[self.landmarks['right_hip']],
                landmarks[self.landmarks['right_shoulder']],
                landmarks[self.landmarks['right_elbow']]
            )
        
        if all(landmarks[i] for i in [self.landmarks['right_shoulder'], 
                                     self.landmarks['right_elbow'], 
                                     self.landmarks['right_wrist']]):
            angles['right_elbow'] = self._calculate_angle(
                landmarks[self.landmarks['right_shoulder']],
                landmarks[self.landmarks['right_elbow']],
                landmarks[self.landmarks['right_wrist']]
            )
        
        return angles

    def _calculate_angle(self, a: List[float], b: List[float], c: List[float]) -> float:
        """Calculate angle between three points"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def analyze_exercise(self, file_path: str, exercise_type: str) -> Dict:
        """
        Analyze exercise form from a video file for a specific exercise type.
        """
        from .exercises.pull_up_analyzer import PullUpAnalyzer
        from .exercises.push_up_analyzer import PushUpAnalyzer
        from .exercises.squat_analyzer import SquatAnalyzer

        analyzers = {
            'pull_up': PullUpAnalyzer,
            'push_up': PushUpAnalyzer,
            'squat': SquatAnalyzer,
        }

        if exercise_type not in analyzers:
            return {'success': False, 'error': f"Invalid exercise type: {exercise_type}"}

        try:
            if not self.mediapipe_available:
                return self._demo_analysis(file_path)

            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                raise ValueError("Could not open video file")

            pose_data = []
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_analysis = self._analyze_frame(frame)
                if frame_analysis['pose_detected']:
                    # Add landmark map to each frame's data
                    frame_analysis['landmark_map'] = self.landmarks
                    pose_data.append(frame_analysis)
            
            cap.release()

            if not pose_data:
                return {'success': False, 'error': 'No pose detected in video'}

            # Get the specific analyzer and analyze the form
            analyzer_class = analyzers[exercise_type]
            analyzer = analyzer_class() if callable(analyzer_class) else analyzer_class
            form_analysis = analyzer.analyze_form(pose_data, exercise_type)

            return {
                'success': True,
                'exercise_type': exercise_type,
                'analysis': form_analysis,
                'frame_count': len(pose_data),
                'pose_data': pose_data  # Include pose data for feedback collection
            }

        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _demo_analysis(self, file_path: str) -> Dict:
        """Demo analysis when MediaPipe is not available"""
        # Determine file type
        file_extension = file_path.lower().split('.')[-1]
        
        # Mock analysis for demo purposes
        exercise_type = 'pull_up'  # Default for demo
        if file_extension in ['mp4', 'avi', 'mov']:
            exercise_type = 'push_up'
        elif file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            exercise_type = 'squat'
        
        return {
            'success': True,
            'exercise_type': exercise_type,
            'analysis': {
                'score': 85,  # Demo score
                'feedback': [
                    "Demo mode: This is a sample analysis since MediaPipe is not installed.",
                    "To get real pose analysis, install MediaPipe: pip install mediapipe",
                    "Your form looks good overall!",
                    "Keep your core engaged throughout the movement.",
                    "Maintain proper breathing during the exercise."
                ],
                'exercise_type': exercise_type
            },
            'frame_count': 1
        }
