import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def loading_data():
    #This function takes city as an input and loads the corresponding CSV file
    print('\nLet\'s explore some US bikeshare data!')
    print(' ')
    print('\nEnter the city you want to analyze the data for:')
    while True:
        print('Chicago\t New York City\t Washington')
        city = input('\nChoose from the city names mentioned above :  ')
        city = city.lower()
        if city in CITY_DATA.keys():
            print("\nValidated Entry\n")
            break    
        else: 
            print("\nThe entered input is wrong. Kindly check and enter again\n")
            continue
    print("\nYou have chosen {} as the city. Data and statistics will be computed for the same.".format(city))        
    print('-'*100)
    # Loads data for the specified city
    print('Loading the data from {}. Please wait....\n'.format(city))
    df = pd.read_csv(CITY_DATA[city])
    #Converting Start Time and End Time into datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    #Extracting from Start Time for data calculation
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month
    df['day_and_month'] = df["Start Time"].dt.day
    return df

def get_filter(df):
    #This function takes filter as an input and asks for additional data if required
    print('\nWould you like your data to be filtered? Choose from the options below : \n')
    while True: 
        filter = input("->Month    ->Day    ->Both   ->None  : ")
        filter = filter.lower()
        if filter == "month":
            print('\n The data is now being filtered by month\n' + ('-'*100) + '\nRequiring additional data....')
            print("\nChoose from the months mentioned below. Please type the full month name to avoid errors\n")
            while True:
                #Taking a month as an input
                month = input("January, February, March, April, May or June?  :  ")
                month = month.strip().lower()
                if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                else:
                    print("\nWrong input. Choose correctly from the mentioned options.\n")
            day,month_day=0,0
            break
        elif filter == "day":
            print('\n The data is now being filtered by the day of the week\n' + ('-'*100) + '\nRequiring additional data....')        
            print("\nEnter any day of the week. Spell correctly to avoid errors.")
            while True:
                #Taking a day as an input
                day = input("\nMonday Tuesday Wednesday Thursday Friday Saturday or Sunday : ")
                day = day.strip().lower()
                if day in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
                    break
                else:
                    print("\nInvalid entry. Check the spelling and re-enter")
            month,month_day=0,0
            break
        elif filter == "both":
            #Here the input is taken for a day in a particular month
            filter = 'day_and_month'
            print ('\n The data is now being filtered by month and day\n' + ('-'*100) + '\nRequiring additional data....')
            print("\nChoose from the months mentioned below. Please type the full month name to avoid errors\n")
            while True:
                month = input("January, February, March, April, May or June?  :  ")
                month = month.strip().lower()
                if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                else:
                    print("\nWrong input. Choose correctly from the mentioned options.\n")
            #Creating a list to store both values of month and day
            month_day = []
            month_day.append(month)
            months = {"january": 1, "february": 2, "march": 3, "april":4, "may": 5, "june":6}
            df = df[df["month"] == months[month]]
            max_day = df["day_and_month"].max()
            while True:
                print("\nEnter the day using a number.There are total of {}".format(max_day) + " days in the month you entered  :  ")
                try:
                    day = int(input())
                except:
                    print("Kindly enter a number as input.Characters are invalid")
                    continue
                if 1 <= day and day<= max_day:
                    month_day.append(day)
                    break
                else: 
                    print("\nWrong input. Entered number is higher than the number of days in the month.")
            break
        elif filter == "none":
            print('\n No filter is being applied to the data\n' + ('-'*100) + '\nNo additional data required....')
            month,day,month_day=0,0,0
            break
        else:
            print("\nYour input is invalid. Kindly check and re-enter")
    return df,filter,month,day,month_day    

def filter_data(df, f, month, d, md):
    #Filter by Month
    if f == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    #Filter by day of week
    if f == 'day_of_week':
        day_of_week = d
        df = df[df['day_of_week'] == day_of_week]

    #filter by both
    if f == "day_and_month":
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = md[0]
        month = months.index(month) + 1
        df = df[df['month']==month]
        day = md[1]
        df = df[df['day_and_month'] == day]
    print('Data has been successfully loaded. Calculating and displaying the statistics below.... \n')
    return df

def sample_data(df):
    #Displaying a sample of the data that is being used to compute the stats
    print('-'*100)
    print("\nDisplaying a sample of original data :\n")
    print(df.drop(['month','day_of_week','day_and_month'],axis=1).head(10))
    print('-'*100)
    print("\nDisplaying a sample of columns that are added after filtering :\n")
    print(df[['month','day_of_week','day_and_month']].tail(10))
    print('-'*100)

def time_stats(df,f):
    """Displays statistics on the most frequent times of travel."""

    print("Displaying statistics on the most frequent times of travel....")
    start_time = time.time()
    m = df.month.mode()[0] #mode with index 0 returns the most frequent value
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[m - 1]
    print("\nThe most common month for traveling is : ", common_month)
    print("The most common day of week is : ", df['day_of_week'].value_counts().idxmax())
    df['hour'] = df['Start Time'].dt.hour #API reference used
    print("The most common start hour is : ", df.hour.mode()[0])
    print("\nThis took %s seconds. " % (time.time() - start_time) + " Filter : {}".format(f))
    print('-'*100)

def station_stats(df,f):
    """Displays statistics on the most popular stations and trip."""

    print("Displaying statistics on the most popular stations and trip....")
    start_time = time.time()
    #idxmax() returns most frequent value
    start_station = df['Start Station'].value_counts().idxmax() 
    end_station = df['End Station'].value_counts().idxmax()
    print ("\nMost commonly used start station is : ", start_station)
    print("Most commonly used start station is : ", end_station)
    combo = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("Most frequent combination of start and end station is : \n\t", combo)
    print("\nThis took %s seconds. " % (time.time() - start_time) + " Filter : {}".format(f))
    print('-'*100)

def trip_duration_stats(df,f):
    """Displays statistics on the total and average trip duration."""

    print("Displaying statistics on the total and average trip duration....")
    start_time = time.time()
    df['Travel Time'] = df['End Time'] - df['Start Time']
    #sum() and mean() used here are built-in pandas method
    print("\nTotal traveling time calculated till June is : ", df['Travel Time'].sum())
    print("Average traveling time calculated till June is : ", df['Travel Time'].mean())
    print("\nThis took %s seconds. " % (time.time() - start_time) + " Filter : {}".format(f))
    print('-'*100)

def user_stats(df,f):
    """Displays statistics on bikeshare users."""

    print("Displays statistics on bikeshare users....")
    start_time = time.time()
    #value_counts() provides the total count of each value
    print('\nTypes of users and their count : \n')
    print(df['User Type'].value_counts())
    try:
        gender_data = df['Gender'].value_counts()
        print("\nGender of users and its count : \n")
        print(gender_data)
    except:
        print("\nNo Gender data in the source file.")
    #Getting Birth Year related data.
    try:
        earliest = df['Birth Year'].min()
        latest = df['Birth Year'].max()
        most_frequent= df['Birth Year'].mode()[0]
        print("\nThe earliest year of birth is : ", earliest)
        print("The latest year of birth is : ", latest)
        print ("The most frequent year of birth is : ", most_frequent)
    except:
        print("\nNo Birth related data in the source file.")
    print("\nThis took %s seconds. " % (time.time() - start_time) + " Filter : {}".format(f))
    print('-'*100)

def main():
    '''This main function is used to call all the important function that collects
        and computes the required data'''
    while True:
        # calling the functions that take inputs from the user 
        df = loading_data()
        df, filter, month, day, month_day = get_filter(df)
        #passing all the inputs to create a dataframe accordingly
        df = filter_data(df, filter, month, day, month_day)
        sample_data(df)
        # calling all the calculation functions
        time_stats(df,filter)
        station_stats(df,filter)
        trip_duration_stats(df,filter)
        user_stats(df,filter)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes': break
if __name__ == "__main__":
	main()
