import unittest
import os
import pandas as pd
import tempfile
from pipmag.file_utils import read_and_format_csv, preprocess_and_save_dataframe
from pipmag.file_utils import read_and_format_csv_for_query


class TestReadAndFormatCSV(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory using the tempfile module
        self.temp_dir = tempfile.TemporaryDirectory()

        # Sample test data for demonstration
        self.sample_csv_data = """date_time,year,month,day,time,instruments,target,comments,video_links,image_links,links,num_links,polarimetry
        2013-06-30 09:15:50,2013,6,30,09:15:50,CRISP;IRIS,Spicules,,http://example.com/video,http://example.com/image,http://example.com/links,3,False
        """

        # Create a temporary CSV file within the temporary directory
        self.sample_csv_file = os.path.join(self.temp_dir.name, 'sample.csv')
        with open(self.sample_csv_file, "w") as f:
            f.write(self.sample_csv_data)

    def tearDown(self):
        # Cleanup the temporary directory
        self.temp_dir.cleanup()

    def test_file_not_found(self):
        self.assertEqual(read_and_format_csv("nonexistent.csv"), "Error: The specified file was not found.")
        
    def test_empty_file(self):
        empty_file_path = os.path.join(self.temp_dir.name, 'empty.csv')
        with open(empty_file_path, "w") as f:
            f.write("")
        self.assertEqual(read_and_format_csv(empty_file_path), "Error: The file is empty.")
    
    def test_incorrect_columns(self):
        self.assertEqual(read_and_format_csv(self.sample_csv_file, expected_columns=['nonexistent_column']), 
                         "Error: Missing expected columns. Expected: ['nonexistent_column'], Found: ['date_time', 'year', 'month', 'day', 'time', 'instruments', 'target', 'comments', 'video_links', 'image_links', 'links', 'num_links', 'polarimetry']")
        
    def test_correct_file(self):
        df = read_and_format_csv(self.sample_csv_file)
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertTrue(pd.to_datetime("2013-06-30 09:15:50") == df['date_time'][0])
        self.assertTrue(df['instruments'][0] == ['CRISP', 'IRIS'])
        self.assertTrue(df['polarimetry'][0] == 'False')


class TestPreprocessAndSaveDataFrame(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = {
            'target': ['active region', 'QS', 'sunspot', 'AR', 'Quiet sun'],
            'links': [['a'], ['b'], ['c'], ['d'], ['e']],
            'video_links': [['f'], ['g'], ['h'], ['i'], ['j']],
            'image_links': [['k'], ['l'], ['m'], ['n'], ['o']],
            'instruments': [['p'], ['q'], ['r'], ['s'], ['t']]
        }
        self.df = pd.DataFrame(self.sample_data)
        self.output_file = "test_output.csv"
        
    def test_preprocess_and_save_dataframe(self):
        preprocess_and_save_dataframe(self.df, self.output_file)
        
        # Read the saved CSV and check its content
        df_read = pd.read_csv(self.output_file)
        
        self.assertEqual(df_read['target'][0], 'Active Region')
        self.assertEqual(df_read['target'][1], 'Quiet Sun')
        self.assertEqual(df_read['target'][2], 'Sunspot')
        self.assertEqual(df_read['links'][0], 'a')
        
        # Clean up
        os.remove(self.output_file)

class TestReadAndFormatCSV(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a temporary file
        cls.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        
        # Sample data
        data = """date_time,year,month,day,time,instruments,target,comments,video_links,image_links,links,num_links,polarimetry
2022-07-01 09:46:53,2022,7,1,09:46:53,CRISP;   CHROMIS,"Active Region, Sunspot",AR13040,http://video.com,http://image.com,http://link.com,50,True
2022-07-01 10:46:53,2022,7,1,10:46:53,CRISP;   CHROMIS,,,"""
        
        # Write sample data to the temporary file and close it
        cls.temp_file.write(data)
        cls.temp_file.close()

    def test_read_and_format_csv_for_query(self):
        # Read and format the CSV file
        df = read_and_format_csv_for_query(self.temp_file.name)
        
        # Validate the DataFrame
        self.assertEqual(df.shape, (2, 13))  # Should have 2 rows and 13 columns
        self.assertEqual(df.loc[0, 'target'], 'Active Region, Sunspot')  # First row, 'target' column should be 'Active Region, Sunspot'
        self.assertEqual(df.loc[1, 'target'], 'None')  # Second row, 'target' column should be None

    @classmethod
    def tearDownClass(cls):
        # Delete the temporary file
        os.remove(cls.temp_file.name)

if __name__ == '__main__':
    unittest.main()
