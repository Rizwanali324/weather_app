import sqlite3
import matplotlib.pyplot as plt

import numpy as np
import plotly.graph_objects as go

   # Connect to the database
connection = sqlite3.connect('db\db.db')
print("Connected to the database successfully.")



def bar_chart_7_day_precipitation(connection, city_id, start_date, end_date):
    try:
        # Query the data
        query = """
            SELECT date, precipitation
            FROM daily_weather_entries
            WHERE city_id = ? AND date BETWEEN ? AND ?
        """

        #print(f"Executing query: {query}")

        cursor = connection.cursor()
        cursor.execute(query, (city_id, start_date, end_date))
        results = cursor.fetchall()


        
        # Print the values
        print("Date\t\t\tPrecipitation (mm)")
        for row in results:
            date, precipitation = row
            print(f"{date}\t\t{precipitation}")

        # Check if there are results before attempting to unpack
        if results:
            # Generate Bar Chart
            dates, precipitation = zip(*results)
            plt.figure(figsize=(12,4))
            plt.bar(dates, precipitation)
            plt.xlabel('Date')
            plt.ylabel('Precipitation (mm)')
            plt.title(f'7-Day Precipitation for City {city_id} ({start_date} to {end_date})')
            plt.show()
        else:
            print(f"No data found for the specified city, start date, and end date.")

    except Exception as e:
        print(f"An error occurred: {e}")


bar_chart_7_day_precipitation(connection,city_id=1,start_date='2022-02-05',end_date='2022-02-12')



def bar_chart_specified_period(connection, start_date, end_date, city_ids):
    try:
        # Create a Plotly figure
        fig = go.Figure()

        for city_id in city_ids:
            # Query the data for each city
            query = f"""
                SELECT date, precipitation
                FROM daily_weather_entries
                WHERE city_id = ? AND date BETWEEN ? AND ?
            """

            cursor = connection.cursor()
            cursor.execute(query, (city_id, start_date, end_date))
            results = cursor.fetchall()

            # Extract data
            dates, precipitation = zip(*results)

            # Add a bar trace for each city
            fig.add_trace(go.Bar(x=dates, y=precipitation, name=f'City {city_id}'))

        # Customize the layout with xaxis_rangeslider
        fig.update_layout(
            barmode='group',  # Use 'group' for side-by-side bars
            xaxis=dict(title='Date', rangeslider=dict(visible=True), type='date'),
            yaxis=dict(title='Precipitation (mm)'),
            title='Precipitation for Specified Period and Cities',
        )

        # Show the plot
        fig.show()

    except Exception as e:
        print(f"An error occurred: {e}")

bar_chart_specified_period(connection, start_date='2022-01-01', end_date='2022-12-31', city_ids=[1, 2])


def bar_chart_avg_yearly_precipitation_by_country(connection, year):
    try:
        # Query the data
        query = f"""
            SELECT countries.name, AVG(daily_weather_entries.precipitation) as avg_precipitation
            FROM daily_weather_entries
            JOIN cities ON daily_weather_entries.city_id = cities.id
            JOIN countries ON cities.country_id = countries.id
            WHERE strftime('%Y', daily_weather_entries.date) = ?
            GROUP BY countries.id
        """

        cursor = connection.cursor()
        cursor.execute(query, (str(year),))
        results = cursor.fetchall()

        # Extract data
        countries, avg_precipitation = zip(*results)

        # Generate Bar Chart with different colors
        colors = plt.cm.viridis(np.linspace(0, 1, len(countries)))  # Use Viridis colormap
        plt.bar(countries, avg_precipitation, color=colors)
        plt.xlabel('Country')
        plt.ylabel('Average Precipitation (mm)')
        plt.title(f'Average Yearly Precipitation by Country ({year})')
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")
bar_chart_avg_yearly_precipitation_by_country(connection, year=2020)



def grouped_bar_chart_weather_stats(connection, location_ids):
    try:
        # Query the data
        query = f"""
            SELECT
                city_id,
                AVG(mean_temp) as avg_temperature,
                MIN(min_temp) as min_temperature,
                MAX(max_temp) as max_temperature,
                AVG(precipitation) as avg_precipitation
            FROM daily_weather_entries
            WHERE city_id IN ({','.join(map(str, location_ids))})
            GROUP BY city_id
        """

        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Extract data
        locations = [row[0] for row in results]
        avg_temperature = [row[1] for row in results]
        min_temperature = [row[2] for row in results]
        max_temperature = [row[3] for row in results]
        avg_precipitation = [row[4] for row in results]
        
        plt.figure(figsize=(12, 4))

        # Set the width of the bars
        bar_width = 0.2
        r1 = np.arange(len(locations))
        r2 = [x + bar_width for x in r1]
        r3 = [x + bar_width for x in r2]
        r4 = [x + bar_width for x in r3]

        # Create grouped bar chart using Matplotlib
        plt.bar(r1, avg_temperature, color='yellow', width=bar_width, edgecolor='grey', label='Avg Temperature')
        plt.bar(r2, min_temperature, color='red', width=bar_width, edgecolor='grey', label='Min Temperature')
        plt.bar(r3, max_temperature, color='green', width=bar_width, edgecolor='grey', label='Max Temperature')
        plt.bar(r4, avg_precipitation, color='blue', width=bar_width, edgecolor='grey', label='Avg Precipitation')

        # Customize the layout
        plt.xlabel('Location')
        plt.ylabel('Values')
        plt.title('Weather Statistics for Selected Locations')
        plt.xticks([r + bar_width for r in range(len(locations))], locations)

        # Move the legend outside the graph
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # Show the plot
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

grouped_bar_chart_weather_stats(connection, location_ids=[1, 2, 3])



def multiline_chart_daily_temperature(connection, city_id, year, month):
    try:
        # Query the data for daily minimum and maximum temperature for the specified month
        query = f"""
            SELECT
                date,
                MIN(min_temp) as min_temperature,
                MAX(max_temp) as max_temperature
            FROM daily_weather_entries
            WHERE city_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
            GROUP BY date
        """

        cursor = connection.cursor()
        cursor.execute(query, (city_id, str(year), str(month).zfill(2)))
        results = cursor.fetchall()

        # Extract data
        dates = [row[0] for row in results]
        min_temperature = [row[1] for row in results]
        max_temperature = [row[2] for row in results]

        # Create multi-line chart using Matplotlib
        plt.figure(figsize=(10, 6))
        plt.plot(dates, min_temperature, label='Min Temperature', marker='o', linestyle='-', color='blue')
        plt.plot(dates, max_temperature, label='Max Temperature', marker='o', linestyle='-', color='red')

        # Customize the layout
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.title(f'Daily Minimum and Maximum Temperature for City {city_id} in {year}-{month}')
        plt.legend()
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

        # Show the plot
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

multiline_chart_daily_temperature(connection, city_id=1, year=2022, month=5)



def scatter_plot_avg_temperature_vs_rainfall(connection, country_id=None, city_ids=None):
    try:
        # Query the data for average temperature and rainfall for the specified country or cities
        if country_id is not None:
            if city_ids is not None:
                query = f"""
                    SELECT
                        AVG(mean_temp) as avg_temperature,
                        AVG(precipitation) as avg_rainfall
                    FROM daily_weather_entries
                    WHERE city_id IN ({','.join(['?']*len(city_ids))})
                """
                params = tuple(city_ids)
            else:
                query = f"""
                    SELECT
                        AVG(mean_temp) as avg_temperature,
                        AVG(precipitation) as avg_rainfall
                    FROM daily_weather_entries
                    JOIN cities ON daily_weather_entries.city_id = cities.id
                    JOIN countries ON cities.country_id = countries.id
                    WHERE country_id = ?
                """
                params = (country_id,)
        else:
            query = """
                SELECT
                    AVG(mean_temp) as avg_temperature,
                    AVG(precipitation) as avg_rainfall
                FROM daily_weather_entries
            """
            params = ()

        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()

        # Extract data
        avg_temperature = result[0]
        avg_rainfall = result[1]

        # Create scatter plot using Matplotlib
        plt.figure(figsize=(12, 4))
        plt.scatter(avg_rainfall, avg_temperature, color='blue', marker='o')

        # Customize the layout
        plt.xlabel('Average Rainfall (mm)')
        plt.ylabel('Average Temperature (°C)')
        if country_id is not None:
            if city_ids is not None:
                plt.title(f'Scatter Plot for Average Temperature vs. Rainfall in Selected Cities ({", ".join(map(str, city_ids))})')
            else:
                plt.title(f'Scatter Plot for Average Temperature vs. Rainfall in Country {country_id}')
        else:
            plt.title('Scatter Plot for Average Temperature vs. Rainfall (All Countries)')
        plt.grid(True)

        # Show the plot
        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

scatter_plot_avg_temperature_vs_rainfall(connection, country_id=1, city_ids=[1, 2, 3])
scatter_plot_avg_temperature_vs_rainfall(connection, country_id=1)  # For all cities in the country
scatter_plot_avg_temperature_vs_rainfall(connection)  # For all countries and cities
connection.close()
