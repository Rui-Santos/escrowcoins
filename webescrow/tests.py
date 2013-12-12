"""
webescrow Tests
run with "manage.py test".
"""

from django.utils import unittest
import escrowhandler
import bitcoin

class EscrowHander(unittest.TestCase):

    """webescrow handler tests"""

    def test_post_emails(self):
    	"""are the number of emails posted 3"""
    	data = {}
    	data['escrower'] = "A@A"
    	data['buyer'] = "A@A"
    	data['sender'] = "A@A"
    	result = escrowhandler.post_handler(data);
    	self.assertEqual(200,result['result']);

class Bitcoin(unittest.TestCase):
	"""test bitcoin handler"""

	def test_private_key_length(self):
		'''check private key length'''
		self.assertEqual(2,len(bitcoin.privatekey()))

	def test_bitcoin_address(self):
		'''check if bitcoin address generate is valid'''
		pk  = bitcoin.privatekey()
		addr = bitcoin.address(pk)
		self.assertEqual(addr,len(bitcoin.address(bitcoin.privatekey())))
		

