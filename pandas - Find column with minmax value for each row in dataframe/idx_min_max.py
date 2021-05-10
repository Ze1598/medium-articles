import pandas as pd

# Working data
data = [
    {
        "Symbol": "KLAC",
        "Company": "KLA Corporation",
        "Sector": "Information Technology",
        "Date": "2018-02-02",
        "Price": 99.11979699999999,
        #"Assignments": 2,
        "DistancesToClusterCenter no.0": 1.360256609384238,
        "DistancesToClusterCenter no.1": 1.6006314317690011,
        "DistancesToClusterCenter no.2": 0.7541492328804794,
        "DistancesToClusterCenter no.3": 1.5081092797555191,
        "DistancesToClusterCenter no.4": 1.5305044066664453,
        "DistancesToClusterCenter no.5": 1.6588949777953004,
        "DistancesToClusterCenter no.6": 1.7548327626939508,
        "DistancesToClusterCenter no.7": 1.6762755894931198,
        "DistancesToClusterCenter no.8": 1.345775444852537,
        "DistancesToClusterCenter no.9": 1.6720496207711137},
    {
        "Symbol": "ADM",
        "Company": "Archer-Daniels-Midland Company",
        "Sector": "Consumer Staples",
        "Date": "2017-08-14",
        "Price": 37.208633,
        #"Assignments": 1,
        "DistancesToClusterCenter no.0": 1.3486943217445082,
        "DistancesToClusterCenter no.1": 0.7179199883155732,
        "DistancesToClusterCenter no.2": 1.5854019756043016,
        "DistancesToClusterCenter no.3": 1.5016190340086706,
        "DistancesToClusterCenter no.4": 1.5052801018087034,
        "DistancesToClusterCenter no.5": 1.6816139760877844,
        "DistancesToClusterCenter no.6": 1.732138364833968,
        "DistancesToClusterCenter no.7": 1.6648399176920667,
        "DistancesToClusterCenter no.8": 1.3388687676479127,
        "DistancesToClusterCenter no.9": 1.6605598470834293
    }
]

# Create a DataFrame for the data
df = pd.DataFrame(data)

# List of names for the cluster distance columns
names = [f"DistancesToClusterCenter no.{i}" for i in range(0, 10)]

# Get the name of the column with the smallest distance for each row as a new column
df["ClusterAssignment"] = df[names].idxmin(axis="columns")
# Clean the values in the new column to have only the cluster number
df["ClusterAssignment"] = df["ClusterAssignment"].map(lambda value: value.split(".")[-1])

# Repeat the above logic, but this time look for the column with the largest value
df["MostDistantCluster"] = df[names].idxmax(axis="columns")
# Clean the values in the new column to have only the cluster number
df["MostDistantCluster"] = df["MostDistantCluster"].map(lambda value: value.split(".")[-1])

# Remove the individual cluster distance column
df = df.drop(names, axis="columns")
# Print the results
print(df)
print(df.columns)