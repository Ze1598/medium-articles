from os import environ
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from typing import List, Dict
# https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py


# Authenticate to Spotify
def authenticate(cliend_id: str, client_secret: str) -> spotipy.client.Spotify:
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=cliend_id,
            client_secret=client_secret
        )
    )

    return sp


# Number of tracks available in the playlist
def get_pl_length(sp: spotipy.client.Spotify, pl_uri: str) -> int:
    return sp.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"
    )["total"]


# Get all the artist info about each track of the playlist.
def get_tracks_artist_info(sp: spotipy.client.Spotify, pl_uri: str) -> List[List[Dict]]:
    artists_info = list()
    # Start retrieving tracks from the beginning of the playlist
    offset = 0
    pl_length = get_pl_length(sp, pl_uri)

    # Playlist track retrieval only fetches 100 tracks at a time, hence\
    # the loop to keep retrieving until we reach the end of the playlist
    while offset != pl_length:
        # Get the next batch of tracks
        pl_tracks = sp.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track"
        )

        # Get the list with the info about the artists of each track from the\
        # latest batch and append it to the running list
        [artists_info.append(pl_item["track"]["artists"])
            for pl_item in pl_tracks["items"]]

        # Update the offset
        offset += len(pl_tracks["items"])

    return artists_info


# Calculate the frequency of each artist in the playlist
def get_artist_counts(artists_info: List[List[Dict]]) -> Dict[str, int]:
    artist_counts = dict()

    # Loop through the lists of artist information
    for track_artists in artists_info:
        # Loop through the artists associated with the current track
        for artist in track_artists:
            # Update the current artist's frequency
            artist_name = artist["name"]
            if artist_name in artist_counts:
                artist_counts[artist_name] += 1
            else:
                artist_counts[artist_name] = 1

    return artist_counts


# Save the artist frequencies in a CSV file
def save_artists_csv(artists_counts: Dict[str, int]) -> None:
    # Get a list of the artists featured in the playlist
    artists = list(artists_counts.keys())
    # Get a list of the frequencies of each artist
    frequencies = [freq for artist, freq in artists_counts.items()]
    # Create a dictionary for the dataframe
    data = {
        "Artist": artists,
        "Frequency": frequencies
    }
    # Create the dataframe and save it as CSV (without indices)
    new_df = pd.DataFrame(data=data)
    new_df.to_csv("artists_frequencies.csv", index=False)


if __name__ == "__main__":
    # Get the credentials from environment variables
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    # Get a Spotify authenticated instance
    sp_instance = authenticate(CLIENT_ID, CLIENT_SECRET)

    # Playlist URI to look up
    pl_uri = "spotify:playlist:7bLzIyyGRUJw78eHtUZItf"

    # Get the artist information for all tracks of the playlist
    artists_info = get_tracks_artist_info(sp_instance, pl_uri)

    # Get the frequencies of each artist
    artists_counts = get_artist_counts(artists_info)

    # Save the artist frequencies in a CSV
    save_artists_csv(artists_counts)
