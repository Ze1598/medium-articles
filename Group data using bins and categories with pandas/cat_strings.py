import pandas as pd
import numpy as np
import plotly.express as px
from typing import List, Union


def create_evaluations(
    categories: List[str],
    mapping_values: List[str],
    length: int
) -> pd.Categorical:
    """
    Create a Series of 200 randomly picked evaluations, sorted according to
    the order of the `options`. However, before returning the Categorical
    data, replace the evaluation options by the corresponding mapping values.
    """
    # Pick 200 random evaluations and create a Categorical Series for that\
    # data. Passing the options as the `categories` ensures the order of\
    # those options to be kept when sorting
    evaluations = pd.Categorical(
        np.random.choice(categories, (length,)),
        categories=categories
    )

    # The values are sorted from "terrible" to "excellent", just like in the\
    # `options` list
    evaluations.sort_values(inplace=True)

    # Map the categorical nominal values to categorical numerical values\
    # (by creating a dictionary that pairs evaluation options to the\
    # corresponding mapping value)
    evaluations = evaluations.map({
        category: map_value for category, map_value in zip(categories, mapping_values)
    })

    return evaluations


def plot_column_chart(
    data_series: pd.Categorical,
    x_labels: List[str],
    title: str,
    axes_titles: List[Union[str, None]]
) -> None:
    """
    Plot the evaluation options' frequencies in a column chart.
    """
    # Change the categories' names to the desired X axis labels
    data_series = data_series.map({
        series_value: x_label for series_value, x_label in zip(data_series.unique(), x_labels)
    })

    # Plot the evaluations against their frequencies
    fig = px.bar(
        x=data_series.unique(),
        y=data_series.value_counts(),
        title=title
    )

    # Change the axes' titles
    fig.update_layout(
        xaxis_title=axes_titles[0],
        yaxis_title=axes_titles[1]
    )

    # Adjust the font and center the title
    fig.update_layout(
        uniformtext_minsize=14,
        uniformtext_mode="hide",
        title_x=0.5
    )

    # Show the finalized plot
    fig.show()


if __name__ == "__main__":
    # Evaluation options
    options = ["terrible", "bad", "so-so", "good", "excellent"]
    # Mapping values
    map_options = [1, 2, 3, 4, 5]

    # Create a Series of 200 randomly picked evaluations, sorted according to\
    # the order of the `options`
    evaluations = create_evaluations(options, map_options, 200)

    # Plot a column chart with the frequency of each option
    plot_column_chart(
        evaluations,
        options,
        "Evaluations' frequency",
        ["Evaluations", None],
    )
