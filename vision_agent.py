"""
Vision Analysis Agent for Lightweight AgenticCyber Framework
Analyzes video frames and images for security threats
"""
import cv2
import os
from pathlib import Path
from typing import Dict, Any, Optional
from google.genai import types
from base_agent import BaseAgent
import config


class VisionAgent(BaseAgent):
    """Agent specialized in analyzing visual content for security threats"""
    
    def __init__(self):
        super().__init__("VisionAgent", config.VISION_MODEL)
        self.temp_frame_path = config.OUTPUT_DIR / "temp_frame.jpg"
    
    def analyze(self, video_path: Optional[Path] = None, frame_time_ms: int = 1000) -> Dict[str, Any]:
        """
        Analyze video frame for security threats
        Args:
            video_path: Path to video file
            frame_time_ms: Time in milliseconds to extract frame
        """
        self.status = "analyzing"
        
        # Try to find video file if not provided
        if video_path is None:
            # First check input folder
            input_videos = list(config.INPUT_VIDEOS_DIR.glob("*.mp4"))
            if input_videos:
                video_path = input_videos[0]
            else:
                # Fallback to root directory
                video_files = list(config.VIDEO_DIR.glob("*.mp4"))
                if video_files:
                    video_path = video_files[0]
                else:
                    return self.format_report(
                        "WARNING",
                        f"No video file found. Please place video files in {config.INPUT_VIDEOS_DIR}",
                        0.0
                    )
        
        if not video_path.exists():
            return self.format_report(
                "WARNING",
                f"Video file not found: {video_path}",
                0.0
            )
        
        try:
            # Extract frame from video
            frame = self._extract_frame(video_path, frame_time_ms)
            
            if frame is None:
                return self.format_report(
                    "WARNING",
                    f"Could not extract frame from video at {frame_time_ms}ms",
                    0.0
                )
            
            # Save frame temporarily
            cv2.imwrite(str(self.temp_frame_path), frame)
            
            # Analyze with LLM
            with open(self.temp_frame_path, "rb") as f:
                image_bytes = f.read()
            
            prompt = """Analyze this security camera frame for threats. Look for:
- Unauthorized persons or suspicious behavior
- Weapons or dangerous objects
- Unusual activity or loitering
- Security breaches or tampering

Provide analysis in this format:
THREAT_LEVEL: [CRITICAL/WARNING/SECURE]
DETAILS: [Description of detected threats or objects]
OBJECTS: [List of detected objects]"""
            
            contents = [
                types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                prompt
            ]
            
            result = self._call_llm("", contents=contents)
            
            # Clean up temp file
            if self.temp_frame_path.exists():
                os.remove(self.temp_frame_path)
            
            # Parse result
            threat_level, details = self._parse_result(result)
            
            self.status = "completed"
            return self.format_report(threat_level, details, 0.75)
            
        except Exception as e:
            self.status = "error"
            # Clean up temp file on error
            if self.temp_frame_path.exists():
                os.remove(self.temp_frame_path)
            return self.format_report(
                "WARNING",
                f"Error analyzing video: {str(e)}",
                0.0
            )
    
    def _extract_frame(self, video_path: Path, time_ms: int) -> Optional[Any]:
        """Extract a frame from video at specified time"""
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        
        cap.set(cv2.CAP_PROP_POS_MSEC, time_ms)
        success, frame = cap.read()
        cap.release()
        
        return frame if success else None
    
    def _parse_result(self, result: str) -> tuple:
        """Parse LLM result to extract threat level and details"""
        threat_level = "SECURE"
        details = result
        
        if "CRITICAL" in result.upper():
            threat_level = "CRITICAL"
        elif "WARNING" in result.upper() or "THREAT" in result.upper():
            threat_level = "WARNING"
        
        # Extract details section if present
        if "DETAILS:" in result:
            details = result.split("DETAILS:")[-1].strip()
        elif "THREAT_LEVEL:" in result:
            details = result.split("THREAT_LEVEL:")[-1].strip()
        
        return threat_level, details
    
    def get_vision_report(self) -> str:
        """Legacy method for compatibility"""
        result = self.analyze()
        return f"{result['threat_level']}: {result['details']}"