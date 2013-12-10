import os
import zmq
import json
import gpg
import ssss
import webcfg
import bitcoin
from django.core.mail import EmailMessage


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
        shares = ssss.split(wif_pk, 3, 3)
        # Send the shares by email.
        for share, email in zip(shares, emails):
            print email
            print share
            print addr
            print note
            print '+++++++++'
            #request.sock.send_multipart([note, share, addr,
            #    email[0], email[1], str(int(email[2]))])
        return result