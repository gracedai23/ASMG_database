# Working used as of Monday week - 6
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pymysql
import csv 

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
window.configure(bg="#f0f0f0")

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
            # Append DataFrame to master_table
            append_to_table(df, "master_table")
        elif all(col in df.columns for col in ['AnimalId', 'Date', 'Hour', 'Motion', 'MotionHeatIndicator']):
            # Convert date column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to master_table_1
            append_to_table(df, "master_table_1")
        elif df.columns[0] == 'ID':
            # Append DataFrame to master_table_2
            append_to_table1(df, "master_table_2")
        elif all(col in df.columns for col in ['Animal_ID', 'Group_ID', 'Date', 'Days_in_Milk', 'Age_Days', 'Lactation_Num', 'RuminationTime(seconds)', 'EatingTime(seconds)']):
            # Convert date column to YYYY-MM-DD format
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to master_table_3
            append_to_table(df, "master_table_3")
        elif df.columns[2] == "Farm_Name":
             # Extract the date part from 'Start_Time' column
             df['Date'] = pd.to_datetime(df['Start_Time']).dt.date
             # Convert date column to YYYY-MM-DD format
             df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
             # Append DataFrame to master_table_4
             append_to_table(df, "master_table_4")
        elif df.columns[0] == 'Cow':
            # Extract the desired columns and rename them
            data_subset = df[['Cow', 'Date', 'DM Consumed']]
            data_subset.rename(columns={'Cow': 'Cow_id', "DM Consumed" : "DM_Consumed" }, inplace=True)
            # Convert date column to YYYY-MM-DD format
            data_subset['Date'] = pd.to_datetime(data_subset['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to master_table_5
            append_to_table(data_subset, "master_table_5")
        elif df.columns[13] == 'Total VFA':
            #Extract the desired columnds and remane them
            df.rename(columns={'Group': "Group_ID", "cowID": "Cow_id", "Valeric acid_mM": "Valeric_acid_mM", "Total VFA": "Total_VFA", "Valeric acid_prop": "Valeric_acid_prop"})
            #Convert date column to YYYY-MM-DD formate
            df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
            # Append DataFrame to master_table_6
            append_to_table(df, "master_table_6")

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
            if table_name == "master_table":
                sql = "INSERT INTO master_table (Cow_id, Date, Hour, RuminationTimeInSeconds, EatingTimeInSeconds) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "master_table_1":
                sql = "INSERT INTO master_table_1 (Cow_id, Date, Hour, Motion, MotionHeatIndicator) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "master_table_2":
                sql = "INSERT INTO master_table_2 (Cow_id, Date, MilkWeights) VALUES (%s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "master_table_3":
                sql = "INSERT INTO master_table_3 (Cow_id, Group_id, Date, DaysInMilk, AgeInDays, LactationNum, RuminationTimeInSeconds, EatingTimeInSeconds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "master_table_4":
                sql = "INSERT INTO master_table_4 (Cow_id, RFID, Farm_Name, FID, Start_Time, End_Time, Good_Data_Duration, Hour_Of_Day, CO2_Massflow, CH4_Massflow, O2_Massflow, H2_Massflow, H2S_Massflow, Average_Airflow, Airflow_CF, Average_Wind_Speed, Average_Wind_Direction, Wind_CF, Was_Interrupted, Interrupting_Tags, Midpoint_Since_Last, Midpoint_Until_Next, Standard_Deviation_of_CH4_Baseline, Pipe_Temperature, Gas_Temperature, RID, Farm, Date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s,%s, %s, %s,%s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "master_table_5":
                sql = "INSERT INTO master_table_5 (Cow_id, Date, DM_Consumed) VALUES (%s, %s, %s)"
                cursor.execute(sql, row)
            elif table_name == "master_table_6":
                sql = "INSERT INTO master_table_6 (Sample, Farm, Date, Cow_id, Cluster, Timepoint, Rep, Acetic_mM, Propionic_mM, Isobutyric_mM, Butyric_mM, Isovaleric_mM, Valeric_acid_mM, Total_VFA, Acetic_prop, Propionic_prop, Isobutyric_prop, Butyric_prop, Isovaleric_prop, Valeric_acid_prop) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, row)
    connection.commit()

def append_to_table1(df, table_name):
    # Replace NaN values with None
    df = df.where((pd.notnull(df)), None)

    # Rename 'ID' column to 'Cow_id'
    df = df.rename(columns={'ID': 'Cow_id'})

    # Reshape the DataFrame
    df = pd.melt(df, id_vars=['Cow_id'], var_name='Date', value_name='MilkWeights')

    # Convert 'Date' column to YYYY-MM-DD format
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y').dt.strftime('%Y-%m-%d')

    # Append DataFrame to MySQL table
    with connection.cursor() as cursor:
        for row in df.itertuples(index=False):
            if table_name == "master_table_2":
                sql = "INSERT INTO master_table_2 (Cow_id, Date, MilkWeights) VALUES (%s, %s, %s)"
                cursor.execute(sql, row)
    connection.commit()



# Function to export master_data table as CSV file
def export_as_csv():
    # Query the master_data table
    with connection.cursor() as cursor:
        sql = "SELECT * FROM master_data"
        cursor.execute(sql)
        data = cursor.fetchall()

    # Convert query result to DataFrame
    df = pd.DataFrame(data, columns=['Cow_id', 'Date', 'Hour', 'RuminationTimeInSeconds', 'EatingTimeInSeconds', 'Motion', 'MotionHeatIndicator', 'MilkWeights', 'Group_id', 'DaysInMilk', 'AgeInDays', 'LactationNum', 
'RFID', 'Farm_Name', 'FID', 'Start_Time', 'End_Time', 'Good_Data_Duration', 'Hour_Of_Day', 'CO2_Massflow', 'CH4_Massflow', 'O2_Massflow', 'H2_Massflow', 'H2S_Massflow', 'Average_Airflow', 'Airflow_CF', 'Average_Wind_Speed', 'Average_Wind_Direction', 'Wind_CF', 'Was_Interrupted', 'Interrupting_Tags', 'Midpoint_Since_Last', 'Midpoint_Until_Next', 'Standard_Deviation_of_CH4_Baseline', 'Pipe_Temperature', 'Gas_Temperature', 'RID', 'Farm', 'DM_Consumed', 
'Sample', 'Cluster', 'Timepoint', 'Rep', 'Acetic_mM', 'Propionic_mM', 'Isobutyric_mM', 'Butyric_mM', 'Isovaleric_mM','Valeric_acid_mM', 'Total_VFA', 'Acetic_prop', 'Propionic_prop','Isobutyric_prop', 'Butyric_prop', 'Isovaleric_prop', 'Valeric_acid_prop'])

    # Prompt user to select the save location for the CSV file
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])

    if file_path:
        # Save DataFrame as CSV file
        df.to_csv(file_path, index=False)
        result_label.config(text="Data exported successfully.", fg="green")
    else:
        result_label.config(text="Export cancelled.", fg="red")

# Function to Merge the SQL query
def execute_query():
    # Execute the SQL query
    with connection.cursor() as cursor:
        # Insert values from master_table
        cursor.execute("""
            INSERT INTO master_data (Cow_id, Date, Hour, RuminationTimeInSeconds, EatingTimeInSeconds)
            SELECT
                mt.Cow_id,
                mt.Date,
                mt.Hour,
                mt.RuminationTimeInSeconds,
                mt.EatingTimeInSeconds
            FROM
                master_table mt
            ON DUPLICATE KEY UPDATE
                RuminationTimeInSeconds = mt.RuminationTimeInSeconds,
                EatingTimeInSeconds = mt.EatingTimeInSeconds
        """)

        # Insert values from master_table_1
        cursor.execute("""
            INSERT INTO master_data (Cow_id, Date, Hour, Motion, MotionHeatIndicator)
            SELECT
                mt1.Cow_id,
                mt1.Date,
                mt1.Hour,
                mt1.Motion,
                mt1.MotionHeatIndicator
            FROM
                master_table_1 mt1
            ON DUPLICATE KEY UPDATE
                Motion = mt1.Motion,
                MotionHeatIndicator = mt1.MotionHeatIndicator
        """)

        # Insert values from master_table_2
        cursor.execute("""
            INSERT INTO master_data (Cow_id, Date, MilkWeights)
            SELECT
                mt2.Cow_id,
                mt2.Date,
                mt2.MilkWeights
            FROM
                master_table_2 mt2
            ON DUPLICATE KEY UPDATE
                MilkWeights = mt2.MilkWeights
        """)

        # Insert values from master_table_3
        cursor.execute("""
            INSERT INTO master_data (Cow_id, Group_id, Date, AgeInDays, DaysInMilk, LactationNum, RuminationTimeInSeconds, EatingTimeInSeconds)
            SELECT
                mt3.Cow_id,
                mt3.Group_id,
                mt3.Date,
                mt3.AgeInDays,
                mt3.DaysInMilk,
                mt3.LactationNum,
                mt3.RuminationTimeInSeconds,
                mt3.EatingTimeInSeconds
            FROM
                master_table_3 mt3
            ON DUPLICATE KEY UPDATE
                Group_id = mt3.Group_id,
                AgeInDays = mt3.AgeInDays,
                DaysInMilk = mt3.DaysInMilk,
                LactationNum = mt3.LactationNum,
                RuminationTimeInSeconds = mt3.RuminationTimeInSeconds,
                EatingTimeInSeconds = mt3.EatingTimeInSeconds
        """)

        # Insert values from master_table_4
        cursor.execute("""
            INSERT INTO master_data (Cow_id, RFID, Farm_Name, FID, Start_Time, End_Time, Good_Data_Duration, Hour_Of_Day, CO2_Massflow, CH4_Massflow, O2_Massflow, H2_Massflow, H2S_Massflow, Average_Airflow, Airflow_CF, Average_Wind_Speed, Average_Wind_Direction, Wind_CF, Was_Interrupted, Interrupting_Tags, Midpoint_Since_Last, Midpoint_Until_Next, Standard_Deviation_of_CH4_Baseline, Pipe_Temperature, Gas_Temperature, RID, Farm)
            SELECT
                mt4.Cow_id,
                mt4.RFID,
                mt4.Farm_Name,
                mt4.FID,
                mt4.Start_Time,
                mt4.End_Time,
                mt4.Good_Data_Duration,
                mt4.Hour_Of_Day,
                mt4.CO2_Massflow,
                mt4.CH4_Massflow,
                mt4.O2_Massflow,
                mt4.H2_Massflow,
                mt4.H2S_Massflow,
                mt4.Average_Airflow,
                mt4.Airflow_CF,
                mt4.Average_Wind_Speed,
                mt4.Average_Wind_Direction,
                mt4.Wind_CF,
                mt4.Was_Interrupted,
                mt4.Interrupting_Tags,
                mt4.Midpoint_Since_Last,
                mt4.Midpoint_Until_Next,
                mt4.Standard_Deviation_of_CH4_Baseline,
                mt4.Pipe_Temperature,
                mt4.Gas_Temperature,
                mt4.RID,
                mt4.Farm
            FROM
                master_table_4 mt4
            ON DUPLICATE KEY UPDATE
                RFID = mt4.RFID,
                Farm_Name = mt4.Farm_Name,
                FID = mt4.FID,
                Start_Time = mt4.Start_Time,
                End_Time = mt4.End_Time,
                Good_Data_Duration = mt4.Good_Data_Duration,
                Hour_Of_Day = mt4.Hour_Of_Day,
                CO2_Massflow = mt4.CO2_Massflow,
                CH4_Massflow = mt4.CH4_Massflow,
                O2_Massflow = mt4.O2_Massflow,
                H2_Massflow = mt4.H2_Massflow,
                H2S_Massflow = mt4.H2S_Massflow,
                Average_Airflow = mt4.Average_Airflow,
                Airflow_CF = mt4.Airflow_CF,
                Average_Wind_Speed = mt4.Average_Wind_Speed,
                Average_Wind_Direction = mt4.Average_Wind_Direction,
                Wind_CF = mt4.Wind_CF,
                Was_Interrupted = mt4.Was_Interrupted,
                Interrupting_Tags = mt4.Interrupting_Tags,
                Midpoint_Since_Last = mt4.Midpoint_Since_Last,
                Midpoint_Until_Next = mt4.Midpoint_Until_Next,
                Standard_Deviation_of_CH4_Baseline = mt4.Standard_Deviation_of_CH4_Baseline,
                Pipe_Temperature = mt4.Pipe_Temperature,
                Gas_Temperature = mt4.Gas_Temperature,
                RID = mt4.RID,
                Farm = mt4.Farm
        """)

        # Insert values from master_table_5
        cursor.execute("""
            INSERT INTO master_table_5 (Cow_id, Date, DM_Consumed)
            SELECT
                mt5.Cow_id,
                mt5.Date,
                mt5.DM_Consumed
            FROM
                master_table_5 mt5
            ON DUPLICATE KEY UPDATE
                DM_Consumed = mt5.DM_Consumed
        """)

        # Insert values from master_table_6
        cursor.execute("""
            INSERT INTO master_table_6 (Sample, Farm, Date, Cow_id, Cluster, Timepoint, Rep, Acetic_mM, Propionic_mM, Isobutyric_mM, Butyric_mM, Isovaleric_mM, Valeric_acid_mM, Total_VFA, Acetic_prop, Propionic_prop, Isobutyric_prop, Butyric_prop, Isovaleric_prop, Valeric_acid_prop) 
            SELECT
                mt6.Sample, 
                mt6.Farm, 
                mt6.Date,
                mt6.Cow_id,
                mt6.Cluster,
                mt6.Timepoint,
                mt6.Rep,
                mt6.Acetic_mM,
                mt6.Propionic_mM,
                mt6.Isobutyric_mM,
                mt6.Butyric_mM,
                mt6.Isovaleric_mM,
                mt6.Valeric_acid_mM,
                mt6.Total_VFA,
                mt6.Acetic_prop,
                mt6.Propionic_prop,
                mt6.Isobutyric_prop,
                mt6.Butyric_prop,
                mt6.Isovaleric_prop,
                mt6.Valeric_acid_prop
            FROM
                master_table_6 mt6
            ON DUPLICATE KEY UPDATE
                Sample = mt6.Sample, 
                Farm = mt6.Farm, 
                Date = mt6.Date,
                Cow_id = mt6.Cow_id,
                Cluster = mt6.Cluster,
                Timepoint = mt6.Timepoint,
                Rep = mt6.Rep,
                Acetic_mM = mt6.Acetic_mM,
                Propionic_mM = mt6.Propionic_mM,
                Isobutyric_mM = mt6.Isobutyric_mM,
                Butyric_mM = mt6.Butyric_mM,
                Isovaleric_mM = mt6.Isovaleric_mM,
                Valeric_acid_mM = mt6.Valeric_acid_mM,
                Total_VFA = mt6.Total_VFA,
                Acetic_prop = mt6.Acetic_prop,
                Propionic_prop = mt6.Propionic_prop,
                Isobutyric_prop = mt6.Isobutyric_prop,
                Butyric_prop = mt6.Butyric_prop,
                Isovaleric_prop = mt6.Isovaleric_prop,
                Valeric_acid_prop = mt6.Valeric_acid_prop
        """)

        # Delete duplicate rows from master_data
        cursor.execute("""
            DELETE FROM master_data
            WHERE (Cow_id, Date, Hour) IN (
                SELECT Cow_id, Date, Hour
                FROM (
                SELECT Cow_id, Date, Hour, ROW_NUMBER() OVER (PARTITION BY Cow_id, Date, Hour ORDER BY (SELECT NULL)) AS row_num
                FROM master_data
            ) AS subquery
                WHERE row_num > 1
                             )
        """)

        connection.commit()
        result_label.config(text="Query executed successfully.", fg="green")




def export_csv():
    # Retrieve selected date range from GUI
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()

    cursor = connection.cursor()

    # Build SQL query
    query = f"SELECT * FROM master_data WHERE Date >= '{start_date}' AND Date <= '{end_date}'"

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
column_listbox.pack(pady=10)

# Add items to the column_listbox
column_names = [
    "Cow_id", "Date", "Hour", "RuminationTimeInSeconds", "EatingTimeInSeconds",
    "Motion", "MotionHeatIndicator", "MilkWeights", "Group_id", "DaysInMilk",
    "AgeInDays", "LactationNum", "RFID", "Farm_Name", "FID", "Start_Time",
    "End_Time", "Good_Data_Duration", "Hour_Of_Day", "CO2_Massflow", "CH4_Massflow",
    "O2_Massflow", "H2_Massflow", "H2S_Massflow", "Average_Airflow", "Airflow_CF",
    "Average_Wind_Speed", "Average_Wind_Direction", "Wind_CF", "Was_Interrupted",
    "Interrupting_Tags", "Midpoint_Since_Last", "Midpoint_Until_Next",
    "Standard_Deviation_of_CH4_Baseline", "Pipe_Temperature", "Gas_Temperature",
    "RID", "DM_Consumed", 'Sample', 'Date', 'Farm', 'Cluster', 'Timepoint', 'Rep',
    'Acetic_mM', 'Propionic_mM', 'Isobutyric_mM', 'Butyric_mM', 'Isovaleric_mM',
    'Valeric_acid_mM', 'Total_VFA', 'Acetic_prop', 'Propionic_prop',
    'Isobutyric_prop', 'Butyric_prop', 'Isovaleric_prop', 'Valeric_acid_prop'
]

for column in column_names:
    column_listbox.insert(tk.END, column)

# Export button
export_button = tk.Button(window, text="Export selected data", command=export_csv, padx=10, pady=5, bg="#4caf50", fg="black", width=20)
export_button.pack(pady=10)



# Create "Browse and Append" button
browse_button = tk.Button(window, text="Browse and Append", command=browse_files, padx=10, pady=5, bg="#4caf50", fg="black", width=20)
browse_button.pack(pady=10)

# Create "Execute Query" button
execute_button = tk.Button(window, text="Merge", command=execute_query, padx=10, pady=5, bg="#4caf50", fg="black", width=20)
execute_button.pack(pady=10)


# Create "Export as CSV" button
export_button = tk.Button(window, text="Export Master Data", command=export_as_csv, padx=10, pady=5, bg="#4caf50", fg="black", width=20)
export_button.pack(pady=10)

# Create result label
result_label = tk.Label(window, text="", fg="black")
result_label.pack(pady=10)



# Run the Tkinter event loop
window.mainloop()

# Close MySQL connection
connection.close()
