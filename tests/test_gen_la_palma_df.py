import unittest
import pandas as pd
from datetime import datetime
import os


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
