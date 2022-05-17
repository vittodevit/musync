from ytmusicapi import YTMusic
import youtube_dl
import sys

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


class YtdlLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def progress_hook(d):
    if d['status'] == 'finished':
        print('\n        Done downloading, now converting ...')
    else:
        sys.stdout.write("\r          " + d["_percent_str"] + " at speed " + d["_speed_str"])
        sys.stdout.flush()


def download(video_id, savepath):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'logger': YtdlLogger(),
        'progress_hooks': [progress_hook],
        'outtmpl': savepath,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + video_id])
