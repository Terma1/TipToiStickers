import boto3
import json
import os

polly_client = boto3.Session(
    aws_access_key_id='PLEASE WRITE YOUR ACCESS KEY',
    aws_secret_access_key='PLEASE WRITE YOUR SECRET ACCESS KEY',
    region_name='us-west-2'
).client('polly')

json_file = 'circle_data.json'

output_directory = 'tttool/audio'
os.makedirs(output_directory, exist_ok=True)

with open(json_file, "r") as f:
    data = json.load(f)

for circle in data.get("circles", []):  # Loop through the "circles" array
    text = circle.get("text", "")  # Get the "text" property from the circle object
    if text:
        response = polly_client.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Matthew')

        audio_file = os.path.join(output_directory, f"audio_{circle['number']}.wav")

        with open(audio_file, 'wb') as f:
            f.write(response['AudioStream'].read())

        print(f"Generated audio file {audio_file}")
