import os
import zmq
import json
import gpg
import ssss
import webcfg
import bitcoin
from django.core.mail import EmailMessage
from escrowcoins.utils import *
import escrowcoins.settings as settings


def post_handler(data):
    emails = (data['sender'], data['buyer'], data['escrower'])
    note = data.get('note', u'').encode('utf8')
    result = False
    if len(emails) == 3:
       # Test GPG.
        using_gpg = False
        for item in emails:
            recipient, use_gpg = item[1], 0
            if not use_gpg:
                continue
            using_gpg = True
            _, failed = gpg.encrypt('test', recipient)
            if failed:
                reply = {'error': 'Failed to obtain public for key %s' %
                        recipient}
                request.write(json.dumps(reply))
                return
        if using_gpg:
            gpg_note = ('If GPG fails for whatever reason, one or more emails '
                    'will be sent in plain text.')
        else:
            gpg_note = ''

        # Generate a new private key, and a bitcoin address from it.
        pk, wif_pk = bitcoin.privatekey()
        addr = bitcoin.address(pk)
        # Split the private key in m parts.
        shares = ssss.split(wif_pk, 2, 3)
        # Send the shares by email.
        sender = settings.ESCROW_SENDER
        subject= settings.ESCROW_SUBJECT
        for share, email in zip(shares, emails):
            message = "%s" %share
            result = send_simple_message(email,sender,message,subject)
        return result