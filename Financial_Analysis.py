import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import yfinance as yf
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import pytz
import yfinance as yf
from datetime import datetime as dt

load_figure_template("minty")

lista = ["PETR4.SA", "GOLL4.SA", "JBSS3.SA", "CMIN3.SA"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server

app.layout = html.Div(children=[
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H2("Ações"),
                dcc.Dropdown(lista,
                             lista[0],
                             id="DropdownAções")
            ])

        ], sm=1),
        dbc.Col([
            dbc.Row([dcc.Graph(id="Grafico")]),
            dbc.Row([dcc.Graph(id="Grafico2")])
        ], sm=11)
    ])
])



@app.callback([Output("Grafico", "figure"),
               Output("Grafico2", "figure")],
              [Input("DropdownAções", "value")])

def fun(Acao):
    tz = pytz.timezone("America/New_York")
    start = tz.localize(dt(2013, 1, 1))
    end = tz.localize(dt(2023, 11, 16))
    df = yf.download(Acao, start, end, auto_adjust=True)["Close"]
    df = pd.DataFrame(df).reset_index()
    df.columns = ["Data", "Fechamento"]
    da = yf.Ticker(Acao).history(period="max")


    fig_evolucao = px.line(df, x="Data", y="Fechamento")
    fig_ganho = px.line(da, x=da.index, y="Dividends")

    return fig_evolucao, fig_ganho


if __name__ == "__main__":
    app.run_server(port=8052, debug=True)
