# https://github.com/sivel/speedtest-cli
import speedtest as st
import pandas as pd
from datetime import datetime


def get_new_speeds():
    # Class for speed tests
    speed_test = st.Speedtest()
    speed_test.get_best_server()

    # Get ping (miliseconds)
    ping = speed_test.results.ping
    # Perform download and upload speed tests (bits per second)
    download = speed_test.download()
    upload = speed_test.upload()

    # Convert download and upload speeds to megabits per second
    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)

    return (ping, download_mbs, upload_mbs)


def update_csv(internet_speeds):
    # Get today's date in the form Month/Day/Year
    date_today = datetime.today().strftime("%m/%d/%Y")
    # File with the dataset
    csv_file_name = "internet_speeds_dataset.csv"

    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
    # If there's an error, assume the file does not exist and create\
    # the dataset from scratch
    except:
        # No dataset loaded means we'll have an empty DataFrame for\
        # the time being
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"]
        )

    # Create a one-row DataFrame for the new test results
    # Because each day has a single row of test results, we can use the dates\
    # as the row indices
    results_df = pd.DataFrame(
        [[ internet_speeds[0], internet_speeds[1], internet_speeds[2] ]],
        columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"],
        index=[date_today]
    )

    # Append the new results to the DataFrame that contains the dataset
    updated_df = csv_dataset.append(results_df, sort=False)
    # Keep only the last row of test results for each duplicate date\
    # https://stackoverflow.com/a/34297689/9263761
    # At the end, write the updated dataset, without duplicates, to the\
    # CSV file
    updated_df\
        .loc[~updated_df.index.duplicated(keep="last")]\
        .to_csv(csv_file_name, index_label="Date")


new_speeds = get_new_speeds()
update_csv(new_speeds)