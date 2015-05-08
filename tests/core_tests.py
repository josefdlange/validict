import unittest

from validict import validate, FailedValidationError

class ValidictTests(unittest.TestCase):
    def test_good_dict(self):
        template = {
            'name': str,
            'age': int,
            'pets': [
                {
                    'name': str,
                    'kind': str
                }
            ],
            'parents': ([{'name': str}], int, None)
        }
        
        kid = {
            'name': "Bart Simpson",
            'age': 10,
            'pets': [
                {'name': "Santa's Little Helper", 'kind': "Dog"},
                {'name': "Snowball II", 'kind': "Cat"}
            ],
            'parents': [
                {'name': "Homer Simpson"},
                {'name': "Marge Simpson"}
            ]
        }
        
        self.assertTrue(validate(template, kid))

    
    def test_bad_dict_loud(self):
        template = {
            'name': str,
            'age': int,
            'pets': [
                {
                    'name': str,
                    'kind': str
                }
            ],
            'parents': ([{'name': str}], int, None)
        }

        bad_kid = {
            'name': "Nelson Muntz",
            'age': 12
        }

        with self.assertRaises(FailedValidationError):
            validate(template, bad_kid)  

    
    def test_bad_dict_quiet(self):
        template = {
            'name': str,
            'age': int,
            'pets': [
                {
                    'name': str,
                    'kind': str
                }
            ],
            'parents': ([{'name': str}], int, None)
        }
 
        bad_kid = {
            'name': "Nelson Muntz",
            'age': 12
        }

        self.assertFalse(validate(template, bad_kid, quiet=True))


    def test_optional_values(self):
        template = {
                'name': None,
                'age': int
                }

        valid = {'age': 2}

        self.assertTrue(validate(template, valid))
