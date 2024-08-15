import os
import iesve
import csv
from ies_file_picker import IesFilePicker

# Initialize the global variable
peak_loads = {}

if __name__ == "__main__":
    try:
        # Get the current project
        project = iesve.VEProject.get_current_project()
        project_folder = project.path
        print(f"Project Folder: {project_folder}")

        # Initialize the results reader
        results_file_path = IesFilePicker.pick_aps_file()
        print(f"Results File Path: {results_file_path}")

        results_reader = iesve.ResultsReader.open(results_file_path)

        room_ids = results_reader.get_room_ids()
        room_list = results_reader.get_room_list()
        print(f"Room IDs: {room_ids}")
        print(f"Room List: {room_list}")
        

        # Collect heating loads
        for index, room_id in enumerate(room_ids):
            aps_data = results_reader.get_peak_results(room_id, ['Room units heating load', 'z'])
            print(aps_data)
            if room_list[index] not in peak_loads:
                peak_loads[room_list[index]] = {}
            peak_loads[room_list[index]]["Peak Heating Load (kW)"] = aps_data
            print(peak_loads)

        # Collect cooling loads
        for index, room_id in enumerate(room_ids):
            apss_data = results_reader.get_peak_results(room_id, ['Room units cooling load', 'z'])
            print(apss_data)
            if room_list[index] not in peak_loads:
                peak_loads[room_list[index]] = {}
            peak_loads[room_list[index]]["Peak Cooling Load (kW)"] = apss_data
            print(peak_loads)

        # Output CSV file
        output_csv = 'room_peak_loads.csv'

        # Write the data to a CSV file
        with open(output_csv, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
    
            # Write the header
            writer.writerow(['Office Name', 'Office ID', 'Area (m2)', 'Volume (m3)', 'Load Type', 'Load Name', 'Load Value (W)','Load Value(kW)','W/m2'])

            # Iterate over each entry in the data
            for key, value in peak_loads.items():
                # Unpack the tuple (Office Name, Office ID, Area, Volume)
                office_name, office_id, area, volume = key

                # Iterate through the nested dictionary to get the load type and load name/value
                for load_type, load_info in value.items():
                    for load_name, load_value in load_info.items():
                        # Write a row to the CSV file
                        writer.writerow([office_name, office_id, area, volume, load_type, load_name, load_value,load_value/1000,load_value/area])

        print(f"Data successfully written to {output_csv}")

    except Exception as e:
        print(f"An error occurred: {e}")