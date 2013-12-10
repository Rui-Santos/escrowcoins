import os


ssl_conf = None

# Configure the following according to where ssss is installed.
# ssss_split = os.path.abspath(os.path.join("ssss-0.5", "ssss-split"))
ssss_split = '/usr/bin/ssss-split'

# GPG command path
gpg = '/usr/local/bin/gpg'

# ZMQ socket path for pushing/pulling data regarding emails to be sent.
# For more configurations about this, check send_email.py
zmqemail = 'ipc:///tmp/zmqemail_escrow'
