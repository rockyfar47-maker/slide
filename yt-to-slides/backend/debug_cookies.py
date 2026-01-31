
import yt_dlp
import os

def test_cookies():
    # URL that usually requires sign-in or is age-gated (good test)
    # Or just a standard video to test basic access
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    
    print(f"Checking for cookies at: {cookies_path}")
    if os.path.exists(cookies_path):
        with open(cookies_path, 'r') as f:
            content = f.read()
            print(f"Cookies file found. Size: {len(content)} bytes")
            print(f"First 100 chars: {content[:100]}")
    else:
        print("❌ No cookies.txt found!")

    ydl_opts = {
        'quiet': False,
        'no_warnings': False,
    }

    if os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path
    
    print("\nAttempting to extract video info...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(test_url, download=False)
            print(f"✅ SUCCESS! Video title: {info.get('title')}")
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")

if __name__ == "__main__":
    test_cookies()
