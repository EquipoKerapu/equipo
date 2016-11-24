from django.test import TestCase
from equipo.utils import *


class UtilsTestCase(TestCase):
    def setUp(self):
        self.bad_emails = [
                    'test@pcc.edu',
                    'john@cppedu',
                    'fred@cp.edu',
                    'gdfgfgdf',
                    'testcpp.edu',
                    'you@edu.edu',
                    'walle@gmail.com'
                    ]
        self.good_emails = [
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

    def test_group_students(self):
        size = 3
        data = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        larger_groups = get_larger_groups(size, data)
        groups = group_students(size, data)
        self.assertEqual(len(larger_groups), size)
        self.assertEqual(len(groups), len(data)/size)

        for group in groups:
            self.assertTrue(len(group) >= size - 1 and len(group) <= size + 1)

        # if len(data)%size == size - 1, get an extra group
        size = 3
        data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        larger_groups = get_larger_groups(size, data)
        groups = group_students(size, data)
        self.assertEqual(len(larger_groups), size)
        self.assertEqual(len(groups), len(data)/size + 1)

        for group in groups:
            self.assertTrue(len(group) >= size - 1 and len(group) <= size + 1)



