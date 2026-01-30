# YouTube Slide Extractor

A premium web application for extracting slides from YouTube lectures and converting them into PDFs.

## Prerequisites
- Python 3.8+
- Active internet connection (to download video streams)

## How to Run

### 1. Start the Backend
Open a terminal in the `backend` directory and run:
```bash
python main.py
```
This will start the FastAPI server at `http://localhost:8000`.

### 2. Open the Frontend
Simply open the `frontend/index.html` file in any modern web browser.

## Features
- **Automatic Slide Detection**: Uses CV2 template matching to detect significant frame changes.
- **Background Processing**: Handles large videos asynchronously.
- **Premium UI**: Modern glassmorphism design with real-time status updates.
- **PDF Generation**: High-quality PDF creation using `img2pdf`.

## Project Structure
- `backend/main.py`: FastAPI server and API endpoints.
- `backend/video_processor.py`: Core logic for slide extraction.
- `frontend/index.html`: Premium standalone frontend.
- `output/`: Directory where generated PDFs are stored.
