from matplotlib import pyplot as plt

# Slice values, labels and colors
slices = [1, 9, 3, 3, 4]
labels = ["Management", "Sales", "Quality Assurance", "Accounting", "Human Resources"]
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#cccccc"]

# Plot the relative sizes of each department at a mock company
# Show the percentages of each slice, with two decimal places
plt.pie(slices, labels=labels, colors=colors, autopct="%1.2f%%")

plt.title("Size of departments at Company A")
plt.tight_layout()
plt.savefig("pie_chart_demo.png")
plt.show()
