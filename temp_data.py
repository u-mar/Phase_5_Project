import psycopg2
import csv

class TemperatureDataLoader:
    def __init__(self, file_path, db_config, table_name):
        self.file_path = file_path
        self.db_config = db_config
        self.table_name = table_name

    def create_table_if_not_exists(self):
        # Establish a database connection
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()

        # Define the CREATE TABLE SQL statement
        create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                dt DATE,
                "AverageTemperature" NUMERIC,
                "AverageTemperatureUncertainty" NUMERIC,
                "City" TEXT,
                "Country" TEXT,
                "Latitude" TEXT,
                "Longitude" TEXT
            );
        '''

        # Execute the CREATE TABLE statement
        cursor.execute(create_table_sql)

        # Commit and close the connection
        connection.commit()
        cursor.close()
        connection.close()

    def insert_data_into_database(self):
        # Establish a database connection
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()

        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                # Define the INSERT INTO SQL statement
                insert_sql = f'''
                    INSERT INTO {self.table_name} (
                        dt, "AverageTemperature", "AverageTemperatureUncertainty",
                        "City", "Country", "Latitude", "Longitude"
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                '''

                # Iterate through the CSV rows and insert data
                for row in reader:
                    dt, avg_temp, temp_uncertainty, city, country, latitude, longitude = row
                    cursor.execute(insert_sql, (dt, avg_temp, temp_uncertainty, city, country, latitude, longitude))

            # Commit the changes to the database
            connection.commit()
        except Exception as e:
            print(f"Error processing and inserting data: {e}")
        finally:
            cursor.close()
            connection.close()

    def run(self):
        # Create the table if it doesn't exist
        self.create_table_if_not_exists()

        # Insert data into the database
        self.insert_data_into_database()

# Define your database connection details
db_config = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'omar',
    'database': 'bluesky'
}

# Define the local file path for the temperature data CSV
temperature_data_file = 'data/TemperaturesByMajor.csv'

# Define table name for temperature data
temperature_table_name = 'temperature_data'

# Create an instance of the TemperatureDataLoader class
temperature_data_loader = TemperatureDataLoader(temperature_data_file, db_config, temperature_table_name)

# Run the data loader to create the table and insert data
temperature_data_loader.run()
