import pandas as pd
from typing import List
# Base clode for splitting and unpivoting a Series
# https://stackoverflow.com/questions/19482970/get-list-from-pandas-dataframe-column-headers


def unpivot_delimited_series(
    series: pd.Series,
    delimiter: str
) -> pd.DataFrame:
    """
    Given a Series of delimited data, split each value into its own
    row, resulting in a Series with a two-level index. 
    The first level represents the index from the original Series, while
    the nested level represents each value that was found in a single row.

    Since these index columns will be needed later, the index is reset to
    create a new, one-level index, allowing access to the two-level index
    as normal columns. This means the end-result is a three-column
    DataFrame: two columns for the two-level index and a third for the
    unpivoted data.
    """

    # First, split each row's data at the specified delimiter (comma,\
    # semicolon, ...), putting each individual value on its own column.
    # Then, those individual values are unpivoted (stacked) so that the\
    # result is once again one single Series/column
    unpivoted_data = series\
        .apply( lambda series_row: pd.Series(series_row.split(delimiter)) )\
        .stack()

    # Since the above results in a multi-level index, now we need to\
    # reset the Series's index to be able to access those levels as\
    # normal columns
    unpivoted_data = unpivoted_data.reset_index()
    return unpivoted_data


def get_other_colum_names(
    source_df: pd.DataFrame,
    unpivoted_column: str
) -> List[str]:
    """
    Get a list with the name of all the existing columns in the source
    DataFrame, excluding the one that had data with delimiters.
    """

    # Get all the available column names
    other_columns = list(source_df.columns.values)
    # And remove the column that had delimited data
    other_columns.remove(unpivoted_column)
    return other_columns


def unpivot_delimited_data(
    source_df: pd.DataFrame,
    target_column: str,
    delimiter: str
) -> pd.DataFrame:
    """
    Given a DataFrame that has one column with delimited data, split that data
    and unpivot the individual values into their own rows.
    """

    # Get a DataFrame with the unpivoted data and respective two-level index
    unpivoted_series = unpivot_delimited_series(
        source_df[target_column], 
        ";"
    )

    # Reset the index of the source DataFrame so we can select the original\
    # index as a normal column
    source_df = source_df.reset_index()

    # Get a list of the source DataFrame columns excluding the one with\
    # delimited data
    source_df_other_columns = get_other_colum_names(
        source_df, 
        target_column
    )

    # Choose the columns from the source DataFrame to keep (this includes\
    # a column with the original index, called `index` after the index reset)
    source_data_to_merge = source_df[source_df_other_columns]

    # Merge the columns with non-delimited data to the unpivoted data
    # The merge is based on the original index of the source DataFrame, which\
    # is found as on the first-level index column of the unpivoted data\
    # (`level_0`) and in the old index column of the source data (`index`)
    merged_data = pd.merge(
        unpivoted_series,
        source_data_to_merge,
        how="inner",
        left_on="level_0",
        right_on="index"
    )

    # Rename the column with unpivoted data (it ends up being called 0 (zero))
    merged_data.rename(
        columns={0: target_column},
        inplace=True
    )

    # List with the names of the columns to keep (the only index kept is the\
    # post-reset index of the source DataFrame)
    columns_to_keep = source_df_other_columns + [target_column]
    columns_to_keep.remove("index")

    # Filter out the unwanted columns
    merged_data = merged_data[columns_to_keep]

    return merged_data


if __name__ == "__main__":
    # Load the original dataset
    data = pd.read_csv("sample_data.csv")

    # Split and unpivot the column with delimited data, keeping the\
    # complete DataFrame
    final_data = unpivot_delimited_data(
        data,
        "Used Social Networks",
        ";"
    )

    print(data)
    print(final_data)
