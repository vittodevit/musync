def sf_get_all_songs(sp, playlist_url):
    # load the first 100 songs
    tracks = []
    result = sp.playlist_items(playlist_url, additional_types=['track'])
    tracks.extend(result['items'])

    # if playlist is larger than 100 songs, continue loading it until end
    while result['next']:
        result = sp.next(result)
        tracks.extend(result['items'])

    # remove all local songs
    i = 0  # just for counting how many tracks are local
    for item in tracks:
        if item['is_local']:
            tracks.remove(item)
            i += 1

    # print result
    return tracks
