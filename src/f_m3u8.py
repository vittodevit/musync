import os
import mmap


def add_to_playlist(playlist_name, spotify_id, duration, title, relative_path):
    playlist_path = playlist_name + ".m3u8"

    # if playlist does not exist create file
    if not os.path.exists(playlist_path):
        f = open(playlist_path, "w", encoding="utf-8")
        f.write("#EXTM3U\n\n")
        f.close()

    with open(playlist_path, 'rb', 0) as file, \
            mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
        if not s.find(bytearray(spotify_id.encode())) != -1:
            file.close()
            # write to file
            f = open(playlist_path, "a", encoding="utf-8")
            f.write("#" + spotify_id + '\n')
            f.write("#EXTINF:")
            f.write(str(int(duration)))
            f.write(",")
            f.write(title)
            f.write("\n")
            f.write(relative_path)
            f.write("\n\n")
            f.close()
        else:
            print("          File already added!")
