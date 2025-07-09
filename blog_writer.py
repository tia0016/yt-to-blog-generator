import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

def generate_blog(transcript, output_type, tone):
    prompt = f"""
You are an AI that writes clear, creative, and engaging content.

Generate a {output_type.lower()} in a {tone.lower()} tone using this transcript:

\"\"\"
{transcript}
\"\"\"
"""

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",  # ✅ This works
            messages=[
                {"role": "system", "content": "You are a helpful blog writing assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ Error generating blog: {str(e)}"
