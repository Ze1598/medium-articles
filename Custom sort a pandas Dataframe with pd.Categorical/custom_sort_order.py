import pandas as pd
import numpy as np

def generate_random_dates(num_dates: int) -> np.array:
	"""Generate a 1D array of `num_dates` random dates.
	"""
	start_date = "2020-01-01"
	# Generate all days for 2020
	available_dates = [np.datetime64(start_date) + days for days in range(365)]
	# Get `num_dates` random dates from 2020
	random_dates = np.random.choice(available_dates, size=100, replace=False)
	return random_dates

dates = generate_random_dates(100)
values = np.random.normal(size=100)
df = pd.DataFrame({"date": dates, "value": values})
# https://strftime.org/
df["year"] = [d.strftime("%y") for d in df["date"]]
df["month"] = [d.strftime("%B") for d in df["date"]]
df["day"] = [d.strftime("%d") for d in df["date"]]
print(df, "\n")

# First attempt: sorts months alphabetically
df.sort_values(by="month", inplace=True)
# Reset the index after sorting
df.reset_index(drop=True, inplace=True)
print(df, "\n")

# Second attempt with "month" as the category data type
months_categories = [
	"January", "February", "March", "April",
	"May", "June", "July", "August", "September",
	"October", "November", "December"
]
# Make "month" a proper categorical column, specifying the categories\
# and their order
df["month"] = pd.Categorical(df["month"], categories=months_categories)
# Exact same sorting function, but this time pandas knows the proper\
# sorting order
df.sort_values(by="month", inplace=True)
# Reset the index after sorting
df.reset_index(drop=True, inplace=True)

print(f"\"month\" data type after casting: {df['month'].dtype}\n")
print(df)