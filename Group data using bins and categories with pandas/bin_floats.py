import pandas as pd
import numpy as np
import plotly.express as px
from typing import List, Union


def bin_work_hours(work_hours_series: pd.Series) -> pd.Series:
    """
    Take a Series of work week hours (floats) and bin its vlaues into
    8-hour intervals (8-80, exclusive).
    """
    # Create the labels for the Series' bins. Each bin represents an\
    # interval of 8 hours (these are the "names" of the bins that will\
    # be created)
    work_hours_labels = [f"[{i}, {i+8})" for i in range(8, 73, 8)]

    # Create a bin for every 8 hours between the work hours of 8 and 80, exclusive\
    # (the bins are closed on left and open on right, i.e., the left side is\
    # inclusive and the right exclusive)
    work_hours_bins = pd.IntervalIndex.from_tuples(
        [(i, i+8) for i in range(8, 73, 8)],
        closed="left"
    )

    # Bin the Series, using the exact bins created before thanks to IntervalIndex.
    # `labels` tells the function to use custom bin labels instead of the bin\
    # intervals; `precision` specifies the rounding precision and `include_lowest`
    # indicates the first bin to be left-inclusive
    work_hours_binned = pd.cut(
        work_hours_series,
        work_hours_bins,
        labels=work_hours_labels,
        precision=2,
        include_lowest=True
    )

    # Sort the binned data in ascending order
    work_hours_binned.sort_values(ascending=True, inplace=True)
    # Change the values from categorical to string to be able to plot them
    work_hours_binned = work_hours_binned.astype("str")

    return work_hours_binned


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
    # Generate a 200-element-long Series of work week hours (floats) between 8 and\
    # 70, inclusive
    work_hours = pd.Series(np.random.random_sample(200,)) * 72 + 8

    # Bin the work week hours
    work_hours_binned = bin_work_hours(work_hours)

    # Plot an histogram with the frequency of each bin
    plot_histogram(
        work_hours_binned,
        10,
        "Work Week Hours binned",
        ["Work week hours", None]
    )
