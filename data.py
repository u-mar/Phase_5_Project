import requests
import psycopg2

class DataExtractor:
    def __init__(self, db_config,file_url, table_name, column_names):
        self.file_url = file_url
        self.db_config = db_config
        self.table_name = table_name
        self.column_names = column_names

    def download_file(self):
        response = requests.get(self.file_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download the file. Status code: {response.status_code}")

    def create_table_if_not_exists(self):
        # Connect to the database
        with psycopg2.connect(**self.db_config) as connection:
            with connection.cursor() as cursor:
                # Define the SQL statement to create the table if it doesn't exist
                create_table_sql = """
                    CREATE TABLE IF NOT EXISTS co2_data (
                        year INT,
                        month INT,
                        decimal FLOAT,
                        average FLOAT,
                        average_unc FLOAT,
                        trend FLOAT,
                        trend_unc FLOAT
                    )
                """
                cursor.execute(create_table_sql)
            
            # Commit the changes and close the cursor and connection
            connection.commit()

    def retrieve_existing_data(self):
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name};")
        existing_data = cursor.fetchall()
        cursor.close()
        connection.close()
        return existing_data

    def data_has_changed(self, new_data, existing_data):
        # Compare new_data with existing_data here
        # Implement your comparison logic, such as comparing specific fields or using a hash function
        # Return True if data has changed, False if it's the same
        # For simplicity, assume data has changed if the lengths of new and existing data are different
        return len(new_data) != len(existing_data)

    def insert_data_into_database(self, data):
        existing_data = self.retrieve_existing_data()

        if not self.data_has_changed(data, existing_data):
            print("Data has not changed. Skipping insertion.")
            return

        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()

        try:
            # Process and insert data into the database here
            data_lines = data.decode('utf-8').splitlines()
            data_started = False

            for line in data_lines:
                if not data_started:
                    if line.startswith("year,month,"):
                        data_started = True
                    continue
                values = line.split(',')
                # Construct the INSERT SQL statement
                insert_sql = f"INSERT INTO {self.table_name} ({', '.join(self.column_names)}) VALUES ({', '.join(['%s']*len(self.column_names))})"
                cursor.execute(insert_sql, values)

            connection.commit()

        except Exception as e:
            print(f"Error processing and inserting data: {e}")
        finally:
            cursor.close()
            connection.close()

    def run(self):
        self.create_table_if_not_exists()  # Create the table if it doesn't exist
        file_content = self.download_file()
        self.insert_data_into_database(file_content)

# Define your database connection details
db_config = {
    'host': 'localhost',
    'port': '5432',
    'user': 'postgres',
    'password': 'omar',
    'database': 'bluesky'
}

co2_file_url = 'https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.csv'

co2_table_name = 'co2_data'
co2_column_names = ['year', 'month', 'decimal', 'average', 'average_unc', 'trend', 'trend_unc']

co2_data_extractor = DataExtractor(co2_file_url, db_config, co2_table_name, co2_column_names)

co2_data_extractor.run()
