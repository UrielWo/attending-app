import sys
import os
import pandas as pd
# csv_file = "/home/uriel/PythonExe/attendance_csv_files/participant-20220824102638.csv" # one file option


def private_cases(df):  # Convert Hebrew names to English
    df.loc[df['Name'] == 'אורן גדמו', 'Name'] = 'Oren Gedamu'
    df.loc[df['Name'] == 'מירב חורש', 'Name'] = 'Meirav Horesh'
    df.loc[df['Name'] == 'יוסי בנגייב', 'Name'] = 'Yossi Bengaev'
    df.loc[df['Attendee_Email'] == 'estherwa@gmai.com', 'Attendee_Email'] = 'estherwa@hotmail.es'
    df.loc[df['Attendee_Email'] == 'estherwa@gmail.com', 'Attendee_Email'] = 'estherwa@hotmail.es'
    df.loc[df['Attendee_Email'] == 'estherwah9@gmail.com', 'Attendee_Email'] = 'estherwa@hotmail.es'

def duration_Col(df):  # split Attendance Duration to use min as int for calculations
    df[['Duration', 'Time_unit']] = df['Attendance_Duration'].str.split(' ', expand=True) # i change for the database adding _ to column name
    df['Duration'] = df['Duration'].astype(int)  # convert column string to int

def single_Pivot_Parse(df,Atten_Duration):
    pivot = pd.pivot_table(df, index=['Attendee_Email', 'Name'], values='Duration', aggfunc='sum').reset_index()  # create pivot table
    pivot = pivot.assign(Time_On_Lesson=lambda x: round(x['Duration'] / Atten_Duration * 100))  # calculate percent of attendence
    pivot = pivot.groupby('Attendee_Email').agg({'Name': 'first', 'Time_On_Lesson': 'sum'}).reset_index()  # group by same email
    pivot = pivot.groupby('Name').agg({'Attendee_Email': 'first', 'Time_On_Lesson': 'sum'}).reset_index()  # group by same names
    pivot.loc[pivot['Time_On_Lesson'] > 100, 'Time_On_Lesson'] = pivot['Time_On_Lesson'] / 2
    return pivot

def integrated_Table_Parse(integrated_Table):
    integrated_Pivot = pd.pivot_table(integrated_Table, index=['Attendee_Email', 'Name'], values='Time_On_Lesson').reset_index()
    integrated_Pivot = integrated_Pivot.groupby('Attendee_Email').agg({'Name': 'first', 'Time_On_Lesson': 'mean'}).reset_index()  # group by same email
    integrated_Pivot = integrated_Pivot.groupby('Name').agg({'Attendee_Email': 'first', 'Time_On_Lesson': 'mean'}).reset_index()  # group by same names
    integrated_Pivot['Time_On_Lesson'] = round(integrated_Pivot['Time_On_Lesson'])
    integrated_Pivot = integrated_Pivot.sort_values(by='Time_On_Lesson', ascending=False)  # sort by time on lesson
    #integrated_Pivot['Time_On_Lesson'] = integrated_Pivot['Time_On_Lesson'].astype(str) + '%' # add % to percent
    return integrated_Pivot

def Daily_Attendence(integrated_Table):  # check by name attendence per lesson
    Daily_Att = integrated_Table.value_counts(subset='Attendee_Email').reset_index()
    Daily_Att = Daily_Att.rename(columns = {0:'Daily_Att'})
    return (Daily_Att)

def merge_daily_to_time(integrated_Count, integrated_Pivot):
    integrated_Total = pd.concat([integrated_Count, integrated_Pivot], axis=0, ignore_index=False)  # concat daily with integrated
    integrated_Total = integrated_Total.groupby('Attendee_Email').agg({'Name': 'last', 'Time_On_Lesson': 'mean', 'Daily_Att': 'sum'}).reset_index()
    integrated_Total['Name'] = integrated_Total['Name'].str.lower()
    integrated_Total = integrated_Total.groupby('Name').agg({'Attendee_Email': 'first', 'Time_On_Lesson': 'mean', 'Daily_Att': 'sum'}).reset_index()
    integrated_Total = integrated_Total[integrated_Total['Daily_Att'] > 2]
    integrated_Total = integrated_Total.reset_index(drop=True)
    return integrated_Total

def attendance_summary(path):
    if not os.path.exists(path):
        print("Your directory not exist :", path)# check dir
    csv_files_list = list(map(lambda x: os.path.join(os.path.abspath(path), x), os.listdir(path)))  # create list of absolute path of files in dir (arg)
    integrated_Table = pd.DataFrame()

    for files in csv_files_list:
        df = pd.read_csv(files, encoding="UTF-16LE", sep="\t")  # encoding
        duration_Col(df)  # split Attendance Duration to use min as int for calculations
        private_cases(df)  # Convert Hebrew names to English
        Atten_Duration = (df['Duration'].max())  # get max value of from duration column
        pivot = single_Pivot_Parse(df, Atten_Duration)
        integrated_Table = pd.concat([integrated_Table, pivot], axis=0)  # concat all the csv files

    integrated_Count = Daily_Attendence(integrated_Table)
    integrated_Pivot = integrated_Table_Parse(integrated_Table)
    return merge_daily_to_time(integrated_Count, integrated_Pivot)

if __name__ == "__main__":
    attendance_summary(sys.argv[1])