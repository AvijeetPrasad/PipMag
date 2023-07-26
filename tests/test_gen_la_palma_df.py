import unittest
import pandas as pd
from datetime import datetime
import os

from pipmag.gen_la_palma_df import load_or_fetch_links, preprocess_links, generate_dataframe, fix_duplicate_times, add_existing_and_new_dataframes

class TestLaPalmaDataFrameFunctions(unittest.TestCase):
    def setUp(self):
        # setup code here if needed
        pass

    def test_load_or_fetch_links(self):
        # Call the function
        result = load_or_fetch_links()

        # Assert that the result is a list
        self.assertTrue(isinstance(result, list), "Expected a list.")

        # Assert that the list is not empty
        self.assertTrue(len(result) > 0, "Expected non-empty list.")

        # Assert that all elements in the list are strings
        self.assertTrue(all(isinstance(item, str) for item in result), "Expected list of strings.")

    def test_preprocess_links(self):
        # Define some test input
        test_input = ['http://tsih3.uio.no/lapalma/2013/2013-06-30//./wb_6563_2013-06-30T09:15:50_scans=0-2133_histoopt.mp4',
                    'http://invalid_link']

        # Call the function with the test input
        result_dates, result_links = preprocess_links(test_input)

        # Assert that the result is a list
        self.assertTrue(isinstance(result_dates, list), "Expected a list.")
        self.assertTrue(isinstance(result_links, list), "Expected a list.")

        # Assert that the lists are not empty
        self.assertTrue(len(result_dates) > 0, "Expected non-empty list.")
        self.assertTrue(len(result_links) > 0, "Expected non-empty list.")

        # Assert that all elements in the lists are strings
        self.assertTrue(all(isinstance(item, str) for item in result_dates), "Expected list of strings.")
        self.assertTrue(all(isinstance(item, str) for item in result_links), "Expected list of strings.")

        # Assert that the invalid link has been filtered out
        self.assertTrue('http://invalid_link' not in result_links, "Expected invalid link to be filtered out.")


    def test_generate_dataframe(self):
        # Define some test input
        test_dates = ['2013-06-30_09:15:50', '2013-06-30_09:15:50', '2013-06-30_09:15:50']
        test_links = [
            'http://tsih3.uio.no/lapalma/2013/2013-06-30//./wb_6563_2013-06-30T09:15:50_scans=0-2133_histoopt.mp4',
            'http://tsih3.uio.no/lapalma/2013/2013-06-30//./wb_6563_2013-06-30T09:15:50_scans=0-2133_minmax.mp4',
            'http://tsih3.uio.no/lapalma/2013/2013-06-30//halpha_SDO_8pan_2013-06-30_091550.mp4'
        ]

        # Call the function with the test input
        result_df = generate_dataframe(test_dates, test_links)

        # Assert that the result is a DataFrame
        self.assertTrue(isinstance(result_df, pd.DataFrame), "Expected a DataFrame.")

        # Assert that the DataFrame has the correct shape
        self.assertEqual(result_df.shape, (1, 13), "Expected DataFrame with 1 row and 13 columns.")

        # Assert that the DataFrame has the correct columns
        expected_columns = ['date_time', 'year', 'month', 'day', 'time', 'instruments', 'target', 'comments',
                            'video_links', 'image_links', 'links', 'num_links', 'polarimetry']
        self.assertEqual(list(result_df.columns), expected_columns, "Expected columns to match.")

        # Assert that the 'date_time' column is of datetime type
        self.assertEqual(result_df['date_time'].dtype, 'datetime64[ns]', "Expected 'date_time' to be datetime type.")

       # Assert that the first row has the correct values
        expected_first_row = {
            'date_time': pd.Timestamp(datetime.strptime(test_dates[0], "%Y-%m-%d_%H:%M:%S")),
            'year': 2013,
            'month': 6,
            'day': 30,
            'time': datetime.strptime(test_dates[0], "%Y-%m-%d_%H:%M:%S").time(),
            'instruments': ['CRISP'],
            'target': None,
            'comments': None,
            'video_links': test_links,
            'image_links': [],
            'links': test_links,
            'num_links': 3,
            'polarimetry': 'False'  # adjusted this line
        }
        first_row = result_df.loc[0].to_dict()
        for key, expected_value in expected_first_row.items():
            self.assertEqual(first_row[key], expected_value, f"Expected {key} to have value {expected_value}.")




    def test_fix_duplicate_times(self):
        # Call the function with some test input
        # result = fix_duplicate_times(test_input)
        # Perform some assertions based on what you expect
        # self.assertEqual(result, ...)
        # self.assertTrue(result, ...)
        pass

    def test_add_existing_and_new_dataframes(self):
        # Call the function with some test input
        # result = add_existing_and_new_dataframes(test_input)
        # Perform some assertions based on what you expect
        # self.assertEqual(result, ...)
        # self.assertTrue(result, ...)
        pass

class TestCSVDataFrame(unittest.TestCase):
    def setUp(self):
        if os.path.exists('data/la_palma_obs_data.csv'):
            self.df = pd.read_csv('data/la_palma_obs_data.csv')
        else:
            raise FileNotFoundError("CSV file not found.")
        
        self.df['date_time'] = pd.to_datetime(self.df['date_time'])
        columns_to_convert = ['links', 'video_links', 'image_links', 'instruments']
        for col in columns_to_convert:
            self.df[col] = self.df[col].apply(lambda x: x.split(';') if isinstance(x, str) else [])
        columns_to_convert = ['comments', 'polarimetry', 'target']
        for col in columns_to_convert:
            self.df[col] = self.df[col].apply(lambda x: None if pd.isna(x) else x)
        self.df['polarimetry'] = self.df['polarimetry'].apply(lambda x: str(x))

    def test_dataframe_columns(self):
        self.assertEqual(self.df['date_time'].dtype, 'datetime64[ns]')
        self.assertEqual(self.df['year'].dtype, 'int64')
        self.assertEqual(self.df['month'].dtype, 'int64')
        self.assertEqual(self.df['day'].dtype, 'int64')
        self.assertEqual(self.df['num_links'].dtype, 'int64')
        self.assertEqual(self.df['polarimetry'].dtype, 'object')
        self.assertEqual(self.df['time'].dtype, 'object')
        self.assertEqual(self.df['instruments'].dtype, 'object')
        self.assertEqual(self.df['target'].dtype, 'object')
        self.assertEqual(self.df['comments'].dtype, 'object')
        self.assertEqual(self.df['video_links'].dtype, 'object')
        self.assertEqual(self.df['image_links'].dtype, 'object')
        self.assertEqual(self.df['links'].dtype, 'object')

    def test_dataframe_values(self):
        self.assertTrue((self.df['year'] >= 2000).all())
        self.assertTrue((self.df['year'] <= datetime.now().year).all())
        self.assertTrue((self.df['month'] >= 1).all())
        self.assertTrue((self.df['month'] <= 12).all())
        self.assertTrue((self.df['day'] >= 1).all())
        self.assertTrue((self.df['day'] <= 31).all())
        self.assertTrue((self.df['num_links'] >= 0).all())
        self.assertTrue((self.df['polarimetry'].isin(['True', 'False'])).all())

if __name__ == '__main__':
    unittest.main()
