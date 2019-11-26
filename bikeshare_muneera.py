import time
import pandas as pd



CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s show some US bikeshare data!')

    #Def function for user to input city
    while True:
        city = input('Which city would you like to check?\nChicago?\nNew York City?\nWashington?\n').lower()
        if city not in (CITY_DATA.keys()):
            print(f'Sorry, "{city.title()}" is not a proper city, please input "Chicago", "New York City", or "Washington".')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(f'Okay! Which month would you like to explore {city.title()}?\nUse "All" for no filter:\n').lower()
        if month not in months:
            print(f'Sorry, "{month}" is not a valid answer, please choose between\nJanuary, February, March, April, May, June, All (no filter)')
        else:
            break
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(f'Last step! Which day would you like to explore {city.title()} in {month.title()}?\nUse "All" for no filter:\n').lower()
        if day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print(f'Sorry, "{day}" is not a valid day of the week or "All", please choose between\nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All(No filter)')
        else:
            break

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = months.index(month)
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is :", df['month'].value_counts().idxmax())

    # display the most common day of week
    print("The most common day of week is :", df['day_of_week'].value_counts().idxmax())

    # display the most common start hour
    print("The most common start hour is :", df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station :", df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print("The most commonly used end station :", df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time :", df['Trip Duration'].sum())

    # display mean travel time
    print("Mean travel time :", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n", df['User Type'].value_counts())
    print()

    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print('Sorry, there is no Gender or Birth Year data for Washington.\n')
    else:
        print("Counts of gender:\n", df['Gender'].value_counts())
        print()
        print("The most earliest birth year:", df['Birth Year'].min())
        print("The most recent birth year:", df['Birth Year'].max())
        print("The most common birth year:", df['Birth Year'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """
    Display raw data based on user input
    """
    idx = 0
    user_input = input("\nWould you like to see rows of data we used to calculate previous stats?\n\
                       Please write 'yes' or 'no' \n").lower()
    while True:
        if user_input == 'no':
            break
        if user_input == 'yes':
            print(df[idx: idx + 5])
            idx = idx + 5
        user_input = input("\nWould you like to see 5 more rows of data?\n\
                           Please write 'yes' or 'no' \n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
