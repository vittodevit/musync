import json
import os
import glob
import spotipy
import ffmpeg
import click
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.mp4 import MP4, MP4Cover
from urllib import request
import f_spoti
import f_ytmusic
import f_m3u8


@click.command()
@click.argument('configfile', type=click.Path(exists=True))
# TODO: musync batch / musync get (differentiate login and not)
def main(configfile):
    config = {}

    try:
        f = open(configfile, "r")
        config = json.load(f)
        # click.echo(config["spotify_client_id"])
        click.echo("[i] Configuration loaded")
    except:
        click.echo("Cannot load json data from configuration file.")
        return

    client_id = config["spotify_client_id"]
    client_secret = config["spotify_client_secret"]
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    error_list = open("error_list.txt", "w", encoding="utf-8")

    for uri in config["playlists"]:
        playlist = sp.playlist(uri)
        click.echo("[i] Loading tracks from playlist `" + playlist["name"] + "`")
        click.echo(
            "    Playlist has " +
            str(playlist["tracks"]["total"]) +
            " tracks"
        )
        for song in f_spoti.sf_get_all_songs(sp, uri):
            try:
                # print info about track
                click.echo(
                    "    Working on `" +
                    song["track"]["name"] +
                    "` by `" +
                    song["track"]["artists"][0]["name"] +
                    "` with ISRC: " +
                    song["track"]["external_ids"]["isrc"]
                )
                # search YouTube music
                yt_id = f_ytmusic.yt_search_closest_match(
                    song["track"]["external_ids"]["isrc"],
                    song["track"]["name"] +
                    " " +
                    song["track"]["artists"][0]["name"],
                    song["track"]["duration_ms"] / 1000
                )

                click.echo("        Found track: https://www.youtube.com/watch?v=" + yt_id)
                artistdir = ""

                # check if artist folder exists, otherwise create it
                if len(song["track"]["album"]["artists"]) > 1:
                    if not os.path.isdir("Various Artists"):
                        os.mkdir("Various Artists")
                    artistdir = "Various Artists"
                else:
                    if not os.path.isdir(song["track"]["album"]["artists"][0]["name"]):
                        os.mkdir(song["track"]["album"]["artists"][0]["name"])
                    artistdir = song["track"]["album"]["artists"][0]["name"]

                albumdir = os.path.join(artistdir, song["track"]["album"]["name"])

                # check if album folder exists, otherwise create it
                if not os.path.isdir(albumdir):
                    os.mkdir(albumdir)

                # check if file is already downloaded
                filename = str(song["track"]["track_number"]) + " " + song["track"]["name"]

                filename_bc = os.path.join(albumdir, filename) + ".webm"
                filename_ac = os.path.join(albumdir, filename) + ".m4a"

                glob_check = glob.escape(os.path.join(albumdir, filename))
                if glob.glob(glob_check + ".m4a"):
                    click.echo("        Song already downloaded! Skipping.")
                else:
                    click.echo("        Downloading song...")
                    f_ytmusic.download(yt_id, filename_bc)

                    #  file conversion
                    ff_input = ffmpeg.input(filename_bc)
                    ff_audio = ff_input.audio
                    ff_out = ffmpeg.output(ff_audio, filename_ac, acodec="aac")
                    ffmpeg.run(ff_out, quiet=True)
                    os.unlink(filename_bc)

                    #  metadata application
                    tags = MP4(filename_ac).tags
                    tags["\xa9nam"] = song["track"]["name"]
                    tags["\xa9alb"] = song["track"]["album"]["name"]

                    i = 0
                    artists = ""
                    for artist in song["track"]["artists"]:
                        if i != 0:
                            artists = artists + ", "
                        artists = artists + artist["name"]
                        i = i + 1
                    tags["\xa9ART"] = artists

                    i = 0
                    albumartists = ""
                    for artist in song["track"]["album"]["artists"]:
                        if i != 0:
                            albumartists = albumartists + ", "
                        albumartists = albumartists + artist["name"]
                        i = i + 1
                    tags["aART"] = albumartists

                    tags["\xa9day"] = song["track"]["album"]["release_date"][-4]
                    tags["\xa9cmt"] = song["track"]["uri"]
                    tags["\xa9too"] = "vittodevit/musync with FFMpeg"
                    tags["trkn"] = [(song["track"]["track_number"], song["track"]["album"]["total_tracks"])]
                    tags["disk"] = [(1, 1)]

                    cover_image = request.urlopen(song["track"]["album"]["images"][0]["url"])
                    tags["covr"] = [MP4Cover(cover_image.read(), imageformat=MP4Cover.FORMAT_JPEG)]

                    tags.save(filename_ac)

                # playlist creation
                click.echo("        Adding to M3U playlist")
                f_m3u8.add_to_playlist(
                    playlist["name"],
                    song["track"]["uri"],
                    song["track"]["duration_ms"] / 1000,
                    song["track"]["name"],
                    filename_ac
                )
            except:
                click.echo(
                    "    Error downloading " +
                    song["track"]["name"] +
                    "` by `" +
                    song["track"]["artists"][0]["name"]
                    , err=True
                )
                error_list.write(
                    "Error downloading " +
                    song["track"]["name"] +
                    "` by `" +
                    song["track"]["artists"][0]["name"] +
                    "` with URL: " +
                    song["track"]["uri"]
                )

    error_list.close()


if __name__ == '__main__':
    main()
