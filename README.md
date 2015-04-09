passweb
=======

Simple Web interface for `pass`. Designed to run on a single computer, and
assumes that gpg-agent has currently cached your PGP passphrase. If you need
remote access to your password and your PGP key is locked, you'll have to find
some way to SSH into your computer and unlock it with the command line (via
a device you own like a smartphone! Don't enter your PGP passphrase on someone
else's computer!) No, I will not implement some hacky thing that lets you enter
your PGP passphrase on some public computer. You should never do that.

## Install

    git clone
    cd passweb
    pip install -r requirements.txt

## Usage

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

## Issues

Doesn't work with passwords stored in folders. You'll have to manually
