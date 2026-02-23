from .base_analyzer import BaseAnalyzer
from typing import List, Dict

class ClamAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__()
        self.exercise_name = "clam"

    def _rule_based_analysis(self, pose_data: List[Dict]) -> Dict:
        # Placeholder for rule-based analysis for Clams
        # In a real scenario, you would implement logic to check hip abduction, knee angle, etc.

        feedback = [
            "Rule-based analysis for Clam. Train an ML model for precise feedback.",
            "Keep your feet together throughout the movement.",
            "Focus on controlled movement, both opening and closing."
        ]
        score = 65 # Default score for rule-based

        # Simple heuristic: if there's any movement (multiple frames), give a slightly better score
        if len(pose_data) > 1:
            score = 75
            feedback.append("Movement detected, indicating an attempt at the exercise.")

        return {
            "score": score,
            "feedback": feedback,
            "method": "rule_based"
        }

    def _analyze_specific_issues(self, pose_data: List[Dict]) -> List[str]:
        # Placeholder for specific feedback for Clams
        specific_feedback = []
        # Example: Check for torso rotation (very basic)
        if pose_data:
            # Assuming shoulder and hip landmarks are present
            # This is a highly simplified example, real analysis would be more complex
            # Check if shoulders rotate significantly relative to hips
            if "landmark_map" in pose_data[0] and \
               pose_data[0]["landmark_map"].get("left_shoulder") is not None and \
               pose_data[0]["landmark_map"].get("right_shoulder") is not None and \
               pose_data[0]["landmark_map"].get("left_hip") is not None and \
               pose_data[0]["landmark_map"].get("right_hip") is not None:

                # Get initial shoulder and hip positions (simplified to y-coordinates for rotation check)
                initial_l_shoulder_y = pose_data[0]["landmarks"][pose_data[0]["landmark_map"]["left_shoulder"]][1]
                initial_r_shoulder_y = pose_data[0]["landmarks"][pose_data[0]["landmark_map"]["right_shoulder"]][1]
                initial_l_hip_y = pose_data[0]["landmarks"][pose_data[0]["landmark_map"]["left_hip"]][1]
                initial_r_hip_y = pose_data[0]["landmarks"][pose_data[0]["landmark_map"]["right_hip"]][1]

                # Check for significant difference in y-coordinates between shoulders and hips over time
                # This is a crude way to detect torso rotation for demonstration
                for frame in pose_data[1:]:
                    current_l_shoulder_y = frame["landmarks"][frame["landmark_map"]["left_shoulder"]][1]
                    current_r_shoulder_y = frame["landmarks"][frame["landmark_map"]["right_shoulder"]][1]
                    current_l_hip_y = frame["landmarks"][frame["landmark_map"]["left_hip"]][1]
                    current_r_hip_y = frame["landmarks"][frame["landmark_map"]["right_hip"]][1]

                    shoulder_diff = abs((current_l_shoulder_y - current_r_shoulder_y) - (initial_l_shoulder_y - initial_r_shoulder_y))
                    hip_diff = abs((current_l_hip_y - current_r_hip_y) - (initial_l_hip_y - initial_r_hip_y))

                    # If shoulder rotation is significantly more than hip rotation, suggest torso stability
                    if shoulder_diff > 0.05 and shoulder_diff > hip_diff * 1.5: # Arbitrary thresholds
                        specific_feedback.append("Avoid rotating your torso; keep your core stable.")
                        break

        return specific_feedback

    @staticmethod
    def get_video_requirements() -> List[str]:
        return [
            "Record from a front or slightly angled view to show knee separation.",
            "Ensure your hips and knees are clearly visible."
        ]
