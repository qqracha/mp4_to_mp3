import os
from pathlib import Path
from moviepy import VideoFileClip

# get the directory where the script is located
script_dir = Path(__file__).parent

# define paths for videos and sounds folders
videos_folder = script_dir / "videos"
sounds_folder = script_dir / "sounds"

# create sounds & videos folder if it doesn't exist
sounds_folder.mkdir(exist_ok=True)
videos_folder.mkdir(exist_ok=True)

# get all mp4 files from videos folder
mp4_files = list(videos_folder.glob("*.mp4"))

if not mp4_files:
    print("// no mp4 files found in videos folder...\n// maybe next time ( ͡° ͜ʖ ͡°)")
else:
    print(f"// found {len(mp4_files)} mp4 file(s) to convert")
    
    # convert each mp4 file to mp3
    for mp4_file in mp4_files:
        try:
            print(f"// converting, pls wait >_<: {mp4_file.name}")
            
            # load video file
            video = VideoFileClip(str(mp4_file))
            
            # create output path with same name but .mp3 extension
            output_path = sounds_folder / f"{mp4_file.stem}.mp3"
            
            # extract audio and save as mp3
            video.audio.write_audiofile(str(output_path), logger=None)
            
            # close the video file
            video.close()
            
            print(f"// ✓ converted: {output_path.name}")
            
        except Exception as e:
            print(f"// ✗ error converting {mp4_file.name}: {str(e)}")
    
    print("\n// conversion completed! enjoy! ƪ(˘⌣˘)ʃ")
