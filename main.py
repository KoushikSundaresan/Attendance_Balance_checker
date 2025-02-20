import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

data = {
    "Subject": ["LOGIC", "DD", "OOPS", "DISCRETE", "FFA", "POE"],
    "Total Classes": [55, 60, 56, 57, 40, 36],
    "Attended Classes": [39, 53, 34, 36, 27, 24],
    "Max Days": [4, 4, 4, 4, 3, 3]
}

def calculate_daywise(total_classes, attended_classes, max_days):
    results = []
    for day in range(max_days + 1):
        skip = max_days - day
        total_attend = attended_classes + day
        total_skip = total_classes + max_days
        attendance = total_attend / total_skip
        results.append((day, skip, attendance * 100))
    return results

df = pd.DataFrame(data)

# Dash App
app = dash.Dash(__name__)
app.title = "Attendance Calculator"

app.layout = html.Div([
    html.H1("Attendance Calculator", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="subject-dropdown",
        options=[{"label": subject, "value": subject} for subject in df["Subject"]],
        value=df["Subject"].iloc[0],
        style={"width": "50%", "margin": "auto"}
    ),
    dcc.Slider(
        id="attend-slider",
        min=0,
        max=4,
        step=1,
        marks={i: str(i) for i in range(5)},
        value=2,
    ),
    dcc.Graph(id="attendance-graph"),
    html.Div(id="attendance-table", style={"width": "80%", "margin": "auto"})
])

@app.callback(
    [
        Output("attendance-graph", "figure"),
        Output("attendance-table", "children")
    ],
    [
        Input("subject-dropdown", "value"),
        Input("attend-slider", "value")
    ]
)
def update_graph_and_table(selected_subject, days_attended):
    row = df[df["Subject"] == selected_subject].iloc[0]
    total_classes = row["Total Classes"]
    attended_classes = row["Attended Classes"]
    max_days = row["Max Days"]

    calculations = calculate_daywise(total_classes, attended_classes, max_days)

    x_values = [f"Attend {day}, Skip {skip}" for day, skip, _ in calculations]
    y_values = [attendance for _, _, attendance in calculations]

    fig = go.Figure(data=[
        go.Bar(x=x_values, y=y_values, name=selected_subject, marker_color="lightskyblue")
    ])
    fig.update_layout(
        title=f"Attendance Projection for {selected_subject}",
        xaxis_title="Scenario",
        yaxis_title="Attendance %",
        yaxis_range=[0, 100]
    )

    table_rows = [
        html.Tr([
            html.Td("Days Attended"),
            html.Td("Days Skipped"),
            html.Td("Attendance %")
        ])
    ]
    for day, skip, attendance in calculations:
        table_rows.append(html.Tr([
            html.Td(day),
            html.Td(skip),
            html.Td(f"{attendance:.2f}%")
        ]))

    table = html.Table([
        html.Thead(html.Tr([
            html.Th("Scenario"),
            html.Th("Days Attended"),
            html.Th("Days Skipped"),
            html.Th("Attendance %")
        ])),
        html.Tbody(table_rows)
    ])

    return fig, table

if __name__ == "__main__":
    app.run_server(debug=True)
