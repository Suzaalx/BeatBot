# BeatBot: AI-Powered Music Recommendation and Playlist Generator

BeatBot is an intelligent music recommendation system that leverages AI to suggest similar songs and automatically create Spotify playlists based on user input.

## Features

- Utilizes Groq AI for generating song recommendations
- Integrates with Spotify API for playlist creation and song searching
- Provides personalized playlist generation based on a single song input
- Handles song availability on Spotify, skipping unavailable tracks

## Requirements

- Python 3.7+
- Spotify Developer Account
- Groq API Key

## Installation

1. Clone the repository
2. Install required packages: `pip install -r requirements.txt`
3. Set up a `.env` file with your Spotify and Groq API credentials

## Usage

1. Run the script: `python beatbot.py`
2. Enter a song name when prompted
3. Provide a name for your new playlist
4. The script will generate recommendations and create a Spotify playlist

## Configuration

Ensure your `.env` file contains:
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
API_KEY=your_groq_api_key