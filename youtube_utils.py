from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re

def extract_video_id(youtube_url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, youtube_url)
    return match.group(1) if match else None

def get_transcript_from_url(youtube_url):
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return "❌ Invalid YouTube URL."

    try:
        # Try to fetch transcript in English first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except NoTranscriptFound:
        try:
            # Try Hindi if English is not found
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        except Exception:
            try:
                # Try fetching in any available language
                transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_generated_transcript(['hi', 'en', 'auto'])
                transcript = transcript.fetch()
            except Exception as e:
                return f"⚠️ Could not fetch transcript: {str(e)}"
    except Exception as e:
        return f"⚠️ Could not fetch transcript: {str(e)}"

    # Join text
    full_text = " ".join([entry['text'] for entry in transcript])
    return full_text
