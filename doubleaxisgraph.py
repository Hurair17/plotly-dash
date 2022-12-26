import plotly.graph_objects as go
from plotly.subplots import make_subplots

class graph:
    def doubleaxisgraph(df):

        run = df[df.Runs>20000][['Player','Runs','Inns']].reset_index(drop='index')
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces Bar chart
        fig.add_trace(
            go.Bar(x=run['Player'], y=run['Runs'], name="Total Runs"),
            secondary_y=False,
        )
        # add traces scatter plot
        fig.add_trace(
            go.Scatter(x=run['Player'], y=run['Inns'], name="Total Inns"),
            secondary_y=True,
        )

        # Add figure title
        fig.update_layout(
            title_text="Players total Runs with Inns"
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Players Name")

        # Set y-axes titles
        fig.update_yaxes(title_text="Total Runs", secondary_y=False)
        fig.update_yaxes(title_text="Total Inns", secondary_y=True)

        return fig