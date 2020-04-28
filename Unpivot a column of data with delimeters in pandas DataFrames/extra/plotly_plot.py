import pandas as pd
import plotly.graph_objects as go

# Load the resulting dataset
data = pd.read_csv("final_data.csv")

# Group by social networks AND gender
gender_socials = data.groupby(by=["Used Social Networks", "Gender"]).count()

# Unstack the genders, leaving only the social networks on the index\
# (columns are now broken down by gender)
socials_gender_unstacked = gender_socials.unstack()

# Get the existing social networks
socials = socials_gender_unstacked.index.values
# Get the values for each gender
female = socials_gender_unstacked[("Respondent ID", "Female")]
male = socials_gender_unstacked[("Respondent ID", "Male")]
other = socials_gender_unstacked[("Respondent ID", "Other")]

# Create a Plotly Figure to produce a plot
fig = go.Figure()
# Add a Bar chart of social networks by the `Female` `Gender`
fig.add_trace(go.Bar(
    x=socials,
    y=female,
    name="Female"
))
# Add a Bar chart of social networks by the `Male` `Gender`
fig.add_trace(go.Bar(
    x=socials,
    y=male,
    name="Male"
))
# Add a Bar chart of social networks by the `Other` `Gender`
fig.add_trace(go.Bar(
    x=socials,
    y=other,
    name="Other"
))
# Format the chart
fig.update_layout(
    barmode="group",
    title_text="Social Networks by Gender",
    xaxis_title="Social Network",
    uniformtext_minsize=14,
    uniformtext_mode="hide",
    title_x=0.5,
    legend={
        "title": "Gender",
        "orientation": "h",
        "x": 0,
        "y": 1.1
    }
)
# Show the resulting chart
fig.show()
