# https://github.com/sivel/speedtest-cli
import speedtest
import pandas as pd
from datetime import datetime


def get_new_speeds() -> tuple:
    # Class for speed tests
    speed_test = speedtest.Speedtest()
    # Get the best server (the one with lowest latency)
    speed_test.get_best_server()

    # Get ping (miliseconds)
    ping = speed_test.results.ping
    # Perform download and upload speed tests (both come bits per second)
    download = speed_test.download()
    upload = speed_test.upload()

    # Convert download and upload speeds to megabits per second
    download_mbs = round(download / 1000000, 2)
    upload_mbs = round(upload / 1000000, 2)

    print(f"Ping: {ping} ms")
    print(f"Download: {download_mbs} Mb/s")
    print(f"Upload: {upload_mbs} Mb/s")

    return (ping, download_mbs, upload_mbs)


def update_csv(internet_speeds) -> None:
    # Get today's date in the form Month/Day/Year
    date_today = datetime.today().strftime("%m/%d/%Y")
    # Using a different name from the dataset loaded into Power BI to keep\
    # that dataset untouched
    csv_file_name = "internet_speeds_dataset.csv"

    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col=0)
    # If the file does not exist, create a new one
    except:
        # Create a new empty DataFrame with the necessary columns
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"]
        )
        # Code to create the new CSV with the empty dataset and load it\
        # right away
        '''
        # Create the CSV with the correct index column
        csv_dataset.to_csv(csv_file_name, index_label="Date")
        # Load the file
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
        '''

    # Create a one-row DataFrame to contain the new test results
    # The date can be used as row index because the dataset has only one\
    # row per day
    write_df = pd.DataFrame(
        [[
            internet_speeds[0],
            internet_speeds[1],
            internet_speeds[2]
        ]],
        columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"],
        index=[date_today]
    )

    # Append the DataFrame to the CSV
    # If the file already existed, it is overwritten. Otherwise, a new file\
    # is created
    csv_dataset.append(write_df, sort=False).to_csv(csv_file_name, index_label="Date")


if __name__ == "__main__":
    new_speeds = get_new_speeds()
    update_csv(new_speeds)
