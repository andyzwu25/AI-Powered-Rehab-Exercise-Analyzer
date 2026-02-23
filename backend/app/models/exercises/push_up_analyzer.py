import numpy as np
from typing import List, Dict
from .base_analyzer import BaseAnalyzer

class PushUpAnalyzer(BaseAnalyzer):
    """
    Analyzes push-up exercises for form and provides feedback.
    """
    
    @staticmethod
    def get_video_requirements() -> List[str]:
        """
        Returns a list of video requirements for push-up analysis.
        """
        return [
            "Ensure your entire body is visible from the side.",
            "Place the camera at a height level with your body.",
            "Use a stable camera with good lighting."
        ]

    def analyze_form(self, pose_data: List[Dict], exercise_type: str = 'push_up') -> Dict:
        """
        Analyzes the quality of push-up form based on pose data.
        
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
        hip_angles = [frame['angles'].get('left_hip', 180) for frame in pose_data]
        
        # 1. Range of Motion
        min_elbow_angle = min(elbow_angles)
        max_elbow_angle = max(elbow_angles)
        if max_elbow_angle < 160:
            feedback.append("Elbows not locking out at the top.")
            score -= 15
        if min_elbow_angle > 105:
            feedback.append("Not going deep enough at the bottom.")
            score -= 15

        # 2. Control (Hip Sagging)
        avg_hip_angle = np.mean(hip_angles)
        if avg_hip_angle < 150:
            feedback.append("Hips are sagging. Maintain a straight body line.")
            score -= 20

        # 3. Hand Placement
        bottom_frame_idx = np.argmin(elbow_angles)
        bottom_frame_landmarks = pose_data[bottom_frame_idx]['landmarks']
        elbow_x = get_landmark(bottom_frame_landmarks, 'left_elbow', landmark_map)[0]
        wrist_x = get_landmark(bottom_frame_landmarks, 'left_wrist', landmark_map)[0]
        if abs(elbow_x - wrist_x) > 0.1:
            feedback.append("Hands may be placed too far forward or back, causing poor elbow alignment.")
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
        """Original rule-based push-up analysis"""
        if not pose_data:
            return {'score': 0, 'feedback': ['No pose data available'], 'method': 'rule_based'}

        feedback = []
        score = 100

        # Helper to get landmark coordinates
        def get_landmark(frame_landmarks, landmark_name, landmark_map):
            return frame_landmarks[landmark_map[landmark_name]]

        landmark_map = pose_data[0]['landmark_map']
        elbow_angles = [frame['angles'].get('left_elbow', 180) for frame in pose_data]
        hip_angles = [frame['angles'].get('left_hip', 180) for frame in pose_data]
        
        # 1. Range of Motion
        min_elbow_angle = min(elbow_angles)
        max_elbow_angle = max(elbow_angles)
        if max_elbow_angle < 160:
            feedback.append("Elbows not locking out at the top.")
            score -= 15
        if min_elbow_angle > 105:
            feedback.append("Not going deep enough at the bottom.")
            score -= 15

        # 2. Control (Hip Sagging)
        avg_hip_angle = np.mean(hip_angles)
        if avg_hip_angle < 150:
            feedback.append("Hips are sagging. Maintain a straight body line.")
            score -= 20

        # 3. Hand Placement
        bottom_frame_idx = np.argmin(elbow_angles)
        bottom_frame_landmarks = pose_data[bottom_frame_idx]['landmarks']
        elbow_x = get_landmark(bottom_frame_landmarks, 'left_elbow', landmark_map)[0]
        wrist_x = get_landmark(bottom_frame_landmarks, 'left_wrist', landmark_map)[0]
        if abs(elbow_x - wrist_x) > 0.1:
            feedback.append("Hands may be placed too far forward or back, causing poor elbow alignment.")
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
