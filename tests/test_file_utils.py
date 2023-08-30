import unittest
import os
import pandas as pd
from pipmag.file_utils import read_and_format_csv

class TestReadAndFormatCSV(unittest.TestCase):

    def setUp(self):
        # Sample test data for demonstration
        self.sample_csv_data = """date_time,year,month,day,time,instruments,target,comments,video_links,image_links,links,num_links,polarimetry
        2013-06-30 09:15:50,2013,6,30,09:15:50,CRISP;IRIS,Spicules,,http://example.com/video,http://example.com/image,http://example.com/links,3,False
        """
        # Create a temporary CSV file for testing
        with open("/mnt/data/sample.csv", "w") as f:
            f.write(self.sample_csv_data)

    def tearDown(self):
        # Delete temporary files
        os.remove("/mnt/data/sample.csv")
        if os.path.exists("/mnt/data/empty.csv"):
            os.remove("/mnt/data/empty.csv")

    def test_file_not_found(self):
        self.assertEqual(read_and_format_csv("/mnt/data/nonexistent.csv"), "Error: The specified file was not found.")
        
    def test_empty_file(self):
        with open("/mnt/data/empty.csv", "w") as f:
            f.write("")
        self.assertEqual(read_and_format_csv("/mnt/data/empty.csv"), "Error: The file is empty.")
    
    def test_incorrect_columns(self):
        self.assertEqual(read_and_format_csv("/mnt/data/sample.csv", expected_columns=['nonexistent_column']), 
                         "Error: Missing one or more expected columns. Expected: ['nonexistent_column'], Found: ['date_time', 'year', 'month', 'day', 'time', 'instruments', 'target', 'comments', 'video_links', 'image_links', 'links', 'num_links', 'polarimetry']")
        
    def test_correct_file(self):
        df = read_and_format_csv("/mnt/data/sample.csv")
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertTrue(pd.to_datetime("2013-06-30 09:15:50") == df['date_time'][0])
        self.assertTrue(df['instruments'][0] == ['CRISP', 'IRIS'])
        self.assertTrue(df['polarimetry'][0] == 'False')
