# YouTube Automation Project

This project automates the process of creating, uploading, and managing YouTube videos using Python. It includes steps to generate content (e.g., scripts, titles, keywords), create videos, and upload them to YouTube using the YouTube Data API.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Dependencies](#dependencies)
- [License](#license)

## Features

- Generate random categories for YouTube videos using GPT-based AI prompts.
- Generate video scripts, titles, keywords, and appropriate YouTube categories.
- Create video files using MoviePy, merging images and audio.
- Automatically add subtitles to videos based on the script.
- Upload the created video to YouTube with generated metadata (title, description, keywords, and category).
- Clean up by removing videos after successful upload.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/youtube_automatization.git
   cd youtube_automatization
   ```

2. **Create a virtual environment (recommended)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # For Windows, use: venv\Scripts\activate
    ```

3. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Install FFmpeg (for working with audio and video)**:
    ```bash
    sudo apt-get install ffmpeg
    ```

## Configuration

1. Set up Google Cloud API credentials to access the YouTube Data API:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/welcome). 
    - Create a new project and enable the YouTube Data API.
    - Download the client_secrets.json file.
    - Place the file in the project directory.

2. Environment Variables:
    - Create a .env file in the project root with the following environment variables:
    - ```bash
    GOOGLE_APPLICATION_CREDENTIALS=path_to_your_client_secrets.json
    OPENAI_API_KEY=your_openai_api_key
    ```
3. AWS Configuration (if deploying to EC2):
    - Ensure you have the correct EC2 key pair file (e.g., yt_automatization.pem).
    - Update the destination path in the SCP commands in the deployment scripts.

## Usage
- Upload the video to YouTube: 
```bash
python upload_video.py
```

## Directory Structure

youtube_automatization/
│
├── scripts/
│   ├── generate_video.py   # Script for generating video content (title, keywords, etc.)
│   └── upload_video.py             # Script for uploading videos to YouTube
│
├── assets/                         # Directory for images and audio used in videos (optional)
├── .env                            # Contains environment variables
├── client_secrets.json             # Google API credentials for YouTube Data API
├── requirements.txt                # Python package dependencies
├── README.md                       # Project documentation

## Dependencies
- Python 3.x
- MoviePy
- Google API Client
- OpenAI API
- FFmpeg (for video processing)
- Boto3 (for AWS, if using EC2)

## License
This project is licensed under the MIT License. See the LICENSE file for details.




