import os
from typing import Set

def allowed_file(filename: str, allowed_extensions: Set[str]) -> bool:
    """Check if a file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def create_upload_folder(folder_path: str) -> None:
    """Create upload folder if it doesn't exist"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes"""
    if not os.path.exists(file_path):
        return 0.0
    
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024)

def is_valid_video_file(filename: str) -> bool:
    """Check if file is a valid video format"""
    video_extensions = {'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'}
    return allowed_file(filename, video_extensions)

def is_valid_image_file(filename: str) -> bool:
    """Check if file is a valid image format"""
    image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
    return allowed_file(filename, image_extensions)

def get_file_type(filename: str) -> str:
    """Get the type of file (video, image, or unknown)"""
    if is_valid_video_file(filename):
        return 'video'
    elif is_valid_image_file(filename):
        return 'image'
    else:
        return 'unknown' 