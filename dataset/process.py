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
        songsList = list()
        playlistList = list()
        for row in table:
            # get the playlist songs array
            if row["playlist_name"] not in playlistList:
                playlistList.append(row["playlist_name"])

            # insert the song
            song_info = dict()
            for key in row:
                # correct the data value
                if key in decimal_column:
                    value = float(row[key])
                elif key in integer_column:
                    value = int(row[key])
                else:
                    value = row[key]
                    
                # populate the songs array
                if key not in [ "artist_name", "album_name" ]:
                    song_info[key] = value
            songsList.append(song_info)

        # export the json
        with open("dataArray.json", 'w', encoding='utf-8') as f:
            json.dump(songsList, f , sort_keys=True)
        with open("dataKey.json", 'w', encoding='utf-8') as f:
            json.dump(playlistList, f, sort_keys=True)
        print("Number of entries: " + str(len(songsList)))
        print("Number of playlists: " + str(len(playlistList)))

if __name__ == "__main__":
	 main()
