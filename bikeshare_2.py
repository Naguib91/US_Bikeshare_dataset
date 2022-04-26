import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # validate the city input
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Invalid Input: City .. Please try again !!')
    # get user input for month (all, january, february, ... , june)
    # validate the month input
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = input('Which month? January, February, ... , June, or all.\n').lower()
        if month in months:
            break
        else:
            print('Invalid Input: Month')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    # validate the day input
    while True:
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']
        day = input('Which day?\n').lower()
        if day in days:
            break
        else:
            print('Invalid Input: Day')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    """Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter using month
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filter using day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: {}'.format(common_month))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: {}'.format(common_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(common_start_station))

    # display most commonly used end station
    common_destination = df['End Station'].mode()[0]
    print('The most common destination is: {}.'.format(common_destination))

    # display most frequent combination of start station and end station trip
    df['Trip Route'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip Route'].mode()[0]
    print('The most common route is from {}.'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Trip Duration'] = df['Trip Duration'].astype(int)
    total_travel_time = df['Trip Duration'].sum()
    print('The total trips took {} seconds.'.format(total_travel_time))

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('The average time per trip is around {} seconds.'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame())

    # Display counts of gender
    # check if 'Gender' & 'Birth Year' exist in the selected data frame
    if 'Gender' in df:
        print(df['Gender'].value_counts().to_frame())
    else:
        print('"Gender" data is not available in this data frame.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth is {}'.format(df['Birth Year'].min()))
        print('The most recent year of birth is {}'.format(df['Birth Year'].max()))
        print('The most common year of birth is {}'.format(df['Birth Year'].mode()[0]))
    else:
        print('"Birth Year" data is not available in this data frame, so we cannot calculate its related stats.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(city):
    """
    to give the users an option to see the raw data of the selected city
    returns 5 rows of the data at a time>
    """
    print('\nRaw Data is available to check ...\n')
    display_raw = input('Would you like to have a look on the raw data? Enter yes or no.\n').lower()

    #The first loop to tell the user what to do if he selected wrong input
    while display_raw not in ('yes','no'):
        print('That\'s invalid input, please enter either "yes" or "no"')
        display_raw = input('Would you like to have a look on the raw data?\n').lower()

    #The second loop to ask user if he selected yes, and needs to see more data
    while display_raw == 'yes':
        try:
            for data in pd.read_csv(CITY_DATA[city],chunksize=5):
                print(data)
                display_raw = input('Would you like to see another 5 rows of the raw data? Enter yes or no.\n').lower()
                if display_raw !='yes':
                    print('Thank You')
                    break
            break

        except KeyboardInterrupt:
            print('Thank You')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
