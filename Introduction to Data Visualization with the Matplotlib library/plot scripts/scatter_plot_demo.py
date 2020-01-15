from matplotlib import pyplot as plt

x_coords = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
fav_nums = [9, 37, 45, 32, 46, 56, 28, 9, 16, 68, 64, 100, 25, 1, 59, 50, 31, 96, 13, 76]

# Plot the favorite numbers of twenty individuals
plt.scatter(x_coords, fav_nums, marker="x", color="red")

plt.ylabel("Favorite number")
# Hide the ticks of the X axis
plt.xticks([])
plt.title("Favorite number of twenty individuals")
plt.tight_layout()
plt.savefig("scatter_plot_demo.png")
plt.show()
