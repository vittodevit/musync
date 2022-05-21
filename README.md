# musync
A program that gets your music from Spotify and downloads it from Youtube Music.
**NOTE**: This program is in it' s alpha stage and i'm not a Python developer, so, any contribution is appreciated!

# Installation
## Using Pip
```bash
  $ pip install musync
```
## Manual
```bash
  $ git clone https://github.com/vittodevit/musync
  $ cd musync
  $ python setup.py install
```
# Usage
```bash
$ musync [configfile]
```
## Configuration
Create a json file with this structure:
```json5
{
  "spotify_client_id": "...",
  "spotify_client_secret": "...",
  "playlists": [
    "https://open.spotify.com/playlist/...",
    /* ... */
  ]
}
```

### Spotify authorization:
To obtain the `client_id` and `client_secret`
1. Sign in [HERE](https://developer.spotify.com/dashboard/applications) with your Spotify account
2. Click on the green button **Create An App** and give it a Name and Description
3. Copy **Client ID**
4. Show and copy **Client Secret**