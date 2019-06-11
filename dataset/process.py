import csv, json

decimal_column = [
    "acousticness",
    "audio_valence",
    "danceability",
    "energy",
    "instrumentalness",
    "liveness",
    "loudness",
    "speechiness",
    "tempo"
]

integer_column = [
    "song_popularity",
    "audio_mode",
    "key",
    "song_duration_ms",
    "time_signature"
]

def main():
    # getting the data of the song details file
    with open("song_data.csv", encoding='utf-8') as song_details_file:
        song_details = csv.DictReader(song_details_file)
        # getting the data of the playlist details file
        with open("song_info.csv", encoding='utf-8') as playlist_details_file:
            playlist_details = csv.DictReader(playlist_details_file)
            # join the tables
            table = list()
            for data in song_details:
                for more_data in playlist_details:
                    if more_data["song_name"] == data["song_name"]:
                        data.update(more_data)
                        table.append(data.copy())
                        break
        # create the result dict
        result = dict()
        songsList = list()
        for row in table:
            # get the playlist node
            if row["playlist"] not in result:
                result[row["playlist"]] = dict()
                result[row["playlist"]]["playlist_name"] = row["playlist"]
                result[row["playlist"]]["artistsD"] = dict()
            playlist = result[row["playlist"]]

            # get the artist node
            if row["artist_name"] not in playlist["artistsD"]:
                playlist["artistsD"][row["artist_name"]] = dict()
                playlist["artistsD"][row["artist_name"]]["artist_name"] = row["artist_name"]
                playlist["artistsD"][row["artist_name"]]["albumsD"] = dict()
            artist = playlist["artistsD"][row["artist_name"]]

            # get the album node
            if row["album_names"] not in artist["albumsD"]:
                artist["albumsD"][row["album_names"]] = dict()
                artist["albumsD"][row["album_names"]]["album_name"] = row["album_names"]
                artist["albumsD"][row["album_names"]]["songs"] = list()
            album = artist["albumsD"][row["album_names"]]

            # insert the song
            song_entry = dict()
            song_info = dict()
            for key in row:
                # correct the data value
                if key in decimal_column:
                    value = float(row[key])
                elif key in integer_column:
                    value = int(row[key])
                else:
                    value = row[key]
                
                if key == "instrumentalness":
                    print(value)
                    
                # populate the songs array
                if key == "playlist":
                    song_info["playlist_name"] = value
                # elif key == "album_names":
                #     song_info["album_name"] = value
                elif key not in ["artist_name", "album_names"]:
                    song_info[key] = value
                
                # populate the playlist array
                if key not in ["artist_name", "album_names", "playlist"]:
                    song_entry[key] = value
            album["songs"].append(song_entry)
            songsList.append(song_info)

        # count the playlist
        # result["#count"] = len(result.keys())
        resultList = list()
        for playlist in result.values():
            if type(playlist) == int:
                continue
            playlist["artists"] = list()
            for artist in playlist["artistsD"].values():
                artist["albums"] = list()
                for album in artist["albumsD"].values():
                    artist["albums"].append(album)
                artist.pop("albumsD")
                playlist["artists"].append(artist)
            playlist.pop("artistsD")
            resultList.append(playlist)

        # export the json
        with open("dataProcessed.json", 'w', encoding='utf-8') as f:
            json.dump(resultList, f, sort_keys=True)
        with open("dataRaw.json", 'w', encoding='utf-8') as f:
            json.dump(songsList, f, sort_keys=True)

if __name__ == "__main__":
	 main()
