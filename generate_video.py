from openai import OpenAI
import random
import os
import re

from gtts import gTTS
import requests
from tempfile import NamedTemporaryFile
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx

client = OpenAI()


class GenrateVideo:

    prompt_variations = [
                "Generate a random and unique category.",
                "Please give me a completely random category, one word only.",
                "What is a random topic for a video? Just a single word category.",
                "Give me a random topic, one-word category only.",
                "Suggest a unique category, just one word."
            ]
    
    def generate_category(self):
        prompt = random.choice(self.prompt_variations)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=24,
            temperature=1.2,  # Increase randomness
            n=1  # Generate one response
        )
        category = response.choices[0].message.content.strip()
        return category

    def generate_script(self):
        category = self.generate_category()
        print(category)
        prompt = f"Generate a real random instresting short story in a paragraph for a youtube shorts about {category}"
        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
          ],
          max_tokens=300,
          temperature=0.9,
          top_p=1,
          frequency_penalty=1,
          presence_penalty=0.5,
          stop=["\n"]
        )
        return response.choices[0].message.content.strip()

    # Helper function to download image from URL and return a temporary file path
    def download_image_from_url(self, image_url):
        response = requests.get(image_url)
        img_temp = NamedTemporaryFile(delete=False, suffix=".png")  # Temporary file
        img_temp.write(response.content)
        img_temp.close()
        return img_temp.name  # Return the file path to the downloaded image

    

    def generate_title_category_keywords(self, script):
        promt= f"""
              I have a script for a YouTube video. Please provide the following based on the content of the script:
              1. A catchy, SEO-optimized title for the video.
              2. A list of relevant keywords (5-10) as python list, that can help the video rank well in search results.
              3. The appropriate YouTube category number only for the video based on its content (e.g., 1 for "Film & Animation", 10 for "Music").

              Here is the script:

              "{script}"

              Please output the result in the following format:

              Title: [Your generated title]
              Keywords: [list of keywords]
              Category Number: [YouTube category number]

              """

        response = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": promt}
          ],
          max_tokens=500,
          temperature=0.9,
          top_p=1,
          frequency_penalty=1,
          presence_penalty=0.5,
        )
        
        result = response.choices[0].message.content.strip()
        # Use regular expressions to capture the title, keywords, and category number
        title_match = re.search(r'Title:\s*(.*)', result)
        keywords_match = re.search(r'Keywords:\s*\[(.*)\]', result)
        category_match = re.search(r'Category Number:\s*(\d+)', result)

        # Extract the matches or provide a default empty value if not found
        title = title_match.group(1) if title_match else None
        keywords = keywords_match.group(1).split(", ") if keywords_match else []
        cleaned_keywords = [item.strip('"') for item in keywords]
        category_number = int(category_match.group(1)) if category_match else None

        hashtags = [f"#{keyword.replace(' ', '_')}" for keyword in cleaned_keywords]

        # Create a dictionary
        video_info = {
            "Title": title,
            "Keywords": ','.join(cleaned_keywords),
            "Category Number": category_number,
            "script": script+ '\n' + ' '.join(hashtags)
        }
        return video_info
        

    def generate_image_audio_pair(self):
        script = self.generate_script()
        images_with_audio = []
        video_info = self.generate_title_category_keywords(script)
        image_prompt= script.split('.')[0].strip()
        response = client.images.generate(
          model="dall-e-2",
          prompt=image_prompt[:999],
          size="512x512",
          quality="standard",
          n=1,
        )

        image_url = response.data[0].url
        image_path = self.download_image_from_url(image_url)

        tts = gTTS(text=script, lang='en', tld='co.in')
        audio_path = f"/tmp/audio_clips/narration.mp3"
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        tts.save(audio_path)
        images_with_audio.append((image_path, audio_path))
        return images_with_audio, video_info

    def create_video(self, output_path="output_video.mp4"):
        clips = []
        images_with_audio, video_info = self.generate_image_audio_pair()
        video_info['output_path'] = output_path
        total_duration = 0
        # Loop through each image URL and its corresponding audio file
        for image_path, audio_path in images_with_audio:
            # Create an AudioFileClip for the corresponding audio
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration  # Set duration to match the length of the audio clip
            total_duration += duration
            # Create an ImageClip for the given image and set its duration
            image_clip = ImageClip(image_path).set_duration(duration)

            # Set the audio for the image clip
            video_clip = image_clip.set_audio(audio_clip)

            # Append the individual video clip to the list
            clips.append(video_clip)

        # Concatenate all the individual video clips
        final_video = concatenate_videoclips(clips)
        # If total video duration is between 60 and 90 seconds, speed up the video
        if 60 <= final_video.duration <= 75:
            # Calculate the speed factor to reduce the video to 59 seconds
            speed_factor = final_video.duration / 59
            final_video = final_video.fx(vfx.speedx, speed_factor)  # Speed up the video

        # Write the final video to the output file
        final_video.write_videofile(output_path, codec="libx264", fps=24)
        print(video_info)
        return video_info



