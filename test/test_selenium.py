""" Tests the dash app works """
import unittest

from test.selenium_utils import open_dash

import src.constants as c

class TestApp(unittest.TestCase):
    """ Tests the dash app works """

    driver = open_dash()

    def test_title(self):
        """ Test that the app is able to load """
        self.assertEqual(c.names.TITLE, self.driver.title)



if __name__ == '__main__':
    unittest.main()
