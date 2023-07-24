# Working used as of Monday week - 6
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pymysql
import csv 
import math
import numpy as np

# Establish MySQL connection
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="linuXshellz448?",
    database="master_database"
)

# Create Tkinter window
window = tk.Tk()
window.title("Database Generator")
window.geometry("500x700")
window.configure(bg="white")

# Function to handle the "Browse and Append" button click event
def browse_files():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        # Read Excel file into a DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        df = df.fillna("NULL") 
        # Check the columns in the DataFrame
        if all(col in df.columns for col in ['AnimalId', 'Date', 'Hour', 'RuminationTimeInSeconds', 'EatingTimeInSeconds']):
            # Convert date column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to RT_ET
            append_to_table(df, "RT_ET")

        elif all(col in df.columns for col in ['AnimalId', 'Date', 'Hour', 'Motion', 'MotionHeatIndicator']):
            # Convert date column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to Animal_Motion
            append_to_table(df, "Animal_Motion")

        elif df.columns[0] == 'ID':
            df = df.rename(columns={'ID': 'Cow_id'})
            # Reshape the DataFrame
            df = pd.melt(df, id_vars=['Cow_id'], var_name='Date', value_name='MilkWeights')
            # Convert 'Date' column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y').dt.strftime('%Y-%m-%d')
            # Append DataFrame to Milk_Weights
            append_to_table(df, "Milk_Weights")

        elif all(col in df.columns for col in ['Animal_ID', 'Group_ID', 'Date', 'Days_in_Milk', 'Age_Days', 'Lactation_Num']):
            # Convert date column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to Cow_Data
            append_to_table(df, "Cow_Data")

        elif df.columns[4] == "Start Time":
            # Extract only the date part from the datetime and overwrite the "Date" column
            df['Start Time'] = pd.to_datetime(df['Start Time']).dt.date
            # Round hour down to nearest whole hour
            df['Hour'] = df['Hour of Day'].apply(math.floor)
            # Drop the undesired columns
            df.drop(columns=['Farm Name', 'FID', 'End Time', 'Was Interrupted', 'Interrupting Tags', 'Midpoint Since Last', 'Midpoint Until Next', 'RID'], inplace=True)
            # Drop all rows where the "RFID" column does not start with "984"
            df = df[df['RFID'].astype(str).str.startswith('984')]
            # Only take first part of farm name
            df['Farm'] = df['Farm'].str.split('_').str[0]
            # Append DataFrame to Gas_Data
            append_to_table(df, "Gas_Data")

        elif df.columns[0] == 'Cow':
            # Extract the desired columns and rename them
            data_subset = df[['Cow', 'Date', 'DM Consumed']]
            # Convert date column to YYYY-MM-DD format
            data_subset['Date'] = pd.to_datetime(data_subset['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to DMI
            append_to_table(data_subset, "DMI")

        elif df.columns[0] == 'Sample':
            # Drop undesired columns
            df.drop(columns=['Farm', 'Timepoint'], inplace=True)
            #Convert date column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to VFA
            append_to_table(df, "VFA")

        elif df.columns[1] == 'Calan_id':
            #Reorder columns 
            df = df.reindex(columns=["Cow_id", "Calan_id", "Ear_id", "Collar_id", "Date"])
            # Append DataFrame to RFID
            append_to_table(df, "RFID")

        elif df.columns[0] == 'Genus':
            df = df.rename(columns={'Genus': 'Taxon'})
            # Reshape the DataFrame and reorder columns 
            df = pd.melt(df, id_vars=['Taxon'], var_name='Sample_id', value_name='Genus_Relative_Freq')
            df = df.reindex(columns=["Sample_id", "Taxon", "Genus_Relative_Freq"])
            # Append DataFrame to Relative Frequency table
            append_to_table(df, "Relative_Freq")

        elif df.columns[0] == 'Unweighted':
            df = df.rename(columns={'Unweighted': 'Sample_id1'})
            # Reshape the DataFrame 
            df = pd.melt(df, id_vars=['Sample_id1'], var_name='Sample_id2', value_name='Unweighted_Distance')
            # Drop any rows where the two sample id's are the same, or if the combination of samples is repeated
            df = df[df['Sample_id1'] != df['Sample_id2']]
            df[['Sample_id1', 'Sample_id2']] = np.sort(df[['Sample_id1', 'Sample_id2']], axis=1)
            df.drop_duplicates(inplace=True)
            # Append DataFrame to Microbial Matrix Table
            append_to_table(df, "Matrix_unweighted")
        
        elif df.columns[0] == 'Weighted':
            df = df.rename(columns={'Weighted': 'Sample_id1'})
            # Reshape the DataFrame 
            df = pd.melt(df, id_vars=['Sample_id1'], var_name='Sample_id2', value_name='Weighted_Distance')
            # Drop any rows where the two sample id's are the same, or if the combination of samples is repeated
            df = df[df['Sample_id1'] != df['Sample_id2']]
            df[['Sample_id1', 'Sample_id2']] = np.sort(df[['Sample_id1', 'Sample_id2']], axis=1)
            df.drop_duplicates(inplace=True)
            # Append DataFrame to Microbial Matrix Table
            append_to_table(df, "Matrix_weighted")

        elif df.column[3] == 'Taxa_Classifier':
            # Append DataFrame to Microbial Metadata Table
            append_to_table(df, "Microbial_Metadata")

        else:
            result_label.config(text="Invalid file format.", fg="red")
            return

        result_label.config(text="File appended successfully.", fg="green")

# Function to append DataFrame to a specified table
def append_to_table(df, table_name):
    # Replace NaN values with None
    df = df.where((pd.notnull(df)), None)

    # Append DataFrame to MySQL table
    with connection.cursor() as cursor:
        for row in df.itertuples(index=False):
            if table_name == "RT_ET":
                sql = "INSERT INTO RT_ET (Cow_id, Date, Hour, RuminationTimeInSeconds, EatingTimeInSeconds) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "Animal_Motion":
                sql = "INSERT INTO Animal_Motion (Cow_id, Date, Hour, Motion, MotionHeatIndicator) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "Milk_Weights":
                sql = "INSERT INTO Milk_Weights (Cow_id, Date, MilkWeights) VALUES (%s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "Cow_Data":
                sql = "INSERT INTO Cow_Data (Cow_id, Group_id, Date, DaysInMilk, AgeInDays, LactationNum) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "Gas_Data":
                sql = "INSERT INTO Gas_Data (Cow_id, Cow_rfid, Date, Good_Data_Duration, Exact_Hour, CO2_Massflow, CH4_Massflow, O2_Massflow, H2_Massflow, H2S_Massflow, Average_Airflow, Airflow_CF, Average_Wind_Speed, Average_Wind_Direction, Wind_CF, Standard_Deviation_of_CH4_Baseline, Pipe_Temperature, Gas_Temperature, Farm, Hour) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "DMI":
                sql = "INSERT INTO DMI (Cow_id, Date, DM_Consumed) VALUES (%s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "VFA":
                sql = "INSERT INTO VFA (Sample_id, Date, Cow_id, Rep, Acetic_mM, Propionic_mM, Isobutyric_mM, Butyric_mM, Isovaleric_mM, Valeric_acid_mM, Total_VFA, Acetic_prop, Propionic_prop, Isobutyric_prop, Butyric_prop, Isovaleric_prop, Valeric_acid_prop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "RFID":
                sql = "INSERT INTO RFID (Cow_id, Calan_id, Ear_id, Collar_id, Date) " \
                        f"VALUES (%s, " \
                        f"COALESCE((SELECT Calan_id FROM RFID WHERE Cow_id = %s AND Date = %s), %s), " \
                        f"COALESCE((SELECT Ear_id FROM RFID WHERE Cow_id = %s AND Date = %s), %s), " \
                        f"COALESCE((SELECT Collar_id FROM RFID WHERE Cow_id = %s AND Date = %s), %s), " \
                        "%s)"
            elif table_name == "Relative_Freq":
                sql = "INSERT INTO Relative_Freq (Sample_id, Taxon, Genus_Relative_Freq) VALUES (%s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "Matrix_unweighted":
                sql = "INSERT INTO Microbial_Matrix (Sample_id1, Sample_id2, Unweighted_Distance) VALUES (%s, %s, %s)"\
                      "ON DUPLICATE KEY UPDATE Unweighted_Distance = VALUES(Unweighted_Distance)"
                cursor.execute(sql, row)
            elif table_name == "Matrix_weighted":
                sql = "INSERT INTO Microbial_Matrix (Sample_id1, Sample_id2, Weighted_Distance) VALUES (%s, %s, %s)"\
                      "ON DUPLICATE KEY UPDATE Weighted_Distance = VALUES(Weighted_Distance)"
                cursor.execute(sql, row)  
            elif table_name == "Microbial_Metadata":
                sql = "INSERT INTO Microbial_Metadata (Sample_id, Cow_id, Farm, Taxa_Classifier, Date, Hour, Mapping_File) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
                cursor.execute(sql, row)
    connection.commit()

def merge_microbial_metadata():
    cursor = connection.cursor()
    # Build SQL query to populate microbial matrix cow_id columns with metadata
    query = "UPDATE Microbial_Matrix mm"\
            "LEFT JOIN Microbial_Metadata md ON mm.Sample_id1 = md.Sample_id"\
            "LEFT JOIN Microbial_Metadata md2 ON mm.Sample_id2 = md2.Sample_id"\
            "SET mm.Cow_id1 = md.Cow_id,"\
                "mm.Cow_id2 = md2.Cow_id"
    # Build SQL query to populate relative frequency cow_id and farm columns with metadata
    query1 = "UPDATE Relative_Freq fq"\
            "LEFT JOIN Microbial_Metadata md ON fq.Sample_id = md.Sample_id"\
            "SET fq.Cow_id = md.Cow_id,"\
                "fq.Farm = md2.Farm"
    # Execute the query
    cursor.execute(query)
    cursor.execute(query1)
    result_label.config(text="Metadata has been merged", fg="green")
    connection.commit()

def export_csv():
    # Retrieve selected date range from GUI
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    cursor = connection.cursor()

    # Build SQL query
    query = f"SELECT * FROM RT_ET WHERE Date >= '{start_date}' AND Date <= '{end_date}'"

    # Execute the query
    cursor.execute(query)

    # Fetch column names from the result set
    column_names = [desc[0] for desc in cursor.description]

    # Get selected columns from the listbox
    selected_columns_indices = column_listbox.curselection()

    # Map selected column indices to column names
    selected_columns = [column_names[index] for index in selected_columns_indices]

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Prepare CSV file name
    file_name = "exported_data.csv"

    # Export selected columns as CSV
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write the column names as the header row
        csv_writer.writerow(selected_columns)

        # Iterate over the fetched data and write the selected columns
        for row in rows:
            selected_values = [str(row[column_index]) for column_index in selected_columns_indices]
            csv_writer.writerow(selected_values)

    result_label.config(text="Select Data Export is complete.", fg="green")
    connection.commit()

 #create merge function to merge all necessary data for the microbial data 

 #========================================================================================  
 # begin GUI elements   

# Date range input fields
start_date_label = tk.Label(window, text="Start Date:")
start_date_label.pack(pady=10)

start_date_entry = tk.Entry(window)
start_date_entry.pack(pady=10)

end_date_label = tk.Label(window, text="End Date:")
end_date_label.pack(pady=10)
end_date_entry = tk.Entry(window)
end_date_entry.pack(pady=10)

# Column selection listbox with checkboxes
column_label = tk.Label(window, text="Select Columns:")
column_label.pack(pady=10)

column_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
column_listbox.pack(pady=10, ipadx=15)

# Add items to the column_listbox
column_names = [
    "Cow_id", "Date", "Hour", "RuminationTimeInSeconds", "EatingTimeInSeconds",
    "Motion", "MotionHeatIndicator", "MilkWeights", "Group_id", "DaysInMilk",
    "AgeInDays", "LactationNum", "RFID", "Farm", "Good_Data_Duration", "CO2_Massflow", "CH4_Massflow",
    "O2_Massflow", "H2_Massflow", "H2S_Massflow", "Average_Airflow", "Airflow_CF",
    "Average_Wind_Speed", "Average_Wind_Direction", "Wind_CF", "Midpoint_Since_Last", "Midpoint_Until_Next",
    "Standard_Deviation_of_CH4_Baseline", "Pipe_Temperature", "Gas_Temperature",
    "DM_Consumed", 'Sample', 'Total_VFA', 'Acetic_prop', 'Propionic_prop',
    'Isobutyric_prop', 'Butyric_prop', 'Isovaleric_prop', 'Valeric_acid_prop'
]

for column in column_names:
    column_listbox.insert(tk.END, column)

# Create "Browse and Append" button
browse_button = tk.Button(window, text="Browse and Append", command=browse_files, padx=10, pady=5, bg="#4caf50", fg="blue", width=20)
browse_button.pack(pady=10)

# Create "Export Selected Data" button
export_button = tk.Button(window, text="Export Selected Data", command=export_csv, padx=10, pady=5, bg="#4caf50", fg="green", width=20)
export_button.pack(pady=10)

# Create "Merge Microbial Metadata" button
export_button = tk.Button(window, text="Merge Microbial Metadata", command=merge_microbial_metadata, padx=10, pady=5, bg="#4caf50", fg="green", width=20)
export_button.pack(pady=10)

# Create result label
result_label = tk.Label(window, text="", fg="black")
result_label.pack(pady=10)


# Run the Tkinter event loop
window.mainloop()

# Close MySQL connection
connection.close()
