"""
Video Processor with threading.
Handles:
- Video reading/writing
- Frame-by-frame processing
- Progress tracking
- Background threading (non-blocking UI)
"""

import cv2
import threading
import time
from pathlib import Path
from typing import Callable, Optional, Dict, Any
from logger import logger
import constants as C
from pose_engine import PoseEngine
from json_handler import JSONHandler

class VideoProcessor:
    """
    Video processing with background threading.
    Keeps UI responsive during heavy processing.
    """
    
    def __init__(self):
        self.pose_engine = PoseEngine()
        self.json_handler = JSONHandler()
        self.is_processing = False
        self.should_stop = False
        self.progress = 0.0
        self.current_frame = 0
        self.total_frames = 0
        
        logger.info("VideoProcessor initialized")
    
    def process_video(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable[[float, str], None]] = None,
        completion_callback: Optional[Callable[[Dict[str, Any]], None]] = None
    ) -> bool:
        """
        Start video processing in background thread.
        
        Args:
            input_path: Path to input video
            output_path: Path to save processed video
            progress_callback: Function called with (progress_percent, status_message)
            completion_callback: Function called when done with result dict
            
        Returns:
            True if thread started successfully
        """
        if self.is_processing:
            logger.warning("Already processing a video")
            return False
        
        self.is_processing = True
        self.should_stop = False
        self.progress = 0.0
        
        # Start processing in background thread
        thread = threading.Thread(
            target=self._process_video_thread,
            args=(input_path, output_path, progress_callback, completion_callback),
            daemon=True
        )
        thread.start()
        
        logger.info(f"Started processing: {input_path} → {output_path}")
        return True
    
    def _process_video_thread(
        self,
        input_path: str,
        output_path: str,
        progress_callback: Optional[Callable],
        completion_callback: Optional[Callable]
    ):
        """Background thread for video processing."""
        result = {
            "success": False,
            "input_file": input_path,
            "output_file": output_path,
            "frames_processed": 0,
            "total_frames": 0,
            "pose_frames": 0,
            "error": None,
            "json_file": None,
            "processing_time": 0
        }
        
        start_time = time.time()
        
        try:
            # Open input video
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                raise Exception(f"Failed to open video: {input_path}")
            
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS) or C.DEFAULT_FPS
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Video: {frame_width}x{frame_height} @ {fps}fps, {self.total_frames} frames")
            
            # Create output video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            
            # Data collection for JSON
            frame_data_list = []
            pose_frames_count = 0
            
            # Process frame by frame
            frame_idx = 0
            while True:
                if self.should_stop:
                    logger.info("Processing stopped by user")
                    break
                
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process frame through pose engine
                pose_result = self.pose_engine.process_frame(frame)
                
                # Write processed frame
                out.write(pose_result["frame_with_pose"])
                
                # Collect data for JSON
                frame_info = {
                    "frame_number": frame_idx,
                    "timestamp": frame_idx / fps,
                    "has_pose": pose_result["has_pose"]
                }
                
                if pose_result["has_pose"]:
                    pose_frames_count += 1
                    frame_info["landmarks"] = pose_result["landmarks"]
                    frame_info["summary"] = self.pose_engine.get_pose_summary(pose_result["landmarks"])
                
                frame_data_list.append(frame_info)
                
                # Update progress
                self.current_frame = frame_idx
                self.progress = (frame_idx / self.total_frames) * 100
                
                if progress_callback:
                    status = f"Processing frame {frame_idx}/{self.total_frames}"
                    progress_callback(self.progress, status)
                
                frame_idx += 1
                
                # Small delay to prevent UI freezing (even in thread)
                if frame_idx % 10 == 0:
                    time.sleep(0.001)
            
            # Release resources
            cap.release()
            out.release()
            
            # Generate JSON output
            json_filename = self.json_handler.save_pose_data(
                frame_data_list,
                input_path,
                output_path,
                {
                    "total_frames": self.total_frames,
                    "pose_frames": pose_frames_count,
                    "fps": fps,
                    "resolution": f"{frame_width}x{frame_height}"
                }
            )
            
            result["success"] = True
            result["frames_processed"] = frame_idx
            result["total_frames"] = self.total_frames
            result["pose_frames"] = pose_frames_count
            result["json_file"] = json_filename
            
            logger.info(f"Processing complete: {frame_idx} frames, {pose_frames_count} with pose")
            
        except Exception as e:
            logger.error(f"Video processing error: {e}")
            result["error"] = str(e)
        
        finally:
            result["processing_time"] = time.time() - start_time
            self.is_processing = False
            
            # Call completion callback
            if completion_callback:
                completion_callback(result)
    
    def stop_processing(self):
        """Signal processing to stop."""
        logger.info("Stop signal sent")
        self.should_stop = True
    
    def get_progress(self) -> float:
        """Get current progress (0-100)."""
        return self.progress
    
    def get_status(self) -> Dict[str, Any]:
        """Get current processing status."""
        return {
            "is_processing": self.is_processing,
            "progress": self.progress,
            "current_frame": self.current_frame,
            "total_frames": self.total_frames
        }