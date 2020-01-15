from matplotlib import pyplot as plt

# Slice values, labels and colors
slices = [1, 9, 6, 7, 8]
labels = ["Dwight", "Pam", "Robert", "Michael", "Jim"]
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#cccccc"]

# Plot the number of movies watched in 2019 by five people, in a pie chart
# Show the percentages of each slice, with two decimal places
plt.pie(slices, labels=labels, colors=colors, autopct="%1.2f%%")

plt.title("Number of movies watched at the cinema in 2019")
plt.tight_layout()
plt.savefig("pie_chart_demo.png")
plt.show()
