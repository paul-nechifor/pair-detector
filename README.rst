This repository has been moved to `gitlab.com/paul-nechifor/pair-detector <http://gitlab.com/paul-nechifor/pair-detector>`_.
============================================================================================================================

Old readme:

Pair Detector
=============

Image detection for pairs.

Usage
-----

Create ``env.env`` which should look like::

    praw_username=<your-user-name>
    praw_password=<your-password>
    praw_client_id=<your-client-id>
    praw_client_secret=<your-client-secret>
    praw_user_agent='<your-user-agent>'
    subreddits='<your-subreddits-to-follow>'

Then run::

    docker-compose up

Tests
-----

Run with::

    docker-compose exec pair-detector src/test

License
-------

MIT
