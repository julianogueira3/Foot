import dash
from layouts import app_layout
from callbacks import (
    # update_velocity_chart,
    # update_acceleration_chart,
    update_scatter_plot,
    update_video_current_time,
    update_playing_state
)

app = dash.Dash(__name__)

app.layout = app_layout

# app.callback(
#     dash.dependencies.Output('velocity-chart-container', 'children'),
#     [dash.dependencies.Input('player-dropdown', 'value'),
#      dash.dependencies.Input('movie_player', 'currentTime')]
# )(update_velocity_chart)

# app.callback(
#     dash.dependencies.Output('acceleration-chart-container', 'children'),
#     [dash.dependencies.Input('player-dropdown', 'value'),
#      dash.dependencies.Input('movie_player', 'currentTime')]
# )(update_acceleration_chart)

app.callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('player-dropdown', 'value'),
     dash.dependencies.Input('movie_player', 'currentTime')]
)(update_scatter_plot)

app.callback(
    dash.dependencies.Output('video-current-time', 'children'),
    [dash.dependencies.Input('movie_player', 'currentTime')]
)(update_video_current_time)

app.callback(
    [
        dash.dependencies.Output('movie_player', 'playing'),
        dash.dependencies.Output('movie_player_traq', 'playing')
    ],
    [dash.dependencies.Input('play-button', 'n_clicks')],
    [
        dash.dependencies.State('movie_player', 'playing'),
        dash.dependencies.State('movie_player_traq', 'playing')
    ]
)(update_playing_state)

if __name__ == '__main__':
    app.run_server(debug=True)
