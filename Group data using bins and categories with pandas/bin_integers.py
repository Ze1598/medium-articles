import pandas as pd
import numpy as np
import plotly.express as px
from typing import List, Union


def bin_ages(age_series: pd.Series) -> pd.Series:
    """
    Take a Series of ages (integers) and bin its values into ten 10-year
    bins (0-100, exclusive).
    """
    # Create the labels for the Series' bins. Each bin represents an\
    # interval of 10 years (these are the "names" of the bins that will\
    # be created)
    age_labels = [f"[{i}, {i+10})" for i in range(0, 91, 10)]

    # Create a bin for every 10 years between the age of 0 and 100, exclusive\
    # (the bins are closed on left and open on right, i.e., the left side is\
    # inclusive and the right exclusive)
    age_bins = pd.IntervalIndex.from_tuples(
        [(i, i+10) for i in range(0, 91, 10)],
        closed="left"
    )

    # Bin the Series, using the exact bins created before thanks to IntervalIndex.
    # `labels` tells the function to use custom bin labels instead of the bin\
    # intervals; `precision` specifies the rounding precision and `include_lowest`
    # indicates the first bin to be left-inclusive
    ages_binned = pd.cut(
        age_series,
        age_bins,
        labels=age_labels,
        precision=0,
        include_lowest=True
    )

    # Sort the binned data in ascending order
    ages_binned.sort_values(ascending=True, inplace=True)
    # Change the values from categorical to string to be able to plot them
    ages_binned = ages_binned.astype("str")

    return ages_binned


def plot_histogram(
    data_series: pd.Series,
    nbins: int,
    title: str,
    axes_titles: List[Union[str, None]]
) -> None:
    """
    Plot an histogram through the Plotly Express API.
    """
    # Plot the histogram
    fig = px.histogram(
        x=data_series,
        nbins=nbins,
        title=title
    )

    # Change the axes' titles
    fig.update_layout(
        xaxis_title=axes_titles[0],
        yaxis_title=axes_titles[1]
    )

    # Adjust the font, remove horizontal gaps between the bins and center the title
    fig.update_layout(
        uniformtext_minsize=14,
        uniformtext_mode="hide",
        bargap=0,
        title_x=0.5
    )

    # Show the finalized plot
    fig.show()


if __name__ == "__main__":
    # Generate a 200-element-long Series of ages (integers) between 10 and\
    # 99, inclusive
    ages = pd.Series(np.random.randint(low=0, high=99, size=200))

    # Bin the ages
    ages_binned = bin_ages(ages)

    # Plot an histogram with the frequency of each bin
    plot_histogram(
        ages_binned,
        10,
        "Ages binned",
        ["Ages", None]
    )
