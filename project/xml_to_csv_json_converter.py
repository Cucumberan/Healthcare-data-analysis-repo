import xml.etree.ElementTree as ET
import csv
from pathlib import Path


def xml_to_csv(input_file):
    """
    Converts the specified XML file to CSV format.

    This function processes an iPhone data XML file, extracting data
    from records of type 'HKQuantityTypeIdentifierDistanceWalkingRunning'.
    It saves the extracted data in CSV format with the same 
    filename as the original XML file.

    Args:
        input_file (str): The path to the XML file to convert.
    """
    # Create a Path object from the input file
    xml_file = Path(input_file)

    # Check if the file exists
    if not xml_file.is_file():
        print(f"The file '{input_file}' does not exist.")
        return

    tree = ET.parse(xml_file)
    root = tree.getroot()

    walking_running = []

    # Extract data from XML for specified record type
    for record in root.findall(".//Record[@type='HKQuantityTypeIdentifierDistanceWalkingRunning']"):
        walking_running.append({
            'start_date': record.get('startDate'),  # Get the start date
            'end_date': record.get('endDate'),      # Get the end date
            'value': record.get('value'),            # Get the value
            'unit': record.get('unit'),              # Get the unit
        })

    # Save the extracted data to a CSV file
    csv_filename = xml_file.with_suffix('.csv')
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        # Define the headers based on the keys of the first dictionary
        if walking_running:
            fieldnames = walking_running[0].keys()
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the header (first row of the CSV)
            csv_writer.writeheader()

            # Write the extracted data to the CSV file
            csv_writer.writerows(walking_running)

    print("Conversion complete! The XML file has been processed.")

if __name__ == '__main__':
    # Prompt the user for the path to the XML file
    input_file = input("Enter the path to the XML file: ").strip("'\"")  # Remove surrounding quotes if any
    xml_to_csv(input_file)
