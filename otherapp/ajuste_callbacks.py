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

def calculate_velocity_and_acceleration(player_id, current_time, df):
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
            if t >= current_time:  # Ajuste aqui para considerar t >= current_time
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
                x_prev, y_prev, t_prev = x, y, t
                listavt.append(vt)
                listaa.append(a)
                listatime.append(count)
            count += 1
        else:
            count += 1  

    return listatime, listavt, listaa

def update_velocity_chart(player_column, current_time, df):
    player_id = f"{int(player_column[1]):02d}"
    _, velocidade, _ = calculate_velocity_and_acceleration(player_id, current_time, df)

    tempo = list(range(len(velocidade)))  # Convertendo range para lista

    data = [go.Scatter(x=tempo, y=velocidade, mode='lines', name='Velocity')]
    layout = go.Layout(title='Gráfico de Velocidade', xaxis=dict(title='Tempo'), yaxis=dict(title='Velocidade'))

    return {'data': data, 'layout': layout}

def update_acceleration_chart(player_column, current_time, df):
    player_id = f"{int(player_column[1]):02d}"
    _, _, aceleracao = calculate_velocity_and_acceleration(player_id, current_time, df)

    tempo = list(range(len(aceleracao)))  # Convertendo range para lista

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tempo, y=aceleracao, mode='lines', name='Acceleration'))
    fig.update_layout(title='Gráfico de Aceleração', xaxis_title='Tempo', yaxis_title='Aceleração')

    return fig

def update_scatter_plot(player_column, current_time):
    player_id = player_column[1] if int(player_column[1]) > 9 else f"{int(player_column[1]):02d}"
    x = []
    y = []
    tempo = []  
    for index, row in df.iterrows():
        x_val, y_val = extract_xy(row[f'p{player_id}'])
        if x_val is not None and y_val is not None and row['t'] <= current_time:
            x.append(x_val)
            y.append(y_val)
            tempo.append(row['t'])  

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', marker=dict(color='blue', size=10), name='Path'))
    fig.update_layout(
        title=f'Mapa de Dispersão do Jogador {player_id}',
        xaxis_title='X',
        yaxis_title='Y',
        width=800,  
        height=600,  
        template='plotly_white',
        xaxis=dict(range=[100, 400]),  
        yaxis=dict(range=[400, 600]),  
    )

    return fig

def extract_xy(cell_value):
    try:
        xy = eval(cell_value)
        return xy[0], xy[1]
    except:
        return None, None

def update_video_current_time(current_time):
    formatted_time = "{:02}:{:02}".format(int(current_time / 60), int(current_time % 60))
    return f"Tempo Atual: {formatted_time}"

def update_playing_state(n_clicks, current_playing_state, current_playing_state_traq):
    if n_clicks % 2 == 1: 
        return True, True  
    else:
        return False, False  

