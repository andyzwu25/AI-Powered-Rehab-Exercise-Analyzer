"""
Data collection module for gathering labeled training data.
Stores user feedback and video analysis results for model training.
"""
import os
import json
import pickle
from typing import List, Dict, Optional
from datetime import datetime


class DataCollector:
    """
    Collects and manages labeled training data for ML models.
    """
    
    def __init__(self, data_dir: str = "models/ml/training_data"):
        """
        Initialize data collector.
        
        Args:
            data_dir: Directory to store training data
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def save_training_example(
        self,
        exercise_type: str,
        pose_data: List[Dict],
        score: float,
        user_feedback: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Save a labeled training example.
        
        Args:
            exercise_type: Type of exercise
            pose_data: Pose data from video analysis
            score: Form score (0-100) - can be from user feedback or expert rating
            user_feedback: Optional user-provided feedback text
            metadata: Optional additional metadata (video path, timestamp, etc.)
            
        Returns:
            ID of saved example
        """
        example_id = f"{exercise_type}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        example = {
            'id': example_id,
            'exercise_type': exercise_type,
            'pose_data': pose_data,
            'score': score,
            'user_feedback': user_feedback,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to exercise-specific file
        exercise_file = os.path.join(self.data_dir, f"{exercise_type}_data.jsonl")
        
        with open(exercise_file, 'a') as f:
            f.write(json.dumps(example) + '\n')
        
        return example_id
    
    def load_training_data(self, exercise_type: str) -> List[Dict]:
        """
        Load all training examples for an exercise type.
        
        Args:
            exercise_type: Type of exercise
            
        Returns:
            List of training examples
        """
        exercise_file = os.path.join(self.data_dir, f"{exercise_type}_data.jsonl")
        
        if not os.path.exists(exercise_file):
            return []
        
        examples = []
        with open(exercise_file, 'r') as f:
            for line in f:
                if line.strip():
                    examples.append(json.loads(line))
        
        return examples
    
    def get_training_statistics(self, exercise_type: str) -> Dict:
        """
        Get statistics about collected training data.
        
        Args:
            exercise_type: Type of exercise
            
        Returns:
            Dictionary with statistics
        """
        examples = self.load_training_data(exercise_type)
        
        if not examples:
            return {
                'count': 0,
                'avg_score': 0,
                'min_score': 0,
                'max_score': 0
            }
        
        scores = [ex['score'] for ex in examples]
        
        return {
            'count': len(examples),
            'avg_score': sum(scores) / len(scores),
            'min_score': min(scores),
            'max_score': max(scores),
            'std_score': (sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores))**0.5
        }

