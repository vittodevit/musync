import click
import json
import os
import spotipy
import glob
from spotipy.oauth2 import SpotifyClientCredentials
import f_spoti
import f_ytmusic


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

    client_id = config["spotify_client_id"]
    client_secret = config["spotify_client_secret"]
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    for uri in config["playlists"]:
        playlist = sp.playlist(uri)
        click.echo("[i] Loading tracks from playlist `" + playlist["name"] + "`")
        click.echo(
            "    Playlist has " +
            str(playlist["tracks"]["total"]) +
            " tracks"
        )
        for song in f_spoti.sf_get_all_songs(sp, uri):
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
            #  TODO: CHECK IF THIS CODE WORKS

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
            filename = song["track"]["track_number"] + " " + song["track"]["name"]

            if glob.glob(os.path.join(albumdir, filename + ".*")):
                click.echo("        Song already downloaded! Skipping.")
            else:
                print()
                #  TODO: download from yt, metadata application, move file


if __name__ == '__main__':
    main()
