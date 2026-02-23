import numpy as np
from typing import List, Dict
from .base_analyzer import BaseAnalyzer

class PullUpAnalyzer(BaseAnalyzer):
    """
    Analyzes pull-up exercises for form and provides feedback.
    """
    
    @staticmethod
    def get_video_requirements() -> List[str]:
        """
        Returns a list of video requirements for pull-up analysis.
        """
        return [
            "Ensure your entire body is visible from the side.",
            "Make sure your face is in view for nose detection.",
            "Use a stable camera with good lighting."
        ]

    def analyze_form(self, pose_data: List[Dict], exercise_type: str = 'pull_up') -> Dict:
        """
        Analyzes the quality of pull-up form based on pose data.
        
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
        elbow_angles = [frame['angles'].get('left_elbow', 180) for frame in pose_data]
        nose_y = [get_landmark(frame['landmarks'], 'nose', landmark_map)[1] for frame in pose_data]
        wrist_y = [get_landmark(frame['landmarks'], 'left_wrist', landmark_map)[1] for frame in pose_data]
        hip_x = [get_landmark(frame['landmarks'], 'left_hip', landmark_map)[0] for frame in pose_data]

        # 1. Range of Motion
        min_elbow_angle = min(elbow_angles)
        max_elbow_angle = max(elbow_angles)
        chin_above_bar = any(n < w for n, w in zip(nose_y, wrist_y))

        if max_elbow_angle < 160:
            feedback.append("Not reaching full extension at the bottom (elbows not straight).")
            score -= 20
        if not chin_above_bar:
            feedback.append("Chin does not appear to go above the bar.")
            score -= 20

        # 2. Control (Kipping/Swinging)
        hip_swing = np.std(hip_x) * 100
        if hip_swing > 3:
            feedback.append(f"Excessive hip swing detected ({hip_swing:.1f}% of screen width). Avoid kipping.")
            score -= 25

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
        """Original rule-based pull-up analysis"""
        if not pose_data:
            return {'score': 0, 'feedback': ['No pose data available'], 'method': 'rule_based'}

        feedback = []
        score = 100

        # Helper to get landmark coordinates
        def get_landmark(frame_landmarks, landmark_name, landmark_map):
            return frame_landmarks[landmark_map[landmark_name]]

        landmark_map = pose_data[0]['landmark_map']
        elbow_angles = [frame['angles'].get('left_elbow', 180) for frame in pose_data]
        nose_y = [get_landmark(frame['landmarks'], 'nose', landmark_map)[1] for frame in pose_data]
        wrist_y = [get_landmark(frame['landmarks'], 'left_wrist', landmark_map)[1] for frame in pose_data]
        hip_x = [get_landmark(frame['landmarks'], 'left_hip', landmark_map)[0] for frame in pose_data]

        # 1. Range of Motion
        min_elbow_angle = min(elbow_angles)
        max_elbow_angle = max(elbow_angles)
        chin_above_bar = any(n < w for n, w in zip(nose_y, wrist_y))

        if max_elbow_angle < 160:
            feedback.append("Not reaching full extension at the bottom (elbows not straight).")
            score -= 20
        if not chin_above_bar:
            feedback.append("Chin does not appear to go above the bar.")
            score -= 20

        # 2. Control (Kipping/Swinging)
        hip_swing = np.std(hip_x) * 100
        if hip_swing > 3:
            feedback.append(f"Excessive hip swing detected ({hip_swing:.1f}% of screen width). Avoid kipping.")
            score -= 25

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
