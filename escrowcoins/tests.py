"""
Escrowcoins Tests
run with "manage.py test".
"""

from django.utils import unittest
from utils import send_simple_message

class Utils(unittest.TestCase):

    """webescrow handler tests"""

    def test_send_email(self):
    	"""Test our email sending utility"""
    	self.assertEqual(200,send_simple_message('madradavid@gmail.com',
    		'madradavid@gmail.com','Testing Email',
    		 'Here is the message.')
    	);

