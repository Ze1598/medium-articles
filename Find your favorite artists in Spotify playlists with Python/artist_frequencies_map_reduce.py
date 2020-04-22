from functools import reduce


def get_artist_counts(artists_info: List[List[Dict]]) -> Dict[str, int]:
    """
    Find the frequency of each artist featured in the playlist and return
    a dictionary of the type Artist:Frequency.
    """
    def map_fn(track_artists: List[Dict]) -> List[str]:
        """
        Helper function for `map`.
        Goes through the list of artists for one song and returns a list of
        strings, i.e., a list with the names of the featured artists.
        """
        return [artist["name"] for artist in track_artists]

    def inner_reduce_fn(all_artists: List[str], song_artists: List[str]) -> List[str]:
        """
        Helper function for the inner `reduce`.
        Take the individual lists of artists featured in each song and reduce
        them to a single list (i.e., the result is a single list with every
        instance of the artist being featured in a song).
        """
        return all_artists + song_artists

    def outer_reduce_fn(result: Dict[str, int], name: str) -> Dict[str, int]:
        """
        Helper function for the outer `reduce`.
        Takes in the current dictionary of artist frequencies and updates it
        given the next artist name.
        """
        if name in result:
            result[name] += 1
            return result
        else:
            result[name] = 1
            return result

    # `map` gets a list where each element is a list with all the featured\
    # artists for one song
    # the inner `reduce` makes a single list of all artist instances
    # the outer `reduce` counts the artist frequency
    artist_counts = reduce(
        outer_reduce_fn,
        reduce(
            inner_reduce_fn,
            map(map_fn, artists_info),
            []
        ),
        {}
    )

    return artist_counts
