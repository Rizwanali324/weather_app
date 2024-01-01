# Author: <Your name here>
# Student ID: <Your Student ID>

import sqlite3


# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.



'''
Satisfactory
'''
"""
def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        for row in results:
            print(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

    except sqlite3.OperationalError as ex:
        print(ex)
"""


def select_all_countries(connection):
    try:

        # Define the query
        query = "SELECT * FROM countries"

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [description[0] for description in cursor.description]

        # Iterate over the results and display the results
        for row in results:
            country_id, country_name, country_timezone = row
            print(f"Country Id: {country_id} -- Country Name: {country_name} -- Country Timezone: {country_timezone}")

    except sqlite3.OperationalError as ex:
        print(ex)


# call the function
#  >>select_all_countries(connection)
'''
def select_all_cities(connection):
    # TODO: Implement this function
    pass

Good
'''



def select_all_cities(connection):
    try:

        
        # Define the query
        query = "SELECT * FROM cities"

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

       # Check if there are any results
        if results:
            # Get the column names from the cursor description
            column_names = [description[0] for description in cursor.description]

          # Iterate over the results and display the results in a single line
        for row in results:
            city_details = ", ".join(f"{column_name}: {value}" for column_name, value in zip(column_names, row))
            print(f"City Details: {city_details}")

   
    except sqlite3.OperationalError as ex:
        print(ex)


#>>>>>>>>>>>>>>>#select_all_cities(connection)


"""
def average_annual_temperature(connection, city_id, year):
    # TODO: Implement this function
    pass


    """

def average_annual_temperature(connection, city_id, year):
    try:
        # Define the query to calculate the average annual temperature
        query = """
            SELECT AVG(mean_temp) as avg_temperature
            FROM daily_weather_entries
            WHERE city_id = ? AND strftime('%Y', date) = ?
        """

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        cursor.execute(query, (city_id, str(year)))

        # Fetch the result
        result = cursor.fetchone()

        # Print the result
        if result and result[0] is not None:
            print(f"Average Annual Temperature for City {city_id} in {year}: {result[0]:.2f} degrees Celsius")
        else:
            print(f"No data found for City {city_id} in {year}")

    except sqlite3.OperationalError as ex:
        print(ex)

#   >>>>>>>average_annual_temperature(connection,city_id=1,year=2022)


"""


def average_seven_day_precipitation(connection, city_id, start_date):
    # TODO: Implement this function
    pass
"""
def average_seven_day_precipitation(connection, city_id, start_date):
    try:
        # Define the query to calculate the average precipitation for a seven-day period
        query = """
            SELECT AVG(precipitation) as avg_precipitation
            FROM daily_weather_entries
            WHERE city_id = ? AND date BETWEEN ? AND date(?,'+6 days')
        """

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        cursor.execute(query, (city_id, start_date, start_date))

        # Fetch the result
        result = cursor.fetchone()

        # Print the result
        if result and result[0] is not None:
            print(f"Average Seven-Day Precipitation for City {city_id} starting from {start_date}: {result[0]:.2f} mm")
        else:
            print(f"No data found for City {city_id} starting from {start_date}")

    except sqlite3.OperationalError as ex:
        print(ex)

#   >>average_seven_day_precipitation(connection,city_id=2,start_date='2020-02-02')


"""
'''
Very good
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    # TODO: Implement this function
    pass
"""



def average_mean_temp_by_city(connection, date_from, date_to):
    try:
        # Define the query to calculate the average mean temperature for each city
        query = """
            SELECT cities.name as city_name, AVG(daily_weather_entries.mean_temp) as avg_mean_temperature
            FROM daily_weather_entries
            JOIN cities ON daily_weather_entries.city_id = cities.id
            WHERE date BETWEEN ? AND ?
            GROUP BY cities.id
        """

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        cursor.execute(query, (date_from, date_to))

        # Fetch the results
        results = cursor.fetchall()

        # Print the results
        if results:
            print("Average Mean Temperature by City:")
            for row in results:
                city_name, avg_mean_temperature = row
                print(f"{city_name}: {avg_mean_temperature:.2f} degrees Celsius")
        else:
            print(f"No data found for the specified date range")

    except sqlite3.OperationalError as ex:
        print(ex)


#>>average_mean_temp_by_city(connection,date_from='2020-02-02',date_to='2020-02-05')
"""
def average_annual_precipitation_by_country(connection, year):
    # TODO: Implement this function
    pass
"""



def average_annual_precipitation_by_country(connection, year):
    try:
        # Define the query to calculate the average annual precipitation for each country
        query = """
            SELECT countries.name as country_name, AVG(daily_weather_entries.precipitation) as avg_annual_precipitation
            FROM daily_weather_entries
            JOIN cities ON daily_weather_entries.city_id = cities.id
            JOIN countries ON cities.country_id = countries.id
            WHERE strftime('%Y', daily_weather_entries.date) = ?
            GROUP BY countries.id
        """

        # Get a cursor object from the database connection
        cursor = connection.cursor()

        # Execute the query via the cursor object
        cursor.execute(query, (str(year),))

        # Fetch the results
        results = cursor.fetchall()

        # Print the results
        if results:
            print("Average Annual Precipitation by Country:")
            for row in results:
                country_name, avg_annual_precipitation = row
                print(f"{country_name}: {avg_annual_precipitation:.2f} mm")
        else:
            print(f"No data found for the specified year")

    except sqlite3.OperationalError as ex:
        print(ex)



#>>>>>>>average_annual_precipitation_by_country(connection,year="2020")

"""
'''
Excellent

You have gone beyond the basic requirements for this aspect.



if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    # above, printing the results to the terminal.
    pass


    """

if __name__ == "__main__":
    """# Create a SQLite3 connection
    
   # Connect to the database
    connection = sqlite3.connect('db\db.db')
    print("Connected to the database successfully.")
    # Call the various functions and print the results
    select_all_countries(connection)
    select_all_cities(connection)
    average_annual_temperature(connection, city_id=1, year=2022)
    average_seven_day_precipitation(connection, city_id=2, start_date='2020-02-02')
    average_mean_temp_by_city(connection, date_from='2020-02-02', date_to='2020-02-05')
    average_annual_precipitation_by_country(connection, year="2020")

    # Close the connection
    connection.close()"""
