from ytmusicapi import YTMusic

yt = YTMusic()


def yt_search_closest_match(isrc, query_string, duration_msec):
    # first search for ISRC (possible exact match)
    ytid = ""
    delta = 1000000  # high number to make the first check possbile
    res_isrc = yt.search(query=isrc,
                         filter="songs"
                         )
    if len(res_isrc) > 0:
        for res in res_isrc:
            # search the closest match in duration to original song
            newdelta = abs(res["duration_seconds"] - duration_msec)
            if newdelta < delta:
                delta = newdelta
                ytid = res["videoId"]

        return ytid

    else:
        # if search with isrc is not successful, search by query string
        res_qs = yt.search(query=query_string)
        for res in res_qs:
            if res["category"] == "Songs" or res["category"] == "Videos":
                # search the closest match in duration to original song
                newdelta = abs(res["duration_seconds"] - duration_msec)
                if newdelta < delta:
                    delta = newdelta
                    ytid = res["videoId"]

        return ytid
