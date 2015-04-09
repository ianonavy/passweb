passweb
=======

Simple Web interface for `pass`. Designed to run on a single computer, and
assumes that gpg-agent has currently cached your PGP passphrase. If you need
remote access to your password and your PGP key is locked, you'll have to find
some way to SSH into your computer and unlock it with the command line (via
a device you own like a smartphone! Don't enter your PGP passphrase on someone
else's computer!) No, I will not implement some hacky thing that lets you enter
your PGP passphrase on some public computer. You should never do that.

## Prerequisites

* Python 3
* pip
* openssl
* pass

## Features

* HTTPS
* CSRF protection on login
* Very simple UI
* Run it yourself
* Gives you the option to change the login password without having to type a
  new one
  - the threat model here is you're logging in on a public computer, and you
    can't assume the computer does not have a keylogger
  - the threat model also assumes that they're not using screen capture software
    because otherwise how would you even see the password

## Install

    git clone
    cd passweb
    pip install -r requirements.txt

## Setup

Generate a private key and self-signed cert:

    cd passweb
    openssl genrsa -out passweb.key 4096
    openssl req -new -x509 -key passweb.key -out passweb.cert -days 1095

Create a secret key for sessions:

    cd passweb
    pwgen 128 1 > secret.txt

Store the password for passweb in pass (duh)

    pass insert passweb
    (enter password here)

## Running

You probably want to run this in a tmux in screen session. An AUR package with a
systemd hook will come later!

    cd passweb
    python server.py

## Issues

Doesn't clear passwords from memory
