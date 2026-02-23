"""
Base analyzer class that provides ML model integration.
All exercise analyzers should inherit from this.
"""
from typing import List, Dict, Optional
from ..ml.model_trainer import ModelTrainer


class BaseAnalyzer:
    """
    Base class for exercise analyzers with ML model support.
    """
    
    def __init__(self):
        """Initialize base analyzer with ML trainer"""
        self.model_trainer = ModelTrainer()
        self.use_ml = True  # Flag to enable/disable ML
    
    @staticmethod
    def get_video_requirements() -> List[str]:
        """
        Returns a list of video requirements for analysis.
        Should be overridden by subclasses.
        """
        return [
            "Ensure your entire body is visible.",
            "Use a stable camera with good lighting."
        ]
    
    def analyze_form(self, pose_data: List[Dict], exercise_type: str) -> Dict:
        """
        Analyze form using ML model if available, otherwise use rule-based.
        
        Args:
            pose_data: List of frame pose data dictionaries
            exercise_type: Type of exercise (e.g., 'pull_up')
            
        Returns:
            Dictionary with score and feedback
        """
        # Try ML model first
        if self.use_ml and self.model_trainer.model_exists(exercise_type):
            try:
                score = self.model_trainer.predict(exercise_type, pose_data)
                feedback = self._generate_feedback_from_score(score, pose_data)
                return {
                    'score': score,
                    'feedback': feedback,
                    'method': 'ml_model'
                }
            except Exception as e:
                print(f"ML prediction failed: {e}, falling back to rule-based")
        
        # Fallback to rule-based analysis
        return self._rule_based_analysis(pose_data)
    
    def _generate_feedback_from_score(self, score: float, pose_data: List[Dict]) -> List[str]:
        """
        Generate feedback based on ML score and pose data.
        Can be enhanced with more sophisticated feedback generation.
        """
        feedback = []
        
        if score >= 90:
            feedback.append("Excellent form! Your technique is very good.")
        elif score >= 75:
            feedback.append("Good form overall, with minor areas for improvement.")
        elif score >= 60:
            feedback.append("Decent form, but there are several areas to work on.")
        else:
            feedback.append("Form needs significant improvement. Focus on the fundamentals.")
        
        # Add specific feedback based on pose data analysis
        specific_feedback = self._analyze_specific_issues(pose_data)
        feedback.extend(specific_feedback)
        
        return feedback
    
    def _analyze_specific_issues(self, pose_data: List[Dict]) -> List[str]:
        """
        Analyze specific form issues from pose data.
        Should be overridden by subclasses for exercise-specific feedback.
        """
        return []
    
    def _rule_based_analysis(self, pose_data: List[Dict]) -> Dict:
        """
        Rule-based analysis as fallback.
        Should be overridden by subclasses.
        """
        return {
            'score': 50,
            'feedback': ['Using rule-based analysis. Train a model for better accuracy.'],
            'method': 'rule_based'
        }

