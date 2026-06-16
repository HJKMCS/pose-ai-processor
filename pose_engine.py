"""
Pose Detection Engine using MediaPipe.
CPU-optimized, isolated in one file.
Takes frame → returns pose landmarks.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Dict, Any, List
from logger import logger
import constants as C

class PoseEngine:
    """
    MediaPipe Pose detection engine.
    Runs on CPU, optimized for speed.
    """
    
    def __init__(self):
        """Initialize MediaPipe Pose with CPU-optimized settings."""
        try:
            self.mp_pose = mp.solutions.pose
            self.mp_drawing = mp.solutions.drawing_utils
            self.mp_drawing_styles = mp.solutions.drawing_styles
            
            # Initialize Pose with CPU-friendly settings
            self.pose = self.mp_pose.Pose(
                static_image_mode=False,  # Video mode (faster)
                model_complexity=1,  # 0=fast, 1=balanced, 2=accurate (but slower)
                min_detection_confidence=C.POSE_DETECTION_CONFIDENCE,
                min_tracking_confidence=C.POSE_TRACKING_SMOOTHING,
                enable_segmentation=False,  # Disable for speed
                smooth_segmentation=False
            )
            
            logger.info("PoseEngine initialized (CPU mode)")
            self.is_initialized = True
            
        except Exception as e:
            logger.error(f"Failed to initialize PoseEngine: {e}")
            self.is_initialized = False
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single frame and extract pose data.
        
        Args:
            frame: Input video frame (BGR format from OpenCV)
            
        Returns:
            Dictionary containing:
            - landmarks: Pose landmarks if detected
            - has_pose: Boolean indicating if pose was detected
            - frame_with_pose: Frame with skeleton drawn
        """
        if not self.is_initialized:
            logger.error("PoseEngine not initialized")
            return {"has_pose": False, "landmarks": None, "frame_with_pose": frame}
        
        try:
            # Convert BGR to RGB (MediaPipe expects RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame
            results = self.pose.process(rgb_frame)
            
            # Prepare output
            output = {
                "has_pose": False,
                "landmarks": None,
                "normalized_landmarks": None,
                "frame_with_pose": frame.copy()
            }
            
            if results.pose_landmarks:
                output["has_pose"] = True
                output["landmarks"] = self._extract_landmarks(results.pose_landmarks)
                output["normalized_landmarks"] = self._extract_normalized_landmarks(results.pose_landmarks)
                
                # Draw pose landmarks on frame
                self.mp_drawing.draw_landmarks(
                    output["frame_with_pose"],
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                )
            
            return output
            
        except Exception as e:
            logger.error(f"Error processing frame: {e}")
            return {"has_pose": False, "landmarks": None, "frame_with_pose": frame}
    
    def _extract_landmarks(self, pose_landmarks) -> List[Dict[str, float]]:
        """Extract 3D landmarks (x, y, z, visibility)."""
        landmarks = []
        for landmark in pose_landmarks.landmark:
            landmarks.append({
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z,
                "visibility": landmark.visibility
            })
        return landmarks
    
    def _extract_normalized_landmarks(self, pose_landmarks) -> List[Dict[str, float]]:
        """Extract normalized landmarks (0-1 range)."""
        landmarks = []
        for landmark in pose_landmarks.landmark:
            landmarks.append({
                "x": landmark.x,
                "y": landmark.y,
                "z": landmark.z
            })
        return landmarks
    
    def get_pose_summary(self, landmarks: List[Dict]) -> Dict[str, Any]:
        """
        Calculate basic pose metrics from landmarks.
        Useful for quick analysis without AI.
        """
        if not landmarks or len(landmarks) < 33:
            return {}
        
        # Key landmark indices (MediaPipe Pose)
        NOSE = 0
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_HIP = 23
        RIGHT_HIP = 24
        
        summary = {
            "shoulder_angle": self._calculate_angle(
                landmarks[LEFT_SHOULDER], landmarks[RIGHT_SHOULDER]
            ),
            "hip_angle": self._calculate_angle(
                landmarks[LEFT_HIP], landmarks[RIGHT_HIP]
            ),
            "head_position": {
                "x": landmarks[NOSE]["x"],
                "y": landmarks[NOSE]["y"]
            },
            "total_landmarks": len(landmarks)
        }
        
        return summary
    
    def _calculate_angle(self, landmark1: Dict, landmark2: Dict) -> float:
        """Calculate angle between two points (simplified)."""
        dx = landmark2["x"] - landmark1["x"]
        dy = landmark2["y"] - landmark1["y"]
        return np.degrees(np.arctan2(dy, dx))
    
    def close(self):
        """Clean up resources."""
        if self.is_initialized:
            self.pose.close()
            logger.info("PoseEngine closed")