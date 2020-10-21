import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV (load date data as proper date types)
df = pd.read_csv("page_views.csv")
df["date"] = pd.to_datetime(df["date"])
# Sort the DF from oldest to most recent recordings
df.sort_values(by="date", inplace=True)
# Use the column of dates as the DF's index
df.set_index(["date"], inplace=True)

# Remove possible outliers (i.e, top and bottom 2.5 percentiles)
df = df[
    (df["page_views"] > df["page_views"].quantile(0.025)) &
    (df["page_views"] < df["page_views"].quantile(0.975))
]

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
# Create a column that has the year of each date recording
df["year"] = df.index.year
# Create a column that has the month (1-12) of each date recording
df["month"] = df.index.month
# Map the month integers to their proper names
df["month"] = df["month"].apply(
    lambda data: months[data-1]
)
# Make this a categorical column so it can be sorted by the order of values\
# in the `months` list, i.e., the proper month order
df["month"] = pd.Categorical(df["month"], categories=months)

# Pivot the DF so that there's a column for each month, each row\
# represents a year, and the cells have the mean page views for the\
# respective year and month
df_pivot = pd.pivot_table(
    df,
    values="page_views",
    index="year",
    columns="month",
    aggfunc=np.mean
)
# Plot a bar chart using the DF
ax = df_pivot.plot(kind="bar")
# Get a Matplotlib figure from the axes object for formatting purposes
fig = ax.get_figure()
# Change the plot dimensions (width, height)
fig.set_size_inches(7, 6)
# Change the axes labels
ax.set_xlabel("Years")
ax.set_ylabel("Average Page Views")

# Use this to show the plot in a new window
# plt.show()
# Export the plot as a PNG file
fig.savefig("page_views_barplot.png")
