import pandas as pd
from IPython.display import display, clear_output, Video
import ipywidgets as widgets
from pipmag.ads_utils import ADS_Search
import os

class MovieSelector:
    '''Class to create a widget to select a movie from a list of movies'''

    def __init__(self, df):
        self.df = df

    def get_links(self, date_time):
        return self.df[self.df['date_time'] == date_time]['video_links'].values[0]

    def create_widget(self):
        # Create a dropdown widget for the date_time column
        self.date_time_dropdown = widgets.Dropdown(
            options=self.df['date_time'], description='Date Time:')

        # Create a dropdown widget for the movie links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Movie Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        # Function to update the links dropdown based on the selected date_time
        def update_links(change):
            date_time = change.new
            links = self.get_links(date_time)
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new

        # Register the function to be called when the date_time dropdown value changes
        self.date_time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Display the dropdown widgets and the output widget
        display(self.date_time_dropdown)
        display(self.links_dropdown)

        def display_selected_link_button(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link))

        display_button = widgets.Button(description='Show')
        display_button.on_click(display_selected_link_button)
        display(display_button)
        display(self.output)


class VideoSelector:
    def __init__(self, df):
        self.df = df

    def create_widget(self):
        # Create a dropdown widget for the year column
        self.year_dropdown = widgets.Dropdown(
            options=self.df['year'].unique(), description='Year:')

        # Create a dropdown widget for the month column
        self.month_dropdown = widgets.Dropdown(
            options=[], description='Month:')

        # Create a dropdown widget for the day column
        self.day_dropdown = widgets.Dropdown(options=[], description='Day:')

        # Create a dropdown widget for the time column
        self.time_dropdown = widgets.Dropdown(options=[], description='Time:')

        # Create a dropdown widget for the links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        # Function to update the month dropdown based on the selected year
        def update_months(change):
            year = change.new
            months = self.df[self.df['year'] == year]['month'].unique()
            self.month_dropdown.options = months

        # Function to update the day dropdown based on the selected month and year
        def update_days(change):
            year = self.year_dropdown.value
            month = change.new
            days = self.df[(self.df['year'] == year) & (
                self.df['month'] == month)]['day'].unique()
            self.day_dropdown.options = days

        # Function to update the time dropdown based on the selected day, month, and year
        def update_time(change):
            year = self.year_dropdown.value
            month = self.month_dropdown.value
            day = change.new
            time = self.df[(self.df['year'] == year) & (
                self.df['month'] == month) & (self.df['day'] == day)]['time'].unique()
            self.time_dropdown.options = time

        # Function to update the links dropdown based on the selected time
        def update_links(change):
            time = change.new
            links = list(self.df[self.df['time'] == time]
                         ['video_links'].values[0])
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new
            self.matches = self.df[self.df['video_links'].apply(
                lambda x: self.selected_link in x)]
            self.selected_index = self.matches.index[0]

        # Function to display the selected link when the display button is pressed
        def display_selected_link(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link,
                        html_attributes='controls autoplay loop'))
                # print("Selected link index:", self.selected_index)
                display(widgets.HTML(
                    f"<h3><b>Index:</b> {self.selected_index}</h3>"))

        # Register the functions to be called when the year, month, and day dropdown values change
        self.year_dropdown.observe(update_months, names='value')
        self.month_dropdown.observe(update_days, names='value')
        self.day_dropdown.observe(update_time, names='value')

        # Register the function to be called when the time dropdown value changes
        self.time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Create a button widget to display the selected link
        self.display_button = widgets.Button(description='Show')
        self.display_button.on_click(display_selected_link)

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')
        # Display the dropdown widgets, the button, and the output widget
        display(self.year_dropdown)
        display(self.month_dropdown)
        display(self.day_dropdown)
        display(self.time_dropdown)
        display(self.links_dropdown)
        display(self.display_button)
        display(self.output)


class DataUpdater:
    def __init__(self, df, column_names):
        self.df = df
        self.column_names = column_names
        self.index_text = widgets.Text(description='Index:')
        self.value_texts = {}
        for column_name in self.column_names:
            self.value_texts[column_name] = widgets.Text(
                description=f'{column_name}:')
        self.update_button = widgets.Button(description='Update')
        self.output = widgets.Output()

        self.update_button.on_click(self.update_values)
        self.index_text.observe(self.display_existing_values, names='value')

    def update_values(self, b):
        index = int(self.index_text.value)
        for column_name in self.column_names:
            value = self.value_texts[column_name].value
            if isinstance(self.df.at[index, column_name], list):
                self.df.at[index, column_name] = value.split(',')
            else:
                self.df.at[index, column_name] = value
        with self.output:
            clear_output()
            display(widgets.HTML(
                f"<b>{', '.join(self.column_names)} updated for index {index}</b>"))

    def display_existing_values(self, change):
        if self.index_text.value:
            index = int(self.index_text.value)
            for column_name in self.column_names:
                existing_value = self.df.at[index, column_name]
                if isinstance(existing_value, list):
                    self.value_texts[column_name].value = ', '.join(
                        existing_value)
                else:
                    self.value_texts[column_name].value = existing_value if pd.notna(
                        existing_value) else ""

    def display(self):
        display(self.index_text)
        for column_name in self.column_names:
            display(self.value_texts[column_name])
        display(self.update_button)
        display(self.output)


class VideoSelector2:
    def __init__(self, df, column_names):
        self.df = df
        self.column_names = column_names

    def create_widget(self):
        # Create a dropdown widget for the year column
        self.year_dropdown = widgets.Dropdown(
            options=self.df['year'].unique(), description='Year:')

        # Create a dropdown widget for the month column
        self.month_dropdown = widgets.Dropdown(
            options=[], description='Month:')

        # Create a dropdown widget for the day column
        self.day_dropdown = widgets.Dropdown(options=[], description='Day:')

        # Create a dropdown widget for the time column
        self.time_dropdown = widgets.Dropdown(options=[], description='Time:')

        # Create a dropdown widget for the links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        self.value_texts = {}
        for column_name in self.column_names:
            self.value_texts[column_name] = widgets.Text(
                description=f'{column_name}:')
        self.update_button = widgets.Button(description='Update')

        # Function to update the month dropdown based on the selected year
        def update_months(change):
            year = change.new
            months = self.df[self.df['year'] == year]['month'].unique()
            self.month_dropdown.options = months

        # Function to update the day dropdown based on the selected month and year
        def update_days(change):
            year = self.year_dropdown.value
            month = change.new
            days = self.df[(self.df['year'] == year) & (
                self.df['month'] == month)]['day'].unique()
            self.day_dropdown.options = days

        # Function to update the time dropdown based on the selected day, month, and year
        def update_time(change):
            year = self.year_dropdown.value
            month = self.month_dropdown.value
            day = change.new
            time = self.df[(self.df['year'] == year) & (
                self.df['month'] == month) & (self.df['day'] == day)]['time'].unique()
            self.time_dropdown.options = time

        # Function to update the links dropdown based on the selected time
        def update_links(change):
            time = change.new
            links = list(self.df[self.df['time'] == time]
                         ['video_links'].values[0])
            # Create a list of the link names (without the full path)
            options = [os.path.basename(link) for link in links]
            # Store the full path of the links in a variable
            self.links_full_name = links
            self.links_dropdown.options = options

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            # Get the index of the selected link
            index = self.links_dropdown.options.index(change.new)
            # Get the full path of the selected link
            self.selected_link = self.links_full_name[index]

            self.matches = self.df[self.df['video_links'].apply(
                lambda x: self.selected_link in x)]
            self.selected_index = self.matches.index[0]

        # Function to display the selected link when the display button is pressed
        def display_selected_link(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link,
                        html_attributes='controls autoplay loop'))
                # print("Selected link index:", self.selected_index)
                display(widgets.HTML(
                    f"<h3><b>Index:</b> {self.selected_index}</h3>"))

        # Function to update the index dropdown based on the selected time

        def update_values(b):
            index = int(self.selected_index)
            for column_name in self.column_names:
                value = self.value_texts[column_name].value
                if isinstance(self.df.at[index, column_name], list):
                    self.df.at[index, column_name] = value.split(',')
                else:
                    self.df.at[index, column_name] = value
            with self.output:
                clear_output()
                display(widgets.HTML(
                    f"<b>{', '.join(self.column_names)} updated for index {index}</b>"))

        def display_existing_values(change):
            if self.selected_index:
                index = int(self.selected_index)
                for column_name in self.column_names:
                    existing_value = self.df.at[index, column_name]
                    if isinstance(existing_value, list):
                        self.value_texts[column_name].value = ', '.join(
                            existing_value)
                    else:
                        self.value_texts[column_name].value = existing_value if pd.notna(
                            existing_value) else ""

        # Register the functions to be called when the year, month, and day dropdown values change
        self.year_dropdown.observe(update_months, names='value')
        self.month_dropdown.observe(update_days, names='value')
        self.day_dropdown.observe(update_time, names='value')

        # Register the function to be called when the time dropdown value changes
        self.time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Create a button widget to display the selected link
        self.display_button = widgets.Button(description='Show')
        self.display_button.on_click(display_selected_link)
        # Create button to update values
        self.update_button = widgets.Button(description='Update')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')
        self.links_dropdown.observe(display_existing_values, names='value')

        # Display the dropdown widgets, the button, and the output widget
        display(self.year_dropdown)
        display(self.month_dropdown)
        display(self.day_dropdown)
        display(self.time_dropdown)
        display(self.links_dropdown)
        display(self.display_button)

        display(self.output)
        # Assign the function to be triggered when update_button is clicked
        self.update_button.on_click(update_values)

        # Display the button
        display(self.update_button)

        # Details at the bottom of the video
        for column_name in self.column_names:
            display(self.value_texts[column_name])
        display(self.update_button)

class VideoSelector3:
    def __init__(self, df, column_names):
        self.df = df
        self.column_names = column_names

        # Adds a search of papers according to the selected day
        self.ads = ADS_Search(df)

    def create_widget(self):
        # Create a dropdown widget for the year column
        self.year_dropdown = widgets.Dropdown(
            options=self.df['year'].unique(), description='Year:')

        # Create a dropdown widget for the month column
        self.month_dropdown = widgets.Dropdown(
            options=[], description='Month:')

        # Create a dropdown widget for the day column
        self.day_dropdown = widgets.Dropdown(options=[], description='Day:')

        # Create a dropdown widget for the time column
        self.time_dropdown = widgets.Dropdown(options=[], description='Time:')

        # Create a dropdown widget for the links column
        self.links_dropdown = widgets.Dropdown(
            options=[], description='Links:')

        # Create a variable to store the selected link
        self.selected_link = ''

        # Create an output widget to display the selected link
        self.output = widgets.Output()

        # Create a text field to display the properties of the selected observations
        self.value_texts = {}
        for column_name in self.column_names:
            self.value_texts[column_name] = widgets.Text(
                description=f'{column_name}:')
        self.update_button = widgets.Button(description='Update')

        # Function to update the month dropdown based on the selected year
        def update_months(change):
            year = change.new
            months = self.df[self.df['year'] == year]['month'].unique()
            self.month_dropdown.options = months

        # Function to update the day dropdown based on the selected month and year
        def update_days(change):
            year = self.year_dropdown.value
            month = change.new
            days = self.df[(self.df['year'] == year) & (
                self.df['month'] == month)]['day'].unique()
            self.day_dropdown.options = days

        # Function to update the time dropdown based on the selected day, month, and year
        def update_time(change):
            year = self.year_dropdown.value
            month = self.month_dropdown.value
            day = change.new
            time = self.df[(self.df['year'] == year) & (
                self.df['month'] == month) & (self.df['day'] == day)]['time'].unique()
            self.time_dropdown.options = time

        # Function to update the links dropdown based on the selected time
        def update_links(change):
            time = change.new
            links = list(self.df[self.df['time'] == time]
                         ['video_links'].values[0])
            self.links_dropdown.options = links

        # Function to update the selected link when the links dropdown value changes
        def links_value_changed(change):
            self.selected_link = change.new
            self.matches = self.df[self.df['video_links'].apply(
                lambda x: self.selected_link in x)]
            self.selected_index = self.matches.index[0]

        # Function to display the selected link when the display button is pressed

        def display_selected_link(b):
            with self.output:
                clear_output()
                display(Video(self.selected_link,
                        html_attributes='controls autoplay loop'))
                # print("Selected link index:", self.selected_index)

                # Display the ADS results
                self.ads.get_results(self.selected_index, pretty_print=True)

                display(widgets.HTML(
                    f"<h3><b>Index:</b> {self.selected_index}</h3>"))

        # Function to update the index dropdown based on the selected time
        def update_values(b):
            index = int(self.selected_index)
            for column_name in self.column_names:
                value = self.value_texts[column_name].value
                if isinstance(self.df.at[index, column_name], list):
                    self.df.at[index, column_name] = value.split(',')
                else:
                    self.df.at[index, column_name] = value
            with self.output:
                clear_output()
                display(widgets.HTML(
                    f"<b>{', '.join(self.column_names)} updated for index {index}</b>"))

        def display_existing_values(change):

            if self.selected_index:
                index = int(self.selected_index)
                for column_name in self.column_names:
                    existing_value = self.df.at[index, column_name]
                    if isinstance(existing_value, list):
                        self.value_texts[column_name].value = ', '.join(
                            existing_value)
                    else:
                        self.value_texts[column_name].value = existing_value if pd.notna(
                            existing_value) else ""

        # Register the functions to be called when the year, month, and day dropdown values change
        self.year_dropdown.observe(update_months, names='value')
        self.month_dropdown.observe(update_days, names='value')
        self.day_dropdown.observe(update_time, names='value')

        # Register the function to be called when the time dropdown value changes
        self.time_dropdown.observe(update_links, names='value')

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')

        # Create a button widget to display the selected link
        self.display_button = widgets.Button(description='Show')
        self.display_button.on_click(display_selected_link)

        # Register the function to be called when the links dropdown value changes
        self.links_dropdown.observe(links_value_changed, names='value')
        self.links_dropdown.observe(display_existing_values, names='value')

        # Display the dropdown widgets, the button, and the output widget
        display(self.year_dropdown)
        display(self.month_dropdown)
        display(self.day_dropdown)
        display(self.time_dropdown)
        display(self.links_dropdown)
        display(self.display_button)

        # Display the video
        display(self.output)

        # Details at the bottom of the video
        for column_name in self.column_names:
            display(self.value_texts[column_name])
        display(self.update_button)


class Query: 
    def __init__(self, df): 
        self.df = df 

    def create_widget(self): 

        # Create a dropdown widget for the instruments column (allows for several instruments to be selected)
        self.instrument_dropdown = widgets.SelectMultiple(
            options=self.df['instruments'].str.split(';').explode().str.strip().unique(),
            description='Instruments:',
            layout=widgets.Layout(width='300px')
            # layout=widgets.Layout(width='300px', description_width='300px'), 
            # HBox = widgets.HBox([widgets.Label('Select Instruments:'), self.instrument_dropdown])
        )

        self.start_date_dropdown = widgets.DatePicker(description='Start Date:', continuous_update=False)
        self.end_date_dropdown = widgets.DatePicker(description='End Date:', continuous_update=False)
        self.start_time_dropdown = widgets.Text(description='Start Time:', value='00:00')
        self.end_time_dropdown = widgets.Text(description='End Time:', value='23:59')

        # Create a dropdown widget for target selection
        self.target_dropdown = widgets.Dropdown(
            options=self.df['target'].str.split(',').explode().str.strip().unique(),
            description='Select Target:',
            layout=widgets.Layout(width='200px', description_width='300px')
        )

        # Function to filter available dates based on selected instruments, start date, end date, start time, and end time
        def filter_dates(instruments, start_date, end_date, start_time, end_time):
            df_filtered = self.df
    
            if instruments:
                df_filtered = df_filtered[df_filtered['instruments'].apply(lambda x: any(item in instruments for item in x.split(';')))]
            if start_date:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['date_time']).dt.date >= pd.to_datetime(start_date).date()]
            if end_date:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['date_time']).dt.date <= pd.to_datetime(end_date).date()]
            if start_time:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['time']).dt.time >= pd.to_datetime(start_time).time()]
            if end_time:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['time']).dt.time <= pd.to_datetime(end_time).time()]
            return df_filtered['time'].dropna().unique()

        # Function to filter available targets based on selected instruments, start date, end date, start time, and end time
        def filter_targets(selected_instruments, start_date, end_date, start_time, end_time):
            df_filtered = self.df
            if selected_instruments:
                df_filtered = df_filtered[df_filtered['instruments'].apply(lambda x: any(item in selected_instruments for item in x.split(';')))]
            if start_date:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['date_time']).dt.date >= pd.to_datetime(start_date).date()]
            if end_date:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['date_time']).dt.date <= pd.to_datetime(end_date).date()]
            if start_time:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['time']).dt.time >= pd.to_datetime(start_time).time()]
            if end_time:
                df_filtered = df_filtered[pd.to_datetime(df_filtered['time']).dt.time <= pd.to_datetime(end_time).time()]
            return df_filtered['target'].str.split(',').explode().str.strip().dropna().unique()
            # return df_filtered['target'].apply(lambda x: any(item in selected_instruments for item in x.split(';')))

        # Function to update the filtered dates and targets based on instrument, start date, end date, start time, and end time selection
        def update_date_and_target(change):
            selected_instruments = self.instrument_dropdown.value
            selected_start_date  = self.start_date_dropdown.value
            selected_end_date    = self.end_date_dropdown.value
            selected_start_time  = self.start_time_dropdown.value
            selected_end_time    = self.end_time_dropdown.value
            
            # filtered_dates = filter_dates(selected_instruments, selected_start_date, selected_end_date, selected_start_time, selected_end_time)            
            filtered_targets = filter_targets(selected_instruments, selected_start_date, selected_end_date, selected_start_time, selected_end_time)
            self.target_dropdown.options = filtered_targets

            # Apply filters and display the resulting DataFrame
            filtered_df = self.df
            if selected_instruments:
                filtered_df = filtered_df[filtered_df['instruments'].apply(lambda x: any(item in selected_instruments for item in x.split(';')))]
            if selected_start_date:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['date_time']).dt.date >= pd.to_datetime(selected_start_date).date()]
            if selected_end_date:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['date_time']).dt.date <= pd.to_datetime(selected_end_date).date()]
            if selected_start_time:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['time']).dt.time >= pd.to_datetime(selected_start_time).time()]
            if selected_end_time:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['time']).dt.time <= pd.to_datetime(selected_end_time).time()]
            # if selected_target: 
                # filtered_df = filtered_df[filtered_df['target'].apply(lambda x: any(item in selected_target for item in x.split(';')))]

            # filtered_targets = filter_targets(selected_instruments, selected_start_date, selected_end_date, selected_start_time, selected_end_time)
            # self.target_dropdown.options = filtered_targets

            # Display the resulting DataFrame
            with output:
                clear_output(wait=True)
                display(filtered_df)
        
        # Attach the update_date_and_target function to the dropdowns' value change event
        self.instrument_dropdown.observe(update_date_and_target, names='value')
        self.start_date_dropdown.observe(update_date_and_target, names='value')
        self.end_date_dropdown.observe(update_date_and_target, names='value')
        self.start_time_dropdown.observe(update_date_and_target, names='value')
        self.end_time_dropdown.observe(update_date_and_target, names='value')
        self.target_dropdown.observe(update_date_and_target, names='value')

        # Create an output widget to display the resulting DataFrame
        output = widgets.Output()

        # Display the instrument, start date, end date, start time, end time, target widgets, and output widget
        display(self.instrument_dropdown)
        display(self.start_date_dropdown)
        display(self.end_date_dropdown)
        display(self.start_time_dropdown)
        display(self.end_time_dropdown)
        display(self.target_dropdown)
        display(output)
