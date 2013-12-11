Requirements for Webescrow app
==============================

Requirements
============

Python 2.7 (http://python.org),
ZMQ (http://zeromq.org/),
pyzmq (https://github.com/zeromq/pyzmq),
python-ecdsa (https://github.com/warner/python-ecdsa)
ssss (http://point-at-infinity.org/ssss/),
tornado (http://www.tornadoweb.org/),
OpenSSL (https://www.openssl.org/),
pyOpenSSL (https://launchpad.net/pyopenssl),
GPG (http://gnupg.org/),
and a SMTP server properly configured.

Setup
=====
Add `local_settings.py` to hold your local
configurations. Make sure the program `ssss-split` is found at
the place specified by `ssss_split` at `settings.py`.
