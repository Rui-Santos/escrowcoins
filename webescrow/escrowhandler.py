import os
import json
import gpg
import ssss
import bitcoin
import mailer


def post_handler(data):
    '''
    returns a json response with error messages etc
    '''
    emails = (['Escrower',data['escrower'], False],
        ['Buyer',data['buyer'], False],
        ['Seller',data['sender'], False]
        )
    note = data.get('note', u'').encode('utf8')
    result = {}
    if len(emails) == 3:
       # Test GPG.
        using_gpg = False
        for item in emails:
            recipient, use_gpg = item[1], item[2]
            if not use_gpg:
                continue
            using_gpg = True
            _, failed = gpg.encrypt('test', recipient)
            if failed:
                result['error'] =  'Failed to obtain public for key %s' %recipient
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
        # Send the shares by email
        for share, email in zip(shares, emails):
            message = "%s" %share
            response = mailer.processMail([note, share, addr,
                email[0], email[1], str(int(email[2]))]
                )
        result['result']=response
        return result