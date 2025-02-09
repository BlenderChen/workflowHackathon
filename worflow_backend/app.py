from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import time
from lumaai import LumaAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Load environment variables for LumaAI and ElevenLabs
load_dotenv("LumaAi.env")
luma_auth_token = os.environ.get("LumaAI_api")
clientLumaAI = LumaAI(auth_token=luma_auth_token)

load_dotenv("ElevenLabs.env")
elevenlabs_auth_token = os.environ.get("ElevenLabs_api")
clientElevenLabs = ElevenLabs(api_key=elevenlabs_auth_token)

# Define the path to the video folder outside of workflow_backend.
# For example, if your project structure is:
# project-root/
#   ├── workflow_backend/ (this file lives here)
#   ├── videos/ (we will save videos here)
VIDEO_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'videos')
os.makedirs(VIDEO_FOLDER, exist_ok=True)  # Ensure the directory exists

# Enable CORS
app = Flask(__name__)
CORS(app)

def mutipleSentence_to_video(sentence):
    """Generates a video using LumaAI and saves it in the VIDEO_FOLDER."""
    generation = clientLumaAI.generations.create(
        prompt=sentence,
        model="ray-2",
        resolution="720p",
        duration="9s"
    )
    completed = False
    while not completed:
        generation = clientLumaAI.generations.get(id=generation.id)
        if generation.state == "completed":
            completed = True
        elif generation.state == "failed":
            raise RuntimeError(f"Generation failed: {generation.failure_reason}")
        print("Generating Video...")
        time.sleep(3)
    
    video_url = generation.assets.video
    response = requests.get(video_url, stream=True)
    
    # Save video file in the VIDEO_FOLDER with a truncated filename
    video_filename = f"{generation.id[:10]}.mp4"
    video_path = os.path.join(VIDEO_FOLDER, video_filename)
    with open(video_path, 'wb') as file:
        file.write(response.content)
    
    print(f"Video saved in VIDEO_FOLDER as {video_filename}")
    return video_filename  # Return the filename

def script_to_audio(script):
    """Converts the script to speech using ElevenLabs."""
    audio = clientElevenLabs.text_to_speech.convert(
        text=script, 
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)

@app.route('/', methods=['GET'])
def get_scripts():
    """Handles the request to generate a video from the given text."""
    script = request.args.get("query", "").strip()

    if not script:
        return jsonify({"error": "No script provided"}), 400

    video_filename = mutipleSentence_to_video(script)  # Generate video and get filename
    script_to_audio(script)  # Convert full script to audio

    # Construct the URL from which the frontend can access the video.
    video_url = f"/videos/{video_filename}"
    print(f"Sending video URL: {video_url}")  # Debugging log

    return jsonify({
        "videoUrl": video_url  # Send relative path to the frontend
    })

# New route to serve videos from the VIDEO_FOLDER
@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
