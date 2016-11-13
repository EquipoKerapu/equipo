from django.test import TestCase
from utils import email_regex

########## Regex Test ##########

class RegexTestCase(TestCase):

    bad_emails = [
                'test@pcc.edu',
                'john@cppedu',
                'fred@cp.edu',
                'gdfgfgdf',
                'testcpp.edu',
                'you@edu.edu',
                'walle@gmail.com'
                ]
    good_emails = [
                'test@cpp.edu',
                'john@cpp.edu',
                'fred@cpp.edu',
                'cristian@cpp.edu'
                ]

    def test_regex_valid(self):
        for bad in self.bad_emails:
            self.assertFalse(email_regex(bad))
        for good in self.good_emails:
            self.assertTrue(email_regex(good))
