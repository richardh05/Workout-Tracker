import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

def run_dashboard(database_path:str, host:str, port:int , debug:bool):
    """
    Initializes and runs the Dash web application.

    Args:
        database_path: Path to the SQLite database file.
        host: The host address for the Dash app to bind to.
        port: The port number for the Dash app to listen on.
        debug: Whether to run the Dash app in debug mode.
    """
    # Replace this with your own data source or SQLite query
    data = {
        'Date': [
            '2024-03-01', '2024-03-01', '2024-03-03',
            '2024-03-05', '2024-03-05', '2024-03-07',
            '2024-03-01', '2024-03-03', '2024-03-07'
        ],
        'Exercise': [
            'Bench Press', 'Bench Press', 'Bench Press',
            'Bench Press', 'Bench Press', 'Bench Press',
            'Deadlift', 'Deadlift', 'Deadlift'
        ],
        'Reps': [10, 8, 5, 6, 5, 3, 5, 4, 3],
        'Value': [60, 65, 80, 75, 85, 90, 100, 110, 120]  # weight
    }

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    # 🧠 Calculate Epley 1RM
    df['Epley1RM'] = df['Value'] * (1 + df['Reps'] / 30)

    # 📋 Prepare exercise options
    exercise_options = sorted(df['Exercise'].unique())

    # 🔧 Dash app setup
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Gym Progress Tracker – Epley 1RM Over Time"),
        
        html.Label("Select Exercise:"),
        dcc.Dropdown(
            id='exercise-dropdown',
            options=[{'label': ex, 'value': ex} for ex in exercise_options],
            value=exercise_options[0]
        ),
        
        dcc.Graph(id='progress-graph')
    ])

    @app.callback(
        Output('progress-graph', 'figure'),
        Input('exercise-dropdown', 'value')
    )
    def update_graph(selected_exercise):
        # Filter and aggregate
        filtered = df[df['Exercise'] == selected_exercise]
        summary = (
            filtered.groupby('Date')
            .agg(Max1RM=('Epley1RM', 'max'))
            .reset_index()
        )
        fig = px.line(summary, x='Date', y='Max1RM',
                    title=f'1RM Progress: {selected_exercise}',
                    markers=True,
                    labels={'Max1RM': 'Estimated 1RM (kg)'})
        fig.update_layout(xaxis_title="Date", yaxis_title="1RM (kg)")
        return fig
    app.run(host=host, port=port, debug=debug)

