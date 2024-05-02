import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_player

external_stylesheets = ['/home/julia/Dash/style.css']

app = dash.Dash(__name__)

app_layout = html.Div([

    html.H1("Dashboard de Futebol", style={'textAlign': 'center','color':'white','margin':'0','padding':'10'}),

    html.Div([
        html.Div([
            dcc.RadioItems(
                id='team-selection',
                options=[
                    {'label': 'Time 1', 'value': 'team1'},
                    {'label': 'Time 2', 'value': 'team2'}
                ],
                value='team1',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '33%', 'display': 'inline-block', 'textAlign': 'center','color':'white'}),

        html.Div([
            dcc.Dropdown(
                id='player-dropdown',
                options=[
                    {'label': f'Jogador {i+1}', 'value': f'p{i+1}'} for i in range(96)
                ],
                value='p1',
                style={'width': '150px', 'margin': 'auto'}
            )
        ], style={'width': '33%', 'display': 'inline-block', 'textAlign': 'center'}),

        html.Div([
            dcc.Input(
                id='video-input',
                type='text',
                placeholder='Insira o link do vídeo',
                style={'width': '100%'}
            )
        ], style={'width': '33%', 'display': 'inline-block', 'textAlign': 'center'})
    ], style={'marginBottom': '20px', 'marginTop': '20px'}),

    html.Div([
        # Vídeo e Gráfico de Velocidade
        html.Div([

            html.Div([
                dash_player.DashPlayer(
                    id='movie_player',
                    url=dash.get_asset_url('qatar2022_argentina_x_france_tactical_cam_1080p_middle_field.mkv'),
                    controls=True,
                    style={'width': '48%', 'height': '100%', 'objectFit': 'contain', 'marginRight': '10px', 'marginLeft': '1%'}
                ),
                dash_player.DashPlayer(
                    id='movie_player_traq',
                    url=dash.get_asset_url('qatar2022_argentina_x_france_tactical_cam_1080p_middle_field_highlighted.mp4'),
                    controls=True,
                    playing=False,  
                    style={'width': '48%', 'height': '100%', 'objectFit': 'contain', 'marginLeft': '10px', 'marginRight': '1%'}
                )

            ], style={'display': 'flex', 'justifyContent': 'space-around', 'textAlign': 'center', 'marginTop': '20px', 'marginBottom': '20px'}),

            html.Span(id='video-current-time', style={'text-align': 'center', 'margin-top': '10px','color':'white'}),
            html.Button("Play", id="play-button", n_clicks=0, style={'margin': 'auto', 'display': 'block', 'marginTop': '20px'}),

            html.Div([
                # Mapa de dispersão
                html.Div([
                    dcc.Graph(id='scatter-plot', style={'width': '100%', 'margin': 'auto'})
                ])
            ], style={'textAlign': 'center', 'paddingTop': '20px','display': 'flex','justifyContent': 'center','alignItems': 'center' }),

            # Gráfico de velocidade
            html.Div([
                html.Div(id='velocity-chart-container', style={'min-height': '340px','max-width': '640px','width': '48%', 'display': 'inline-block', 'textAlign': 'center', 'marginRight': '1%'}),
                html.Div(id='acceleration-chart-container', style={'min-height': '340px','max-width': '640px','width': '48%', 'display': 'inline-block', 'textAlign': 'center', 'marginLeft': '1%'})
            ], style={'display': 'flex', 'justifyContent': 'space-around', 'paddingTop': '20px', 'paddingBottom': '20px'})
        ])
    ], style={'textAlign': 'center'}),

],style={'textAlign': 'center','backgroundColor':'black', 'margin':'0px'} )

if __name__ == '__main__':
    app.run_server(debug=True)
