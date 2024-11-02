# Programmer: Amrit Bhaganagare 12619462 and Venkata Dheeraj Reddy Busireddy 12576469
# Class: CS 5300
# parser.py

import csv

def parse_csv(csv_file_location: str) -> tuple[list[str], list[tuple]]:
    """
    This function parses a CSV file and returns a tuple containing the column headers and the data.

    Args:
        csv_file_location (str): The location of the CSV file.

    Returns:
        tuple[list[str], list[tuple]]: A tuple containing the column headers and the data.
    """
    column_headers = []
    data = []

    try:
        with open(csv_file_location, 'r') as file:
            csv_reader = csv.reader(file)
            column_headers = next(csv_reader)  # Read the column headers
            for row in csv_reader:
                data.append(tuple(row))  # Read the data and convert each row to a tuple
    except FileNotFoundError:
        print(f"Error: The file {csv_file_location} was not found.")
    except csv.Error as e:
        print(f"Error: An error occurred while reading the CSV file: {e}")

    return column_headers, data