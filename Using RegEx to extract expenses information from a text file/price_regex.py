import re
import datetime
import pandas as pd

PATTERN = r'(^([\d]+)([\.]?)([\d]*))( - )(.*)'

# Load text
with open("expenses.txt", "r") as f:
	expenses_txt = f.readlines()
# Put all the lines into a single string
whole_txt = "".join(expenses_txt)

# Find all the expense matches
matches = re.findall(PATTERN, whole_txt, flags=re.MULTILINE)
# Extract the relevant match information
expenses = [ [m[5], m[0]] for m in matches ]

# Create a DF for the expenses
df = pd.DataFrame(data=expenses)
# Reset the index so we have an actual column for it
df.reset_index(inplace=True)
# Rename the columns
df.columns = ["ExpenseID", "Name", "Cost"]
# Increase all IDs so they start at 1
df["ExpenseID"] += 1
# Export it as a CSV
df.to_csv("expenses.csv", index=False)