import psycopg2
import csv

class TemperatureDataLoader:
    def __init__(self, file_path, db_config, table_name):
        self.file_path = file_path
        self.db_config = db_config
        self.table_name = table_name

    def create_table_if_not_exists(self):
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                dt DATE,
                "AverageTemperature" NUMERIC,
                "AverageTemperatureUncertainty" NUMERIC,
                "City" TEXT,
                "Country" TEXT,
                "Latitude" TEXT,
                "Longitude" TEXT
            );
        ''')
        connection.commit()
        cursor.close()
        connection.close()

    def insert_data_into_database(self):
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()

        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    # Ensure that data types match the table schema
                    dt, avg_temp, temp_uncertainty, city, country, latitude, longitude = row
                    insert_sql = f'''
                        INSERT INTO {self.table_name} (
                            dt, "AverageTemperature", "AverageTemperatureUncertainty",
                            "City", "Country", "Latitude", "Longitude"
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    '''
                    cursor.execute(insert_sql, (dt, avg_temp, temp_uncertainty, city, country, latitude, longitude))

            connection.commit()
        except Exception as e:
            print(f"Error processing and inserting data: {e}")
        finally:
            cursor.close()
            connection.close()

    def run(self):
        self.create_table_if_not_exists()  # Create the table if it doesn't exist
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