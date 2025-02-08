import requests
import time
from lumaai import LumaAI
import os
from dotenv import load_dotenv
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()
client = ElevenLabs()

audio = client.text_to_speech.convert(
    text="The first move is what sets everything in motion.",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

play(audio)


load_dotenv("LumaAi.env")
auth_token=os.environ.get("LumaAI_api")
client = LumaAI(auth_token=auth_token)


# generation = client.generations.image.create(
#   prompt="A teddy bear in sunglasses playing electric guitar and dancing",
# )
# completed = False
# while not completed:
#   generation = client.generations.get(id=generation.id)
#   if generation.state == "completed":
#     completed = True
#   elif generation.state == "failed":
#     raise RuntimeError(f"Generation failed: {generation.failure_reason}")
#   print("Dreaming")
#   time.sleep(2)

# image_url = generation.assets.image

# # download the image
# response = requests.get(image_url, stream=True)
# with open(f'{generation.id}.jpg', 'wb') as file:
#     file.write(response.content)
# print(f"File downloaded as {generation.id}.jpg")