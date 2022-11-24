# Author Khushnud Boqiev

# Importing libariries
import dash
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import pandas as pd
from plotly.graph_objs import *

# Index(['Country', 'State', 'Time_Period', 'Outcome', 'Date'], dtype='object')
df = pd.read_excel("assets/dashboard.xlsx")

states = df.State.unique().tolist()
outcomes = df.Outcome.unique().tolist()
states.insert(0, "all")
outcomes.insert(0, "all")
sdate = df.Date.min()
edate = df.Date.max()


def filter_date(outcome, state, start_date, end_date):

    global df, total_calls, total_success, total_failure, dfsd, call_bystate, success_bystate, failure_bystate, totac, totsuc, totaction, totsuccess, new_df

    df = pd.read_excel("assets/dashboard.xlsx")

    if outcome == "all" and state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    elif outcome == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State == state]
    elif state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.Outcome == outcome]
    else:
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State == state]
        df = df[df.Outcome == outcome]

    # 1- Total number of calls per date
    total_calls = df.groupby("Date")["Outcome"].count()
    # 2- Total number of Success per date
    total_success = df[df["Outcome"] == "Success"].groupby("Date")["Outcome"].count()
    # 3- Total number of failures per date
    total_failure = df[df["Outcome"] == "Failure"].groupby("Date")["Outcome"].count()
    dfsd = total_calls[total_success.index]
    dfsd = total_success.values * 100 / dfsd

    call_bystate = df.groupby("State")["Outcome"].count().reset_index()

    # Total number of Success by state
    success_bystate = (
        df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count().reset_index()
    )
    # print(success_bystate)

    # Total number of failures by state
    failure_bystate = (
        df[df["Outcome"] == "Failure"].groupby("State")["Outcome"].count().reset_index()
    )

    totac = df.groupby("State")["Outcome"].count().reset_index()
    totsuc = (
        df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count().reset_index()
    )

    # best = dfm["ratio"].max()
    # best = dfm.loc[dfm["ratio"].idxmax()]

    totaction = df.groupby("State")["Outcome"].count()
    totsuccess = df[df["Outcome"] == "Success"].groupby("State")["Outcome"].count()

    df["Time_Period"] = [
        "0" + year if len(year) < 11 else year for year in df["Time_Period"]
    ]
    new_df = (
        df[df["Outcome"] == "Success"]
        .groupby("Time_Period")["Outcome"]
        .count()
        .reset_index()
    )


# --------------------------------------EX 1 ----------------------------------------------------------------
def q1():
    fig_total = px.line(total_calls, title="Total Calls")
    fig_total.add_scatter(
        x=total_success.index, y=total_success.values, mode="lines", name="Success"
    )
    fig_total.add_scatter(
        x=total_failure.index, y=total_failure.values, mode="lines", name="Failure"
    )
    fig_total.add_scatter(x=dfsd.index, y=dfsd.values, mode="lines", name="Ratio%")

    return fig_total


# -------------------------------------EX 2 -----------------------------------------------------------------
def q2():
    figure = {
        "data": [
            {
                "x": call_bystate.State,
                "y": call_bystate.Outcome,
                "type": "bar",
                "name": "Total",
            },
            {
                "x": failure_bystate.State,
                "y": failure_bystate.Outcome,
                "type": "bar",
                "name": "Failure",
            },
            {
                "x": success_bystate.State,
                "y": success_bystate.Outcome,
                "type": "bar",
                "name": "Success",
            },
        ],
        "layout": {
            "title": "Success and Failure by State",
            "legend_title": "Success & Failure",
            "xaxis": {"title": "State"},
            "yaxis": {"title": "number of calls"},
        },
    }
    return figure


# -------------------------------------Ex 3 ---------------------------------------------------------
def q3():
    fig_pie = px.pie(
        names=["Success", "Failure", "Time Out"],
        values=[
            df[df["Outcome"] == "Success"].shape[0],
            df[df["Outcome"] == "Failure"].shape[0],
            df[df["Outcome"] == "Time out"].shape[0],
        ],
        title="succes vs failure vs timeout",
    )
    return fig_pie


# ---------------------------------------------EX 4 -----------------------------------------------------------------
def q4():
    try:
        dfm = pd.merge(totac, totsuc, on="State").fillna(0)
        dfm["ratio"] = dfm["Outcome_y"] / dfm["Outcome_x"]
        dfm = dfm.sort_values(by="ratio", ascending=False)
        fig_bar = px.bar(x=dfm.State, y=dfm.ratio)
        return fig_bar
    except Exception as e:
        pass


# ---------------------------------------------Ex 5 ---------------------------------------------------------------------
def q5():
    trace1 = {
        "uid": "c3b30774-4638-4107-b886-a4b90742fe88",
        "hole": 0.86,
        "sort": False,
        "type": "pie",
        "domain": {"x": [0.2, 0.8], "y": [0.1, 0.9]},
        "marker": {"colors": ["#CB4335", "#2E86C1"]},
        "rotation": 180,
        "direction": "clockwise",
        "labels": totaction.index,
        "values": totaction.values,
    }
    trace2 = {
        "uid": "be0c29b2-21b2-4e89-b014-e917baf0b1f1",
        "hole": 0.9,
        "sort": False,
        "type": "pie",
        "domain": {
            "x": [0, 1],
            # "y": [0, 1]
        },
        "marker": {"colors": ["#EC7063", "#7f7f7f"]},
        "rotation": 180,
        "direction": "clockwise",
        "labels": totsuccess.index,
        "values": totsuccess.values,
        #   "showlegend": False
    }
    data = Data([trace1, trace2])
    layout = {"title": {"text": "Double piechart"}}
    fig_e = Figure(data=data, layout=layout)

    return fig_e


# ---------------------------------------------EX 6 ----------------------------------------------------------------------
def q6():
    try:
        fig_f = px.bar(new_df, x=new_df.Time_Period, y=new_df.Outcome)
        return fig_f
    except Exception as e:
        pass


# App
app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)


# Main layout
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.H2("DASH - CALLS ANALYSIS"),
                        html.P(
                            """Select different days using the date picker or by selecting
                            different states and outcomes from the dropdowns"""
                        ),
                        # Filter
                        html.Div(
                            
                            className="div-for-dropdown",
                            children=[
                                html.P("Outcomes:"),
                                dcc.Dropdown(
                                    id="outcomes",
                                    options=outcomes,
                                    value="all",
                                )
                            ],
                        ),
                        # Change to side by side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.P("States:"),
                                        dcc.Dropdown(
                                            id="states",
                                            options=states,
                                            value="all",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        html.P("Dates"),
                                        dcc.DatePickerRange(
                                            month_format="M-D-Y-Q",
                                            end_date_placeholder_text="M-D-Y-Q",
                                            id="date_range",
                                            start_date=sdate,
                                            end_date=edate,
                                            min_date_allowed=sdate,
                                            max_date_allowed=edate,
                                            style={"border": "0px solid black"},
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                # Graphs
                html.Div(
                    className="nine columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id="plot1",
                        ),

                        html.Div(
                            className="g1",
                            children=
                            [
                                dcc.Graph(
                                    id="plot2",
                                ),
                                dcc.Graph(
                                    id="plot3",
                                ),
                            ]
                        ),
                       
                        dcc.Graph(
                            id="plot4",
                        ),

                        html.Div(
                            className="g1",
                            children=
                            [
                                dcc.Graph(
                                    id="plot5",
                                ),
                                dcc.Graph(
                                    id="plot6",
                                ),
                            ]
                        ),
                      
    
                    ],
                ),
            ],
        )
    ],
)


# Function for changing the Exercices
@app.callback(
    [
        Output("plot1", "figure"),
        Output("plot2", "figure"),
        Output("plot3", "figure"),
        Output("plot4", "figure"),
        Output("plot5", "figure"),
        Output("plot6", "figure"),
    ],
    [
        Input("outcomes", "value"),
        Input("states", "value"),
        Input("date_range", "start_date"),
        Input("date_range", "end_date"),
    ],
)
def update_output(outcome, state, start_date, end_date):

    filter_date(outcome, state, start_date, end_date)

    return q1(), q2(), q3(), q4(), q5(), q6()


if __name__ == "__main__":
    app.run_server(debug=False)
