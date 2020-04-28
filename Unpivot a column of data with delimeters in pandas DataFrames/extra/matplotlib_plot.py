import pandas as pd
from matplotlib import pyplot as plt

# Load the resulting dataset
data = pd.read_csv("final_data.csv")

# Group by social networks AND gender
gender_socials = data.groupby(by=["Used Social Networks", "Gender"]).count()

# Unstack the grouped DataFrame and plot it in a bar chart (the genders\
# are unstacked to the columns)
# This means the socials are in the X axis and the frequencies of each\
# social on the Y axis, broken down by gender
gender_socials.unstack().plot(kind="bar", rot=0)

# Add a title to the plot
plt.title("Social Networks by Gender")
# Update the legend to show only the gender options
plt.legend(set(data["Gender"]))
# Show the finalized plot
plt.show()
