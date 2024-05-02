import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import math
import base64
import matplotlib.pyplot as plt
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# Carregar imagem do campo e dados de coordenadas
campo_img = plt.imread('/home/julia/Dash/app/imagens/campo_corte.jpg')
df = pd.read_csv('/home/julia/Dash/data/coords.csv')

# Função para extrair as coordenadas utilizando eval
def extract_xy(cell_value):
    try:
        xy = eval(cell_value)
        return xy[0], xy[1]
    except:
        return None, None

# Função para calcular a velocidade e aceleração do jogador
def calculate_velocity_and_acceleration(player_id):
    count = 0
    linhas = len(df)
    listavt = []
    listaa = []
    listatime = []
    x_prev, y_prev, t_prev = 0, 0, 0  
    while count < linhas:
        x, y = extract_xy(df[f'p{player_id}'].iloc[count])  
        if x is not None and y is not None:
            t = df['t'].iloc[count]
            if count == 0:
                vx = 0
                vy = 0
                vt = 0
                a = 0
            else:
                vx = (x - x_prev) / (t - t_prev)
                vy = (y - y_prev) / (t - t_prev)
                vt = math.sqrt((vx ** 2) + (vy ** 2))
                a = vt / t
            count += 1
            x_prev, y_prev, t_prev = x, y, t
            listavt.append(vt)
            listaa.append(a)
            listatime.append(count)
        else:
            count += 1  

    return listatime, listavt, listaa

def update_velocity_chart(player_column):
    player_id = f"{int(player_column[1]):02d}" 
    tempo, velocidade, _ = calculate_velocity_and_acceleration(player_id)

    # Gráfico de velocidade
    velocity_fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tempo, velocidade)
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Velocidade')
    ax.set_title('Gráfico de Velocidade')
    velocity_buf = BytesIO()
    velocity_fig.savefig(velocity_buf, format='png')
    velocity_buf.seek(0)
    velocity_img_str = "data:image/png;base64," + base64.b64encode(velocity_buf.read()).decode('utf-8')
    velocity_chart = html.Img(src=velocity_img_str, style={'width': '100%'})

    return velocity_chart

def update_acceleration_chart(player_column):
    player_id = f"{int(player_column[1]):02d}"  
    tempo, _, aceleracao = calculate_velocity_and_acceleration(player_id)

    # Gráfico de aceleração
    acceleration_fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tempo, aceleracao)
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Aceleração')
    ax.set_title('Gráfico de Aceleração')
    acceleration_buf = BytesIO()
    acceleration_fig.savefig(acceleration_buf, format='png')
    acceleration_buf.seek(0)
    acceleration_img_str = "data:image/png;base64," + base64.b64encode(acceleration_buf.read()).decode('utf-8')
    acceleration_chart = html.Img(src=acceleration_img_str, style={'width': '100%'})

    return acceleration_chart


def update_scatter_plot(player_column):
    player_id = player_column[1]  
    if int(player_id) > 9:  
        player_id = int(player_id) 
    else:
        player_id = f"{int(player_id):02d}"  
    x = []
    y = []
    tempo = []  
    for index, row in df.iterrows():
        x_val, y_val = extract_xy(row[f'p{player_id}'])
        if x_val is not None and y_val is not None:
            x.append(x_val)
            y.append(y_val)
            tempo.append(row['t'])  

    fig = go.Figure()

    fig.update_layout(
        title=f'Mapa de Dispersão do Jogador {player_id}',
        xaxis_title='X',
        yaxis_title='Y',
        width=800,
        height=600,
        template='plotly_white',
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(
                        label="▶",
                        method="animate",
                        args=[None, {"frame": {"duration": 0, "redraw": True}, "fromcurrent": True}],
                    ),
                    dict(
                        label="⏸️",
                        method="animate",
                        args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    ),
                ],
                showactive=False,
                direction="left",  
                x=-0.3,  
                y=-0.2,  
                xanchor="left",
                yanchor="bottom",
            ),
        ],
        sliders=[ 
            dict(
                active=0,
                steps=[
                    dict(label=str(i), method="animate", args=[
                        None, {"frame": {"duration": i * 100, "redraw": True}, "mode": "immediate"}]) for i in range(1, 11)
                ],
                pad={"t": 50},
                len=0.9,
                x=0.5, 
                y=-0.3,  
                xanchor="center",
                yanchor="bottom",
                transition=dict(duration=0),
            ),
        ],
    )

    frames = [go.Frame(data=go.Scatter(x=x[:i+1], y=y[:i+1], mode='markers', marker=dict(color='blue', size=10), name='Path')) for i in range(len(x))]

    fig.frames = frames

    fig.add_trace(go.Scatter(x=[x[0]], y=[y[0]], mode='markers', marker=dict(color='blue', size=10), name='Path'))

    return fig

def update_video_current_time(current_time):
    if current_time is not None:
        formatted_time = "{:02}:{:02}".format(int(current_time / 60), int(current_time % 60))
        return f"Tempo Atual: {formatted_time}"
    else:
        return "Tempo Atual: --:--" 

def update_playing_state(n_clicks, current_playing_state, current_playing_state_traq):
    if n_clicks % 2 == 1:  
        return not current_playing_state, not current_playing_state_traq
    else:
        return current_playing_state, current_playing_state_traq


