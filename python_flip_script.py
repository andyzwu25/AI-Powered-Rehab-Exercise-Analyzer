import os
from moviepy import VideoFileClip
import moviepy.video.fx as vfx

root_folder = "data/raw/clamshell"

for root, dirs, files in os.walk(root_folder):
    for filename in files:
        # 1. Convert to lowercase for checking extension
        fn_lower = filename.lower()
        
        # 2. Check extension and ensure it hasn't been flipped yet
        if fn_lower.endswith((".mp4", ".mov", ".avi", ".mkv", ".webm")):
            if "_flipped" in fn_lower:
                continue # Skip already flipped files
            
            # Check if the flipped version already exists in the folder
            name, ext = os.path.splitext(filename)
            output_name = f"{name}_flipped{ext}"
            if output_name in files:
                print(f"Skipping: {output_name} already exists.")
                continue

            print(f"Now Flipping: {filename}")
            path = os.path.join(root, filename)
            output_path = os.path.join(root, output_name)
            
            try:
                with VideoFileClip(path) as clip:
                    flipped_clip = clip.with_effects([vfx.MirrorX()])
                    flipped_clip.write_videofile(output_path, codec="libx264", audio=False)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            # This tells you if it found a file it didn't recognize as a video
            if not filename.startswith('.'): # Ignore hidden system files
                print(f"Ignored non-video file: {filename}")

print("\n--- Process Complete ---")