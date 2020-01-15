from matplotlib import pyplot as plt
import numpy as np

days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# Need to save the data for the Y axis as NumPy arrays because the\
# `fill_between()` method needs to receive arrays instead of lists
company_sales = np.array([2, 6, 9, 12, 8, 15, 20, 32, 27, 30])
competition_sales = np.array([1, 2, 4, 5, 13, 12, 18, 22, 34, 38])

plt.plot(days, company_sales, color="blue", label="Company A")
# Plot the competition with a dashed black line
plt.plot(days, competition_sales, linestyle="--", color="black", label="Competition")

# Given the plot of the sales of the company and its competition, fill the\
# area between both plots where the company sold more than its competition
plt.fill_between(
    days, company_sales, competition_sales,
    where=(company_sales > competition_sales),
    interpolate=True,
    color="green",
    alpha=0.25,
    label="Company A sold more"
)

# Given the plot of the sales of the company and its competition, fill the\
# area between both plots where the competition sold more as much as the\
# company
plt.fill_between(
    days, competition_sales, company_sales,
    where=(company_sales <= competition_sales),
    interpolate=True,
    color="red",
    alpha=0.25,
    label="Competition sold more"
)

plt.title("Company A vs Competition sales")
plt.xlabel("Day")
plt.ylabel("Number of sales (thousands)")
plt.legend()
plt.savefig("fill_between_demo.png")
plt.show()
