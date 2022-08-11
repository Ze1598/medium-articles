from os import environ
import requests
import pandas as pd
from typing import List, Dict


def authenticate(client_id: str, client_secret: str) -> str:
    session = requests.Session()
    session.auth = (client_id, client_secret)

    auth = session.post(
        "https://accounts.spotify.com/api/token",
        {"grant_type": "client_credentials"}
    )
    token = auth.json()["access_token"]

    return token


def get_playlists(access_token: str, username: str) -> Dict[str, str]:
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(
        f"{BASE_URL}v1/users/{username}/playlists",
        headers = headers
    )

    # List of playlist dicts
    pl_array = resp.json()["items"]
    # Map id to name
    pl_dict = {pl["id"]: pl["name"] for pl in pl_array}

    return pl_dict


def flatten_playlist(data: Dict) -> pd.DataFrame:
    df = pd.json_normalize(data, sep="_")
    df.to_csv("temp.csv", index=False)
    # Keep only tracks provided by spotify
    df = df.query("is_local == False")
    df = df[["track_album_name", "track_album_id", "track_album_album_type", "track_artists", "track_id", "track_name"]]

    # Explode the artist arrays
    flat_col = df["track_artists"].explode().to_frame()
    # Indexes are duplicated upon explode, i.e. still in sync with original DF
    df = df.drop(columns=["track_artists"]).join(flat_col)

    # Flatten the artist objects
    flat_col = pd.json_normalize(df["track_artists"], sep = "_").add_prefix("artist_")
    # Reuse the index of the original DF
    flat_col.index = df.index
    # And append horizontally the flattened columns
    df = pd.concat([df, flat_col], axis=1).drop(columns=["track_artists"])

    # Select and rename final columns
    df = df[["track_id", "track_name", "track_album_id", "track_album_name", "track_album_album_type", "artist_id", "artist_name"]]
    df.columns = ["track_id", "track_name", "album_id", "album_name", "album_type", "artist_id", "artist_name"]
    
    return df


def get_playlist_tracks(access_token: str, playlist_id: str, username: str) -> pd.DataFrame:
    headers = {"Authorization": f"Bearer {access_token}"}
    offset = 0
    run_loop = True
    pages_array = list()

    # Get the complete playlist
    while run_loop:
        resp = requests.get(
            f"{BASE_URL}v1/users/{username}/playlists/{playlist_id}/tracks?offset={offset}",
            headers=headers
        )
        resp_json = resp.json()
        pl_total = resp_json["total"]
        pages_array.append(resp_json["items"])

        offset += 100
        if offset > pl_total:
            run_loop = False

    # Flatten each dict
    pages_array_flat = [flatten_playlist(page_dict) for page_dict in pages_array]
    # And consolidate as a single DF
    complete_pl = pd.concat(pages_array_flat)

    return complete_pl


def get_all_playlists_tracks(access_token: str, pl_dict: Dict[str, str], username: str) -> pd.DataFrame:
    # List for the complete DF of each playlist
    pl_tracks_array = list()

    # Get a single DF per playlist with all its tracks
    for pl_id in pl_dict:
        playlist = get_playlist_tracks(access_token, pl_id, username)
        playlist["playlist_id"] = pl_id
        playlist["playlist_name"] = pl_dict[pl_id]
        pl_tracks_array.append(playlist)

    # Consolidade all playlist DFs into a single DF
    complete_df = pd.concat(pl_tracks_array)

    return complete_df


def process_audio_features(data: List[Dict]) -> pd.DataFrame:
    audio_features_array_flat = [pd.json_normalize(pd.DataFrame(track_features)["audio_features"]) for track_features in data]
    audio_features_df = pd.concat(audio_features_array_flat)
    
    columns_list = ["id", "danceability", "energy", "loudness", "acousticness", "instrumentalness", "valence", "tempo", "duration_ms"]
    audio_features_df = audio_features_df[columns_list]
    
    audio_features_df["duration_minutes"] = audio_features_df["duration_ms"] / 1000 // 60
    audio_features_df.drop("duration_ms", axis = 1, inplace = True)
    
    columns_list = [name.replace("_", " ").capitalize() for name in columns_list]
    columns_list[0] = "track_id"
    columns_list[8] = "Duration (minutes)"
    audio_features_df.columns = columns_list
    
    audio_features_df = audio_features_df.melt(columns_list[0], columns_list[1:])
    
    return audio_features_df


def get_all_tracks_audio_features(access_token: str, tracks_array: List[str]) -> pd.DataFrame:
    audio_features_array = list()
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    for i in range(0, len(tracks_array), 50):
        tracks_query = ",".join(tracks_array[i: i+50])
        resp = requests.get(
            f"{BASE_URL}v1/audio-features?ids={tracks_query}",
            headers=headers
        )
        audio_features_array.append(resp.json())
    
    complete_df = process_audio_features(audio_features_array)
    
    return complete_df


if __name__ == "__main__":
    # Read env variables
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    BASE_URL = "https://api.spotify.com/"
    USERNAME = "your_username"
    token = authenticate(CLIENT_ID, CLIENT_SECRET)

    # Playlists must be public and added to the user profile
    playlists = get_playlists(token, USERNAME)

    # Get all albums, artists, and tracks for each playlist    
    complete_playlists = get_all_playlists_tracks(token, playlists, USERNAME)
    complete_playlists.to_parquet("tracks_playlists.parquet", index = False)

    # Get the audio features for each unique track discovered
    tracks_array = complete_playlists["track_id"].unique()
    audio_features_df = get_all_tracks_audio_features(token, tracks_array)
    audio_features_df.to_parquet("audio_features.parquet", index = False)