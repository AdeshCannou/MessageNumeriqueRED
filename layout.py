import os
import time
import json
import dash
import json
from dash import Dash, html, Input, Output, ctx, callback, State, dcc, MATCH, ALL, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    
    clients = dbc.RadioItems(
            id="client",
            inline=True,
            value=1)

    offcanvas = html.Div(
        [
            dbc.Button(
                "Choix des plugins", id="open-offcanvas", n_clicks=0,color="light", className="me-1",style={"margin-top": "15px"}
            ),
            dbc.Offcanvas(
                dcc.Checklist( id="plugins",options=[{'label': 'Noyau', 'value': 'noyau', 'disabled': True},
                                                      {'label': 'Film', 'value': 'film'},
                                                      {'label': 'Friandise', 'value': 'friandise'}], value=["noyau"]),
                id="offcanvas",
                title="Choix des plugins",
                is_open=True,
                placement="top",
            ),
        ]
    )

    return dbc.Row([dbc.Col(title, md=6),dbc.Col(offcanvas, md=2) ,dbc.Col(clients, md=3)])

def textbox(text, client):
    
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if client == 1:
        style["margin-left"] = "auto"
        style["margin-right"] = 0
        color = "primary"

    elif client == 2:
        style["margin-left"] = 0
        style["margin-right"] = "auto"
        color = "success"

    else:
        raise ValueError("Incorrect option for `client`.")

    if "Sondage" in text:
        survey = text.split("Sondage")[1].replace(" ", "/")
        return dbc.Card(f"{survey}", style=style, body=True, color=color, inverse=True)

    return dbc.Card(f"{text}", style=style, body=True, color=color, inverse=True)

# Define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.ZEPHYR])
server = app.server

# Define Layout
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 145px)",
        "flex-direction": "column-reverse",
    },
)


controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="Client A...", type="text"),
        dbc.Button("Submit", id="submit")
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[

        Header("Conversation", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        dcc.Store(id="store-message", data=""),
        conversation,
        controls,
        dbc.Alert(id='alert', color='danger', dismissable=True, is_open=False),
        dcc.Dropdown(
                    [{'label': 'Noyau', 'value': '', 'disabled': True},
                        {'label': 'Message', 'value': 'message'},
                        {'label': 'Date', 'value': 'date'},
                        {'label': 'Sondage', 'value': 'sondage'},
                        {'label': 'Nombre', 'value': 'nombre'},

                    ], placeholder="Selectionner option(s)",multi=True,id="select", value="message"
                )
           ,html.Div(
                        [
                            dcc.Input(id="new-item-input"),
                            html.Button("Ajouter la réponse", id="add-btn"),
                            html.Div(id="list-container-div"),
                            html.Button("Effacer le sondage", id="clear-done-btn"),
                            html.Div(id="totals-div"),
                            dcc.Store(id="keep-answers")
                        ],
                    id="survey-container",hidden=True)
    ],
)