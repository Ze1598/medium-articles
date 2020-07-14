library(readr)
library(dplyr)
library(plotly)
library(tidyr)
library(stringr)

data <- read_csv("sample_data.csv")

# Split and unpivot
# --------------------------------------
max_split_cols <- max(mapply(str_count, data$`Used Social Networks`, ";"), na.rm = TRUE) + 1

sep_into_cols <- unname(mapply(paste, "Col", 1:max_split_cols, sep = ""))
(mapply(paste, "Col", 1:max_split_cols, sep = ""))

# Split the individual values of each row into their own column
separated_data <- data %>%
  separate(`Used Social Networks`, sep_into_cols, sep = ";", fill = "right")

# Unpivot the columns of individual options into a single column
# Column names go into "TempCols", values go into "Used Social Networks"
unpivot_wide_data <- separated_data %>%
  pivot_longer(
    sep_into_cols,
    names_to = "TempCols",
    values_to = "Used Social Networks",
    values_drop_na = TRUE
  )

# Remove the column with the names of the temporary columns
unpivot_wide_data <- unpivot_wide_data %>%
  select(-TempCols)
# --------------------------------------  


# Count frequencies
# --------------------------------------
# Count the frequency of each social network in the "Used Social Networks" column
data_counts <- unpivot_wide_data %>%
  group_by(`Used Social Networks`) %>%
  summarize(Frequency = n())

# Order the data by descending order of the frequency
data_counts <- data_counts[
  order(data_counts$Frequency, decreasing = TRUE)
  ,]
# --------------------------------------


# Plot column chart
# --------------------------------------
# Order the X axis by the current order of the values in the "Frequency" column
fig <- plot_ly(data_counts) %>%
  add_bars(
    x = ~ `Used Social Networks`,
    y = ~ Frequency) %>%
  layout(
    title = "Users of Social Networks",
    xaxis = list(
      title = "Social Networks",
      categoryorder = "array",
      categoryarray = data_counts$Frequency
    ),
    yaxis = list(title = "Users")
  )
fig
# --------------------------------------


# Clear environment variables
rm(list = ls())
