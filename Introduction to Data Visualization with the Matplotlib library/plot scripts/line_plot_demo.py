from matplotlib import pyplot as plt

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
doubles = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
squares = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Plot the base numbers against their doubles and against their squares
plt.plot(nums, doubles, label="Doubles", color="red")
plt.plot(nums, squares, label="Squares", color="blue")

# Give a label to each axis
plt.xlabel("Number")
plt.ylabel("Result")
# Give a title to the graph
plt.title("Evolution of doubles and squares for the range [1,10]")
# By default the legend is drawn in the top left corner
plt.legend()
plt.tight_layout()
# Save the current plot as PNG file (need to save before `show()` otherwise\
# the plot is lost)
plt.savefig("line_plot_demo.png")
plt.show()