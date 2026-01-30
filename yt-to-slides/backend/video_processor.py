import cv2
import yt_dlp
import img2pdf
import os
import shutil
import numpy as np
from PIL import Image

def get_stream_url(youtube_url):
    # Path to optional cookies file for cloud deployment
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    
    ydl_opts = {
        'format': 'best[height<=720]',
        'quiet': True,
        'no_warnings': True,
        # Aggressive spoofing
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'referer': 'https://www.youtube.com/',
        'nocheckcertificate': True,
        # Multi-client spoofing: iOS and Android are much less likely to trigger bot checks
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'web'],
                'skip': ['webpage', 'configs']
            }
        },
    }
    
    # If the user has provided a cookies.txt file, use it. 
    # This is the "Nuclear Option" that always works.
    if os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path
        print("Using cookies.txt for authentication")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

def extract_slides(youtube_url, output_pdf_path, temp_dir='temp_slides', threshold=0.98, skip_seconds=2):
    """
    Extracts unique slides from a YouTube video and saves them as a PDF.
    
    Args:
        youtube_url (str): The YouTube video URL.
        output_pdf_path (str): Path to save the generated PDF.
        temp_dir (str): Temporary directory to store frame images.
        threshold (float): Similarity threshold (0-1). Lower means more slides.
        skip_seconds (int): Number of seconds to skip between frame checks.
    """
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        stream_url = get_stream_url(youtube_url)
        cap = cv2.VideoCapture(stream_url)
        
        if not cap.isOpened():
            raise Exception("Could not open video stream. The URL might be restricted or invalid.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0: fps = 30 # Fallback
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        skip_frames = max(1, int(fps * skip_seconds))

        prev_frame = None
        slide_count = 0
        saved_images = []

        frame_idx = 0
        while True:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            if not ret:
                break

            # Processing for comparison (grayscale and resize for speed/robustness)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_small = cv2.resize(gray, (640, 360))

            is_new_slide = False
            if prev_frame is not None:
                # Template matching for similarity
                res = cv2.matchTemplate(gray_small, prev_frame, cv2.TM_CCOEFF_NORMED)
                score = res[0][0]
                
                # If similarity is below threshold, it's likely a new slide
                if score < threshold:
                    is_new_slide = True
            else:
                # First frame is always a slide
                is_new_slide = True

            if is_new_slide:
                slide_count += 1
                img_path = os.path.join(temp_dir, f"slide_{slide_count:03d}.jpg")
                cv2.imwrite(img_path, frame)
                saved_images.append(img_path)
                prev_frame = gray_small
                print(f"Detected slide {slide_count} at {frame_idx/fps:.2f}s")

            frame_idx += skip_frames
            if total_frames > 0 and frame_idx >= total_frames:
                break

        cap.release()

        if saved_images:
            print(f"Generating PDF with {len(saved_images)} slides...")
            # Ensure images are in order
            saved_images.sort()
            with open(output_pdf_path, "wb") as f:
                f.write(img2pdf.convert(saved_images))
            return output_pdf_path
        else:
            return None
            
    finally:
        # Cleanup temp directory if desired, or keep for debugging
        # shutil.rmtree(temp_dir)
        pass

if __name__ == "__main__":
    # Test path
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Demo
    # extract_slides(test_url, "test_output.pdf")
