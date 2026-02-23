"""
Feature extraction module for converting MediaPipe pose data into ML-ready features.
"""
import numpy as np
from typing import List, Dict, Optional
from collections import deque


class FeatureExtractor:
    """
    Extracts features from pose data for machine learning models.
    Converts raw MediaPipe landmarks and angles into meaningful features.
    """
    
    def __init__(self, window_size: int = 10):
        """
        Initialize feature extractor.
        
        Args:
            window_size: Number of frames to use for temporal features
        """
        self.window_size = window_size
    
    def extract_features(self, pose_data: List[Dict]) -> np.ndarray:
        """
        Extract features from a sequence of pose data frames.
        
        Args:
            pose_data: List of frame dictionaries with 'landmarks' and 'angles'
            
        Returns:
            Feature vector as numpy array
        """
        if not pose_data:
            return np.zeros(self._get_feature_count())
        
        features = []
        
        # Extract frame-level features
        frame_features = self._extract_frame_features(pose_data)
        features.extend(frame_features)
        
        # Extract temporal features (movement patterns)
        temporal_features = self._extract_temporal_features(pose_data)
        features.extend(temporal_features)
        
        # Extract statistical features
        statistical_features = self._extract_statistical_features(pose_data)
        features.extend(statistical_features)
        
        return np.array(features)
    
    def _extract_frame_features(self, pose_data: List[Dict]) -> List[float]:
        """Extract features from individual frames"""
        features = []
        
        # Get key angles from all frames
        all_angles = {
            'elbow': [],
            'shoulder': [],
            'hip': [],
            'knee': []
        }
        
        for frame in pose_data:
            angles = frame.get('angles', {})
            
            # Average left and right angles
            left_elbow = angles.get('left_elbow', 180)
            right_elbow = angles.get('right_elbow', 180)
            all_angles['elbow'].append((left_elbow + right_elbow) / 2)
            
            left_shoulder = angles.get('left_shoulder', 180)
            right_shoulder = angles.get('right_shoulder', 180)
            all_angles['shoulder'].append((left_shoulder + right_shoulder) / 2)
            
            left_hip = angles.get('left_hip', 180)
            right_hip = angles.get('right_hip', 180)
            all_angles['hip'].append((left_hip + right_hip) / 2)
            
            left_knee = angles.get('left_knee', 180)
            right_knee = angles.get('right_knee', 180)
            all_angles['knee'].append((left_knee + right_knee) / 2)
        
        # Key angle statistics
        for angle_type in ['elbow', 'shoulder', 'hip', 'knee']:
            if all_angles[angle_type]:
                angles_array = np.array(all_angles[angle_type])
                features.extend([
                    np.min(angles_array),  # Minimum angle (deepest position)
                    np.max(angles_array),  # Maximum angle (top position)
                    np.mean(angles_array),  # Average angle
                    np.std(angles_array),   # Variability
                    np.max(angles_array) - np.min(angles_array)  # Range of motion
                ])
            else:
                features.extend([0, 0, 0, 0, 0])
        
        return features
    
    def _extract_temporal_features(self, pose_data: List[Dict]) -> List[float]:
        """Extract temporal/movement pattern features"""
        features = []
        
        if len(pose_data) < 2:
            return [0] * 20  # Return zeros if not enough frames
        
        # Calculate velocities (change in position over time)
        landmark_map = pose_data[0].get('landmark_map', {})
        
        key_landmarks = ['left_wrist', 'left_elbow', 'left_shoulder', 
                        'left_hip', 'left_knee', 'left_ankle']
        
        velocities = {landmark: [] for landmark in key_landmarks}
        
        for i in range(1, len(pose_data)):
            prev_frame = pose_data[i-1]
            curr_frame = pose_data[i]
            
            prev_landmarks = prev_frame.get('landmarks', [])
            curr_landmarks = curr_frame.get('landmarks', [])
            
            for landmark_name in key_landmarks:
                if landmark_name in landmark_map:
                    idx = landmark_map[landmark_name]
                    if idx < len(prev_landmarks) and idx < len(curr_landmarks):
                        prev_pos = np.array(prev_landmarks[idx][:2])  # x, y
                        curr_pos = np.array(curr_landmarks[idx][:2])
                        velocity = np.linalg.norm(curr_pos - prev_pos)
                        velocities[landmark_name].append(velocity)
        
        # Statistical features of velocities
        for landmark_name in key_landmarks:
            if velocities[landmark_name]:
                vel_array = np.array(velocities[landmark_name])
                features.extend([
                    np.mean(vel_array),  # Average velocity
                    np.std(vel_array),   # Velocity variability
                    np.max(vel_array)    # Peak velocity
                ])
            else:
                features.extend([0, 0, 0])
        
        # Smoothness (low variance in velocity = smooth movement)
        all_velocities = []
        for vels in velocities.values():
            all_velocities.extend(vels)
        
        if all_velocities:
            features.append(np.std(all_velocities))  # Overall movement smoothness
        else:
            features.append(0)
        
        return features
    
    def _extract_statistical_features(self, pose_data: List[Dict]) -> List[float]:
        """Extract statistical features across the entire sequence"""
        features = []
        
        if not pose_data:
            return [0] * 10
        
        # Body alignment features
        landmark_map = pose_data[0].get('landmark_map', {})
        
        # Calculate body line straightness (shoulder-hip-ankle alignment)
        alignment_scores = []
        
        for frame in pose_data:
            landmarks = frame.get('landmarks', [])
            if len(landmarks) < 28:
                continue
            
            # Get key points for alignment
            shoulder_idx = landmark_map.get('left_shoulder', 11)
            hip_idx = landmark_map.get('left_hip', 23)
            ankle_idx = landmark_map.get('left_ankle', 27)
            
            if (shoulder_idx < len(landmarks) and 
                hip_idx < len(landmarks) and 
                ankle_idx < len(landmarks)):
                
                shoulder = np.array(landmarks[shoulder_idx][:2])
                hip = np.array(landmarks[hip_idx][:2])
                ankle = np.array(landmarks[ankle_idx][:2])
                
                # Calculate how straight the body line is
                vec1 = hip - shoulder
                vec2 = ankle - hip
                
                # Angle between vectors (should be close to 180 for straight line)
                cos_angle = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-6)
                cos_angle = np.clip(cos_angle, -1, 1)
                angle = np.arccos(cos_angle) * 180 / np.pi
                
                # Score: closer to 180 degrees = better alignment
                alignment_score = 1 - abs(angle - 180) / 180
                alignment_scores.append(alignment_score)
        
        if alignment_scores:
            features.extend([
                np.mean(alignment_scores),  # Average body alignment
                np.min(alignment_scores),  # Worst alignment
                np.std(alignment_scores)    # Alignment consistency
            ])
        else:
            features.extend([0, 0, 0])
        
        # Exercise completion features
        # Detect if full range of motion was achieved
        angles = []
        for frame in pose_data:
            frame_angles = frame.get('angles', {})
            # Combine all angles to detect movement
            all_frame_angles = list(frame_angles.values())
            if all_frame_angles:
                angles.extend(all_frame_angles)
        
        if angles:
            angle_array = np.array(angles)
            features.extend([
                np.max(angle_array) - np.min(angle_array),  # Total range
                len(pose_data),  # Number of frames
                np.mean([len(frame.get('angles', {})) for frame in pose_data])  # Average detected joints
            ])
        else:
            features.extend([0, 0, 0])
        
        # Symmetry features (left vs right side)
        symmetry_scores = []
        for frame in pose_data:
            angles = frame.get('angles', {})
            left_elbow = angles.get('left_elbow', 180)
            right_elbow = angles.get('right_elbow', 180)
            left_shoulder = angles.get('left_shoulder', 180)
            right_shoulder = angles.get('right_shoulder', 180)
            
            elbow_symmetry = 1 - abs(left_elbow - right_elbow) / 180
            shoulder_symmetry = 1 - abs(left_shoulder - right_shoulder) / 180
            
            symmetry_scores.append((elbow_symmetry + shoulder_symmetry) / 2)
        
        if symmetry_scores:
            features.append(np.mean(symmetry_scores))
        else:
            features.append(0)
        
        return features
    
    def _get_feature_count(self) -> int:
        """Get the total number of features this extractor produces"""
        # Frame features: 4 angle types * 5 stats = 20
        # Temporal features: 6 landmarks * 3 stats + 1 smoothness = 19
        # Statistical features: ~10
        return 49  # Approximate, adjust based on actual extraction

