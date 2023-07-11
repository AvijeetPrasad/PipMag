# import libraries related to querying links and downloading files from the web
from datetime import timedelta
import pandas as pd
from pipmag import file_utils as fu
from pipmag import la_palma_utils as lp
import re

# Print the years for which the La Palma Observatory has data at UiO
obs_years = lp.get_obs_years()

# Get the observing dates for all the years
obs_dates = lp.get_obs_dates(obs_years)
obs_dates_list = lp.get_obs_dates_list(obs_dates)

# print the first, last and total number of observing dates
print(f'first entry: {obs_dates_list[0]}\n'
      f'last entry : {obs_dates_list[-1]}\n'
      f'total observing dates: {len(obs_dates_list)}')

# get the latest file from the list of files in the data directory
latest_all_media_links_file = fu.get_latest_file('../data/all_media_links*')

# check if all_media_links.pkl exists then load the pickle file, otherwise get the links
if latest_all_media_links_file is None:
    video_links = lp.get_video_liks(obs_dates)  # get the video links, one for each observing date
    image_links = lp.get_image_links(obs_dates)  # get the image links, one for each observing date
    all_image_links = lp.get_all_links(image_links)  # get all the image links, one for each image
    all_video_links = lp.get_all_links(video_links)  # get all the video links, one for each video
    # print the number of video and image links and all the video and image links
    print(f'number of video links: {len(all_video_links)}\nnumber of image links: {len(all_image_links)}')
    print(f'video links: {len(all_video_links)}\nimage links: {len(all_image_links)}')
    all_media_links = all_image_links + all_video_links  # combine the image and video links
    all_media_links = sorted(all_media_links)  # sort the list of links
    # print the total number of media links
    print(f'total number of media links: {len(all_media_links)}')
    # save all the media links as a pickle file
    fu.save_pickle(all_media_links, '../data/' + lp.add_timestamp('all_media_links.pkl'))
else:
    # load the latest pickle file
    all_media_links = fu.load_pickle(latest_all_media_links_file)
    print(f'total number of media links: {len(all_media_links)}')

# get the date and time from the links and find the links that do not have date and time and save them as a list
date_time_from_all_media_links, date_time_not_found = lp.get_date_time_from_link_list(all_media_links)
# remove all the links that do not have a date and time from all_media_links
all_media_links_with_date_time = [link for link in all_media_links if link not in date_time_not_found]
# print the number of links that contain date and time and the number of links that do not contain date and time
print(f'number of links with date and time: {len(all_media_links_with_date_time)}\n'
      f'number of links without date and time: {len(date_time_not_found)}')
invalid_dates = lp.get_invalid_dates(date_time_from_all_media_links)
# remove the entries from date_time_from_all_media_links that are not in the correct format
date_time_from_all_media_links = [date for date in date_time_from_all_media_links if date not in invalid_dates]
# find the string pattern before the underscore in the invalid dates
# and search for the pattern in the links with date and time
# and save the links that contain the pattern in a list
invalid_dates_pattern = [re.search(r'(.+?)_', date).group(1) for date in invalid_dates]
# find the links that contain the pattern in invalid_dates_pattern and save them in a list
invalid_dates_links = [link for link in all_media_links_with_date_time
                       if any(pattern in link for pattern in invalid_dates_pattern)]

# convert the date and time to datetime format
date_time_from_all_media_links_datetime = lp.convert_to_datetime(date_time_from_all_media_links)
# get the unique date_time_from_all_media_links_datetime  values
unique_date_time_from_all_media_links_datetime = list(set(date_time_from_all_media_links_datetime))
# print the number of unique date_time_from_all_media_links_datetime values
print(f'number of unique date_time_from_all_media_links_datetime values: '
      f'{len(unique_date_time_from_all_media_links_datetime)}')
# create a dataframe with the date_time_from_all_media_links_datetime as the index and the all_media_links as the column
df = pd.DataFrame(all_media_links_with_date_time, index=date_time_from_all_media_links_datetime, columns=['links'])
# print first, last and total number of entries in the dataframe
print(f'first entry: {df.index[0]}\nlast entry : {df.index[-1]}\ntotal entries: {len(df.index)}')

# group the dataframe by the time index and combine the links into a list
df = df.groupby(df.index).agg({'links': lambda x: list(x)})
# print the first, last and total number of entries in the dataframe
print(f'first entry: {df.index[0]}\nlast entry : {df.index[-1]}\ntotal entries: {len(df.index)}')

# add a column called 'obs_id' and set it equal to the row number of the dataframe
# add the 'id' column
df['obs_id'] = range(0, len(df))
# set the index as 'obs_id' and add a column for the date and time
df['date_time'] = df.index
df = df.set_index('obs_id')
# add a column for the number of links in each row
df['num_links'] = df['links'].apply(lambda x: len(x))
# add columns for the year, month and day to the dataframe
df['year'] = df['date_time'].apply(lambda x: x.year)
df['month'] = df['date_time'].apply(lambda x: x.month)
df['day'] = df['date_time'].apply(lambda x: x.day)
# add a column for the time of day
df['time'] = df['date_time'].apply(lambda x: x.time())
# add a column called 'target' and set it equal to None
df['target'] = None
df['comments'] = None
df['polarimetry'] = None
instrument_keywords = {
    'CRISP': ['wb_6563', 'ha', 'Crisp', '6173', '8542', '6563', 'crisp'],
    'CHROMIS': ['Chromis', 'cak', '4846'],
    'IRIS': ['sji']
}
# apply the get_instrument_info function to the 'links' column of the dataframe
# and add the result to a new column called 'instruments'
df['instruments'] = df['links'].apply(lambda x: lp.get_instrument_info(x, instrument_keywords))
# apply the get_links_with_string function to the 'links' column of the dataframe with the strings 'mp4' and 'mov'
# and add the result to a new column called 'video_links'
df['video_links'] = df['links'].apply(lambda x: lp.get_links_with_string(x, ['mp4', 'mov']))
# apply the get_links_with_string function to the 'links' column of the dataframe with the strings 'jpg' and 'png'
# and add the result to a new column called 'image_links'
df['image_links'] = df['links'].apply(lambda x: lp.get_links_with_string(x, ['jpg', 'png']))
# pm.get_links_with_string(df.iloc[0]['links'], ['mp4','mov'])
# make the columns date-time, year, month, day, time, instruments, target, video_links, image_links, links, num_links
df = df[['date_time', 'year', 'month', 'day', 'time', 'instruments', 'target',
         'comments', 'video_links', 'image_links', 'links', 'num_links', 'polarimetry']]

# === Fix duplicate times === #

# Convert 'date_time' column to DateTime type
df['date_time'] = pd.to_datetime(df['date_time'])

# Sort the DataFrame by 'date_time'
sorted_df = df.sort_values('date_time')

# Define threshold for time difference
threshold = timedelta(seconds=60)

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
    'polarimetry': 'min'
})

# convert the 'date_time' column back
grouped_df['date_time'] = grouped_df['date_time'].apply(lambda x: x.to_pydatetime())

# print a summary of the dataframe
grouped_df.info()
# save the dataframe as a pickle file
grouped_df.to_pickle('../data/' + fu.add_timestamp('la_palma_obs_data.pkl'))
