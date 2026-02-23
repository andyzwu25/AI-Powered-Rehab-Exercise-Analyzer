"""
Model training module for exercise form analysis.
Trains machine learning models on labeled exercise videos.
"""
import os
import pickle
import numpy as np
from typing import List, Dict, Optional, Tuple
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib

from .feature_extractor import FeatureExtractor


class ModelTrainer:
    """
    Trains and manages ML models for exercise form analysis.
    """
    
    def __init__(self, models_dir: str = "models/ml/saved_models"):
        """
        Initialize model trainer.
        
        Args:
            models_dir: Directory to save/load trained models
        """
        self.models_dir = models_dir
        self.feature_extractor = FeatureExtractor()
        self.scalers = {}  # One scaler per exercise type
        os.makedirs(models_dir, exist_ok=True)
    
    def train_model(
        self,
        exercise_type: str,
        training_data: List[Dict],
        labels: List[float],
        model_type: str = "random_forest",
        test_size: float = 0.2
    ) -> Dict:
        """
        Train a model for a specific exercise type.
        
        Args:
            exercise_type: Type of exercise (e.g., 'pull_up', 'push_up')
            training_data: List of pose data dictionaries from videos
            labels: List of form scores (0-100) for each video
            model_type: Type of model ('random_forest' or 'gradient_boosting')
            test_size: Proportion of data to use for testing
            
        Returns:
            Dictionary with training results and metrics
        """
        if len(training_data) != len(labels):
            raise ValueError("Training data and labels must have the same length")
        
        if len(training_data) < 10:
            raise ValueError(f"Need at least 10 training examples, got {len(training_data)}")
        
        # Extract features from training data
        print(f"Extracting features from {len(training_data)} examples...")
        X = []
        for pose_data in training_data:
            features = self.feature_extractor.extract_features(pose_data)
            X.append(features)
        
        X = np.array(X)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers[exercise_type] = scaler
        
        # Train model
        print(f"Training {model_type} model for {exercise_type}...")
        
        if model_type == "random_forest":
            model = RandomForestRegressor(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
        elif model_type == "gradient_boosting":
            model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=10,
                learning_rate=0.1,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        y_train_pred = model.predict(X_train_scaled)
        y_test_pred = model.predict(X_test_scaled)
        
        train_mse = mean_squared_error(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
        # Save model and scaler
        self._save_model(exercise_type, model, scaler)
        
        results = {
            'success': True,
            'exercise_type': exercise_type,
            'model_type': model_type,
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'train_mse': float(train_mse),
            'test_mse': float(test_mse),
            'train_r2': float(train_r2),
            'test_r2': float(test_r2),
            'train_rmse': float(np.sqrt(train_mse)),
            'test_rmse': float(np.sqrt(test_mse))
        }
        
        print(f"Training complete! Test R²: {test_r2:.3f}, Test RMSE: {np.sqrt(test_mse):.2f}")
        
        return results
    
    def load_model(self, exercise_type: str) -> Optional[Tuple]:
        """
        Load a trained model for an exercise type.
        
        Args:
            exercise_type: Type of exercise
            
        Returns:
            Tuple of (model, scaler) or None if not found
        """
        model_path = os.path.join(self.models_dir, f"{exercise_type}_model.pkl")
        scaler_path = os.path.join(self.models_dir, f"{exercise_type}_scaler.pkl")
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            return None
        
        try:
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return (model, scaler)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def predict(self, exercise_type: str, pose_data: List[Dict]) -> float:
        """
        Predict form score for given pose data.
        
        Args:
            exercise_type: Type of exercise
            pose_data: List of frame pose data dictionaries
            
        Returns:
            Predicted form score (0-100)
        """
        model_data = self.load_model(exercise_type)
        if model_data is None:
            # Fallback to rule-based if no model available
            return 50.0  # Default score
        
        model, scaler = model_data
        
        # Extract features
        features = self.feature_extractor.extract_features(pose_data)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Predict
        score = model.predict(features_scaled)[0]
        
        # Clamp to 0-100 range
        score = max(0, min(100, score))
        
        return float(score)
    
    def _save_model(self, exercise_type: str, model, scaler):
        """Save trained model and scaler to disk"""
        model_path = os.path.join(self.models_dir, f"{exercise_type}_model.pkl")
        scaler_path = os.path.join(self.models_dir, f"{exercise_type}_scaler.pkl")
        
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        print(f"Model saved to {model_path}")
    
    def model_exists(self, exercise_type: str) -> bool:
        """Check if a trained model exists for an exercise type"""
        model_path = os.path.join(self.models_dir, f"{exercise_type}_model.pkl")
        return os.path.exists(model_path)

