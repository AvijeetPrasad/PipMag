import unittest
import os
import time
from pipmag import pipmag  # import the module you're testing


class TestPipmag(unittest.TestCase):
    def test_add_timestamp(self):
        result = pipmag.add_timestamp('test.txt')
        self.assertTrue(result.startswith('test_'))
        self.assertTrue(result.endswith('.txt'))

    def test_get_latest_file(self):
        # Setup - Create some dummy files
        for i in range(5):
            with open(f'test_file{i}.txt', 'w') as f:
                f.write('Hello, World!')
            time.sleep(1)  # Ensure files have different timestamps

        latest_file = pipmag.get_latest_file('test_file*.txt')
        # We expect the last created file (test_file4.txt) to be the latest
        self.assertEqual(latest_file, 'test_file4.txt')

        # Teardown - Clean up dummy files
        for i in range(5):
            os.remove(f'test_file{i}.txt')
