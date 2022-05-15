import click
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import f_spoti
import f_ytmusic


@click.command()
@click.argument('configfile', type=click.Path(exists=True))
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


if __name__ == '__main__':
    main()
