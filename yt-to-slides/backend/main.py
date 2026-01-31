from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
from video_processor import extract_slides

app = FastAPI()

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage for results
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# In-memory status tracking (could be replaced with Redis/DB for production)
jobs = {}

@app.on_event("startup")
async def startup_event():
    # Check for cookies in environment variable (Secure method for Render/Railway)
    env_cookies = os.getenv("YOUTUBE_COOKIES")
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    
    if env_cookies:
        # Write the env var content to the file
        try:
            with open(cookies_path, 'w') as f:
                f.write(env_cookies)
            print(f"✅ SUCCESS: cookies.txt created from environment variable.")
        except Exception as e:
            print(f"❌ ERROR: Failed to write cookies from env var: {e}")

    # Verify file exists
    if os.path.exists(cookies_path):
        print(f"✅ SUCCESS: cookies.txt found at {cookies_path}")
    else:
        print(f"❌ WARNING: cookies.txt NOT found. You may encounter 'Sign in' errors.")

@app.post("/process")
async def process_video(youtube_url: str, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "processing", "url": youtube_url}
    
    background_tasks.add_task(run_extraction, job_id, youtube_url)
    
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

@app.get("/download/{job_id}")
async def download_result(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if jobs[job_id]["status"] != "completed":
        raise HTTPException(status_code=400, detail="Job not completed yet")
    
    file_path = jobs[job_id]["file_path"]
    return FileResponse(file_path, media_type='application/pdf', filename=f"slides_{job_id}.pdf")

def run_extraction(job_id: str, youtube_url: str):
    try:
        output_path = os.path.join(OUTPUT_DIR, f"{job_id}.pdf")
        temp_dir = os.path.join("temp", job_id)
        
        result = extract_slides(youtube_url, output_path, temp_dir=temp_dir)
        
        if result:
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["file_path"] = output_path
        else:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = "No slides detected"
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
