# lastfm nowplaying in mastodon profile

- Copy `.env.dist` to `.env`
- Put your keys and stuff
    - Mastodon: `https://[your instance]/settings/applications`
    - LastFM: https://www.last.fm/api/account/create
    - The two `MASTODON_NOTPLAYING_*` keys are what should be replaced and what will be shown if nothing is playing 
- Install deps in `requirements.txt`
- Run `nowplaying.py` and login if asked
- Let it run