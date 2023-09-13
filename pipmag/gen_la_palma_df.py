import os
import pandas as pd
from datetime import timedelta
from pipmag import la_palma_utils as lp

# Constants
MEDIA_LINKS_FILE = 'data/all_media_links.csv'
LA_PALMA_OBS_DATA_FILE = 'data/la_palma_obs_data.csv'
TIME_DIFF_THRESHOLD_SECONDS = 60
INSTRUMENT_KEYWORDS = {
    'CRISP': ['wb_6563', 'ha', 'Crisp', '6173', '8542', '6563', 'crisp'],
    'CHROMIS': ['Chromis', 'cak', '4846'],
    'IRIS': ['sji']
}
POLARIMETRY_KEYWORDS = {
    'True': ['Bz+Bh', 'blos', 'Blos']
}

def load_or_fetch_links(reload=False):
    """
    Load media links from file if it exists; otherwise, fetch the links.
    """
    # Check if MEDIA_LINKS_FILE exists then load the file, otherwise get the links
    if os.path.isfile(MEDIA_LINKS_FILE) and not reload:
        links_df = pd.read_csv(MEDIA_LINKS_FILE)
        all_media_links = links_df['Links'].tolist()
    else:
        print('Fetching links from La Palma website...')
        # Fetch observation years and dates
        obs_years = lp.get_obs_years()
        obs_dates = lp.get_obs_dates(obs_years)

        # Get video and image links for each observation date
        video_links = lp.get_video_liks(obs_dates)
        image_links = lp.get_image_links(obs_dates)

        # Get all video and image links
        all_video_links = lp.get_all_links(video_links)
        all_image_links = lp.get_all_links(image_links)

        # Combine and sort all media links
        all_media_links = sorted(all_image_links + all_video_links)

        # Save media links to file
        links_df = pd.DataFrame(all_media_links, columns=['Links'])
        links_df.to_csv(MEDIA_LINKS_FILE, index=False)

    return all_media_links


def preprocess_links(all_media_links):
    """
    Preprocess media links to extract date and time, and filter out invalid dates.
    """
    # Get date and time from link list
    date_time_from_all_media_links, date_time_not_found = lp.get_date_time_from_link_list(all_media_links)

    # Filter out links without date and time
    all_media_links_with_date_time = [link for link in all_media_links if link not in date_time_not_found]

    # Filter out invalid dates
    invalid_dates = lp.get_invalid_dates(date_time_from_all_media_links)
    date_time_from_all_media_links = [date for date in date_time_from_all_media_links if date not in invalid_dates]

    return date_time_from_all_media_links, all_media_links_with_date_time


def generate_dataframe(date_time_from_all_media_links, all_media_links_with_date_time):
    """
    Generate DataFrame from preprocessed media links.
    """
    # Convert date and time to datetime format
    date_time_from_all_media_links_datetime = lp.convert_to_datetime(date_time_from_all_media_links)

    # Create DataFrame from media links with datetime index
    df = pd.DataFrame(all_media_links_with_date_time, index=date_time_from_all_media_links_datetime, columns=['links'])

    # Group links by datetime index
    df = df.groupby(df.index).agg({'links': lambda x: list(x)})
    df['obs_id'] = range(0, len(df))
    df['date_time'] = df.index
    df = df.set_index('obs_id')

    # Extract features from date and time
    df['num_links'] = df['links'].apply(lambda x: len(x))
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month
    df['day'] = df['date_time'].dt.day
    df['time'] = df['date_time'].dt.time
    df['target'] = None
    df['comments'] = None
    df['polarimetry'] = 'False'

    # Extract instrument info from links
    df['instruments'] = df['links'].apply(lambda x: lp.get_instrument_info(x, INSTRUMENT_KEYWORDS))
    df['polarimetry'] = df['links'].apply(lambda x: lp.get_instrument_info(x, POLARIMETRY_KEYWORDS, 'False'))
    df['video_links'] = df['links'].apply(lambda x: lp.get_links_with_string(x, ['mp4', 'mov']))
    df['image_links'] = df['links'].apply(lambda x: lp.get_links_with_string(x, ['jpg', 'png']))

    # Reorder columns
    df = df[['date_time', 'year', 'month', 'day', 'time', 'instruments', 'target', 'comments',
             'video_links', 'image_links', 'links', 'num_links', 'polarimetry']]

    return df


def fix_duplicate_times(df):
    """
    Fix duplicate times in DataFrame by grouping rows based on time proximity.
    """
    # Convert 'date_time' column to DateTime type and sort DataFrame by 'date_time'
    df['date_time'] = pd.to_datetime(df['date_time'])
    sorted_df = df.sort_values('date_time')

    # Define threshold for time difference
    threshold = timedelta(seconds=TIME_DIFF_THRESHOLD_SECONDS)

    # Group rows based on time proximity
    grouped_df = sorted_df.groupby((sorted_df['date_time'].diff() > threshold).cumsum()).agg({
        'date_time': 'first',
        'year': 'first',
        'month': 'first',
        'day': 'first',
        'time': 'first',
        'instruments': 'sum',
        'target': 'first',
        'comments': 'first',
        'video_links': 'sum',
        'image_links': 'sum',
        'links': 'sum',
        'num_links': 'sum',
        'polarimetry': lambda x: 'True' if any(x) else 'False'
    })

    # Fix duplicates in 'instruments' column
    grouped_df['instruments'] = grouped_df['instruments'].apply(lambda x: list(set(x)))

    # Convert 'date_time' column back to native Python datetime
    grouped_df['date_time'] = grouped_df['date_time'].apply(lambda x: x.to_pydatetime())

    return grouped_df

def add_existing_and_new_dataframes(new_df):
    """
    Add a potential new DataFrame to the old DataFrame file without losing any data.
    """
    # Load the existing CSV file as a dataframe
    existing_df = pd.read_csv(LA_PALMA_OBS_DATA_FILE)

    # Read the date_time column as datetime
    existing_df['date_time'] = pd.to_datetime(existing_df['date_time'])

    # List of columns to convert from strings to lists
    columns_to_convert = ['links', 'video_links', 'image_links', 'instruments']

    # Convert the strings in each column back to lists
    for col in columns_to_convert:
        existing_df[col] = existing_df[col].apply(lambda x: x.split(';') if isinstance(x, str) else [])

    # List of columns to convert from NaN to None
    columns_to_convert = ['comments', 'polarimetry', 'target']

    # Convert the NaNs in each column back to None
    for col in columns_to_convert:
        existing_df[col] = existing_df[col].apply(lambda x: None if pd.isna(x) else x)

    # Concatenate the existing dataframe and the new dataframe
    df3 = pd.concat([existing_df, new_df])
    df3.drop_duplicates(subset=['date_time'], inplace=True, keep='first')

    return df3

def main():
    """
    Main function to load or fetch links, preprocess links, generate DataFrame, and fix duplicate times.
    """
    all_media_links = load_or_fetch_links(reload=True)
    date_time_from_all_media_links, all_media_links_with_date_time = preprocess_links(all_media_links)
    df = generate_dataframe(date_time_from_all_media_links, all_media_links_with_date_time)
    grouped_df = fix_duplicate_times(df)
    grouped_df = add_existing_and_new_dataframes(grouped_df)

    # List of columns to convert from lists to strings
    columns_to_convert = ['links', 'video_links', 'image_links', 'instruments']
    for col in columns_to_convert:
        grouped_df[col] = grouped_df[col].apply(lambda x: ';'.join(x))

    # Save DataFrame to CSV file
    grouped_df.to_csv(LA_PALMA_OBS_DATA_FILE, index=False)
    print('Dataframe saved to {}'.format(LA_PALMA_OBS_DATA_FILE))


if __name__ == "__main__":
    main()
