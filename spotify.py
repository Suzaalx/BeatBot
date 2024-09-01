import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import List, Optional
import json
from pydantic import BaseModel
from groq import Groq

load_dotenv('./.env')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
groq = Groq(api_key=os.getenv('API_KEY'))
print(client_id)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_profile = sp.current_user()
print(f"Logged in as {user_profile['display_name']}")

class SongRecommendation(BaseModel):
    song_name: str
    artist: Optional[str] = None

def get_similar_songs(song_name: str) -> List[SongRecommendation]:
    prompt = f"Give me a list of songs similar to {song_name}."
    
    try:
        chat_completion = groq.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a music expert and you just give more than 10 music recommendations in json.\n"
                    f" The JSON object must use the schema: {json.dumps(SongRecommendation.model_json_schema(), indent=2)}",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="llama-3.1-8b-instant",
            response_format={"type": "json_object"},
        )
        
        response_content = chat_completion.choices[0].message.content
        
        recommendations_data = json.loads(response_content)
       
        
       
        return recommendations_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

song = input("Enter the name of the song: ")
playlist_name = input("Enter the name for the playlist: ")
similar_songs = get_similar_songs(song)
print(similar_songs)
print(f"Found {len(similar_songs)} songs similar to '{song}':")

songs_uri = []
for song in similar_songs:
    result = sp.search(q=f"track:{song}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


if songs_uri:
    playlist = sp.user_playlist_create(user_profile['id'], playlist_name, public=False)
    sp.playlist_add_items(playlist['id'], songs_uri)
    print(f"Playlist '{playlist_name}' created with {len(songs_uri)} songs.")
else:
    print("No songs were found to add to the playlist.")

playlist = sp.user_playlist_create(user_profile['id'], playlist_name, public=False)
sp.playlist_add_items(playlist['id'], items=songs_uri)
