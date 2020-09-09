import pandas as pd
import numpy as np

# Current employee dataset
original = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["Michael", "Jim", "Pam", "Dwight"],
    "age": [46, 35, 35, 38],
    "email": ["michael@dundermifflin.com", "jim@dundermifflin.com", "pam@dundermifflin.com", "dwight@dundermifflin.com"],
    "in_company": [True, True, True, True]
})
# The latest employee listing. It has two new employees (ids 5 and 6)\
# and is missing one person from the previous data (id 2). Some employees\
# also updated their data
new_data = pd.DataFrame({
    "id": [1, 3, 4, 5, 6],
    "name": ["Michael", "Pam", "Dwight", "Kevin", "Stanley"],
    "age": [47, 36, 38, 41, 55],
    "email": ["michael@dundermifflin.com", "pam@dundermifflin.com", "dwight@schrutefarms.com", "kevin@dundermifflin.com", "stanley@dundermifflin.com"],
    "in_company": [True, True, True, True, True]
})

# Update the employment status of employees missing in the new listing
original.loc[~original["id"].isin(new_data["id"]), "in_company"] = False

# Append the new listing to the original to create a single DF
updated = original.append(new_data, ignore_index=True)
# For the employees in both DFs, keep only their latest information\
# (rows are considered duplicate based on the "id")
updated = updated.drop_duplicates(["id"], keep="last")
# Sort the employees by their id
updated.sort_values("id", inplace=True)
# Reset the DF index after all the transformations (don't keep the\
# previous index a.k.a. `drop=True`)
updated.reset_index(drop=True, inplace=True)

print("---Updated employee data:\n", updated)
