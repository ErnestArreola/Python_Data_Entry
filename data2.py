import tkinter as tk
from tkinter import filedialog
import pandas as pd
import usaddress

# Function to browse and select a file
def browse_file():
    # Set up the Tkinter root window (it won't be shown shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open the file dialog and get the file path
    file_path = filedialog.askopenfilename(
        title="Select a file", 
        filetypes=(("Excel Files", "*.xlsx;*.xls"), ("All Files", "*.*"))
    )

    # Return the file path as a string
    return file_path

# Function to format the parsed address into a readable string
def format_address(parsed_address):
    try:
        # Extract components from the parsed address dictionary
        address_number = parsed_address.get('AddressNumber', '')
        street_name = parsed_address.get('StreetName', '')
        street_type = parsed_address.get('StreetNamePostType', '')  # Street type (e.g., St, Ave, Rd)
        street_direction = parsed_address.get('StreetNamePreDirectional', '')  # Street direction (e.g., N, S, E, W)
        street_post_direction = parsed_address.get('StreetNamePostDirectional', '')  # Street post-directional (e.g., NW, SE)
        occupancy_type = parsed_address.get('OccupancyType', '')
        occupancy_id = parsed_address.get('OccupancyIdentifier', '')
        place_name = parsed_address.get('PlaceName', '')
        state_name = parsed_address.get('StateName', '')
        zip_code = parsed_address.get('ZipCode', '')

        # List to hold address components
        address_parts = []

        # Handle P.O. Box
        if occupancy_type and 'box' in occupancy_type.lower():  # Checks if the occupancy is a P.O. Box
            if occupancy_id:
                address_parts.append(f"{occupancy_type} {occupancy_id}")
            else:
                address_parts.append(f"{occupancy_type}")
        else:
            # Add the street number, name, type (handling pre-directional, post-directional if exists)
            if address_number and street_name:
                # If we have a direction, add it before the street name
                if street_direction:
                    address_parts.append(f"{address_number} {street_direction} {street_name} {street_type}")
                else:
                    address_parts.append(f"{address_number} {street_name} {street_type}")

                # Add post-directional if it exists
                if street_post_direction:
                    address_parts.append(f"{street_post_direction}")

            elif address_number:
                address_parts.append(f"{address_number}")
            elif street_name:
                address_parts.append(f"{street_name}")

            # Add occupancy type (e.g., Suite) and identifier (e.g., 100)
            if occupancy_type and occupancy_id:
                address_parts.append(f"{occupancy_type} {occupancy_id}")

        # Add the place name (city) if present
        if place_name:
            address_parts.append(f"{place_name}")

        # Add the state and zip code
        if state_name:
            address_parts.append(f"{state_name}")

        if zip_code:
            address_parts.append(f"{zip_code}")

        # If address_parts is empty (i.e., no recognizable address components), return an error message
        if not address_parts:
            raise ValueError("The address could not be parsed into recognizable components.")

        # Join parts with commas to create a full address
        return ', '.join(address_parts)

    except Exception as e:
        # If an error occurs, print or log the exception and return a default error message
        print(f"Error formatting address: {e}")
        return "Invalid address format"


# Function to process the Excel file and parse the addresses
def process_excel_file(file_path, column_name, output_file=None):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Check if the specified column exists
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the Excel file.")

        # Apply the `parse_and_format_address` function to each row in the specified column
        df['Formatted Address'] = df[column_name].apply(parse_and_format_address)

        # Print the first few rows of the DataFrame with the formatted addresses
        print(df[['Formatted Address']].head())

        # Optionally, save the results to a new Excel file
        if output_file:
            df.to_excel(output_file, index=False)
            print(f"Formatted addresses saved to {output_file}")

    except Exception as e:
        # Handle any errors that occur during the processing
        print(f"Error processing the Excel file: {e}")

# Main function to browse the file and process it
def main():
    file_path = browse_file()  # Browse for the Excel file
    if file_path:  # If a file was selected
        column_name = 'Address'  # Name of the column that contains the addresses
        output_file = 'formatted_addresses.xlsx'  # Optional output file name
        process_excel_file(file_path, column_name, output_file)  # Process the file

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
