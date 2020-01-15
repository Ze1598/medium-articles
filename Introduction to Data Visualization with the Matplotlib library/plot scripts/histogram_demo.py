from matplotlib import pyplot as plt

ages = [83, 50, 88, 31, 37, 52, 81, 58, 23, 60, 51, 62, 36, 95, 64, 59, 91, 70, 35,
        94, 61, 65, 96, 21, 95, 78, 99, 33, 29, 35, 29, 98, 54, 48, 97, 41, 29, 82,
        67, 55, 37, 99, 20, 69, 70, 98, 88, 41, 30, 58, 96, 33, 25, 52, 40, 69, 40,
        32, 50, 51, 64, 57, 75, 87, 37, 37, 82, 68, 65, 96, 45, 27, 52, 86, 51, 45,
        52, 67, 72, 98, 84, 76, 43, 26, 44, 41, 58, 19, 84, 21, 87, 46, 84, 76, 61,
        74, 32, 58, 66, 29]
# Bin edges (class intervals)
bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Plot the ages of 100 people, using the specified class intervals
plt.hist(ages, bins=bins, color="red", edgecolor="black")

plt.title("Distribution of ages in a group of 100 people")
plt.xlabel("Ages")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("histogram_demo.png")
plt.show()
