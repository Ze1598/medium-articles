from matplotlib import pyplot as plt

pairs_owned = [16, 9, 9, 6]
options = ["One", "Two", "Three", "Four+"]

# Plot the years of experience working with Python of 40 individuals in a bar chart
plt.barh(options, pairs_owned)

plt.title("Years of experience working with Python (n=40)")
plt.xlabel("Number of respondents")
plt.tight_layout()
plt.savefig("bar_hor_chart_demo.png")
plt.show()
