import numpy as np
from typing import List, Dict
from .base_analyzer import BaseAnalyzer

class SquatAnalyzer(BaseAnalyzer):
    """
    Analyzes squat exercises for form and provides feedback.
    """
    
    @staticmethod
    def get_video_requirements() -> List[str]:
        """
        Returns a list of video requirements for squat analysis.
        """
        return [
            "Ensure your entire body is visible from the side.",
            "Place the camera at a height that captures your full range of motion.",
            "Use a stable camera with good lighting."
        ]

    def analyze_form(self, pose_data: List[Dict], exercise_type: str = 'squat') -> Dict:
        """
        Analyzes the quality of squat form based on pose data.
        
        Args:
            pose_data: A list of dictionaries, where each dictionary represents
                       the pose data for a single frame.
                       
        Returns:
            A dictionary containing the form score and feedback.
        """
        if not pose_data:
            return {'score': 0, 'feedback': ['No pose data available']}

        feedback = []
        score = 100

        # Helper to get landmark coordinates
        def get_landmark(frame_landmarks, landmark_name, landmark_map):
            return frame_landmarks[landmark_map[landmark_name]]

        landmark_map = pose_data[0]['landmark_map']
        knee_angles = [frame['angles'].get('left_knee', 180) for frame in pose_data]
        hip_angles = [frame['angles'].get('left_hip', 180) for frame in pose_data]
        
        # 1. Range of Motion
        min_knee_angle = min(knee_angles)
        max_knee_angle = max(knee_angles)
        if max_knee_angle < 160:
            feedback.append("Not fully extending knees at the top.")
            score -= 15
        if min_knee_angle > 100:
            feedback.append("Squat depth is too shallow. Aim for at least 90 degrees.")
            score -= 15

        # 2. Knee Position (Knees over Toes)
        bottom_frame_idx = np.argmin(knee_angles)
        bottom_frame_landmarks = pose_data[bottom_frame_idx]['landmarks']
        knee_x = get_landmark(bottom_frame_landmarks, 'left_knee', landmark_map)[0]
        ankle_x = get_landmark(bottom_frame_landmarks, 'left_ankle', landmark_map)[0]
        if knee_x > ankle_x + 0.05:
            feedback.append("Knees are travelling too far forward over toes.")
            score -= 20
            
        # 3. Back Posture
        if min(hip_angles) < 60:
            feedback.append("Lower back may be rounding. Keep your chest up.")
            score -= 10

        # Final Score and Feedback
        score = max(0, score)
        if not feedback:
            feedback.append("Good form detected!")

        if score >= 90:
            feedback.append("Excellent overall form!")
        elif score >= 70:
            feedback.append("Good form, but with room for minor improvements.")
        else:
            feedback.append("Form needs significant work. Focus on the feedback provided.")

        # Try ML model first, then fallback to rule-based
        ml_result = super().analyze_form(pose_data, exercise_type)
        if ml_result.get('method') == 'ml_model':
            return ml_result
        
        # Rule-based analysis (original logic)
        return {
            'score': score,
            'feedback': feedback,
            'method': 'rule_based'
        }
    
    def _rule_based_analysis(self, pose_data: List[Dict]) -> Dict:
        """Original rule-based squat analysis"""
        if not pose_data:
            return {'score': 0, 'feedback': ['No pose data available'], 'method': 'rule_based'}

        feedback = []
        score = 100

        # Helper to get landmark coordinates
        def get_landmark(frame_landmarks, landmark_name, landmark_map):
            return frame_landmarks[landmark_map[landmark_name]]

        landmark_map = pose_data[0]['landmark_map']
        knee_angles = [frame['angles'].get('left_knee', 180) for frame in pose_data]
        hip_angles = [frame['angles'].get('left_hip', 180) for frame in pose_data]
        
        # 1. Range of Motion
        min_knee_angle = min(knee_angles)
        max_knee_angle = max(knee_angles)
        if max_knee_angle < 160:
            feedback.append("Not fully extending knees at the top.")
            score -= 15
        if min_knee_angle > 100:
            feedback.append("Squat depth is too shallow. Aim for at least 90 degrees.")
            score -= 15

        # 2. Knee Position (Knees over Toes)
        bottom_frame_idx = np.argmin(knee_angles)
        bottom_frame_landmarks = pose_data[bottom_frame_idx]['landmarks']
        knee_x = get_landmark(bottom_frame_landmarks, 'left_knee', landmark_map)[0]
        ankle_x = get_landmark(bottom_frame_landmarks, 'left_ankle', landmark_map)[0]
        if knee_x > ankle_x + 0.05:
            feedback.append("Knees are travelling too far forward over toes.")
            score -= 20
            
        # 3. Back Posture
        if min(hip_angles) < 60:
            feedback.append("Lower back may be rounding. Keep your chest up.")
            score -= 10

        # Final Score and Feedback
        score = max(0, score)
        if not feedback:
            feedback.append("Good form detected!")

        if score >= 90:
            feedback.append("Excellent overall form!")
        elif score >= 70:
            feedback.append("Good form, but with room for minor improvements.")
        else:
            feedback.append("Form needs significant work. Focus on the feedback provided.")

        return {
            'score': score,
            'feedback': feedback,
            'method': 'rule_based'
        }
