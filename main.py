import os
import time
import json
import dash
import json
from dash import Dash, html, Input, Output, ctx, callback, State, dcc, MATCH, ALL, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import datetime

from layout import app, textbox
from validate import validate_message

response_filter = {}
clientId = 1
placeholder = "Client A..."


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

@app.callback(
    Output("select", "options"),
    Input("plugins", "value"),
    State("select", "options")
)
def update_dropdown(plugins, current_options):
    base_options = [{'label': 'Noyau', 'value': '', 'disabled': True},
                    {'label': 'Message', 'value': 'message'},
                    {'label': 'Date', 'value': 'date'},
                    {'label': 'Couleur', 'value': 'couleur'},
                    {'label': 'Nombre', 'value': 'nombre'}]

    film_options = [{'label': 'Film', 'value': '', 'disabled': True},
                    {'label': 'Siège', 'value': 'siege'},
                    {'label': 'Créneau', 'value': 'creneau'},
                    {'label': 'Genre', 'value': 'genre'}]

    friandise_options = [{'label': 'Friandise', 'value': '', 'disabled': True},
                         {'label': 'Type Friandise', 'value': 'type_friandise'},
                         {'label': 'Taille Friandise', 'value': 'taille_friandise'}]

    new_options = base_options.copy()

    if "film" in plugins:
        new_options += film_options
    if "friandise" in plugins:
        new_options += friandise_options

    return new_options if new_options else base_options



@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [textbox(x.split(": ")[1], int(x.split(": ")[0][-1])) for x in chat_history.split("<split>")[:-1]]

@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    return ""

@app.callback(
    [Output("store-conversation", "data"),
     Output('alert', 'children'),
     Output('alert', 'is_open'),
     Output("user-input", "placeholder")],
    [Input("store-message", "data"),
     Input("submit", "n_clicks"),
     Input("client", "value"),
     Input("user-input", "n_submit")],
    [State("store-conversation", "data"),
     State('alert', 'is_open')]
)
def conversation_manager(store_message, n_clicks, client, enter, chat_history, is_open):
    global response_filter, clientId, placeholder
    alert_message = None
    alert_is_open = False
    input_message = ""
    

    if (ctx.args_grouping[1]["triggered"] and client) or (ctx.args_grouping[3]["triggered"] and client):
        store_message = json.loads(store_message)

        print(f'Former response filter: {response_filter}')
        print(f"Message received: {store_message}")


        if len(response_filter.keys()) > 0:
            print("Validation en cours")
            if "message" in store_message:
                if store_message["message"] != "" and validate_message(response_filter, store_message["message"]):
                    print("Message validé")
                    response_filter.clear()
                else:
                    print("Message invalide")
                    alert_message = "Réponse invalide. Veuillez répondre à la demande."
                    alert_is_open = True
                    return chat_history, alert_message, alert_is_open, placeholder
            else:
                alert_message = "Réponse invalide. Veuillez répondre à la demande."
                alert_is_open = True
                return chat_history, alert_message, alert_is_open, placeholder

        response_filter = store_message.copy()

        if "message" in response_filter:
            response_filter.pop("message")
            input_message = store_message["message"]
        else:
            input_message = ""
        
        print(f"New response filter: {response_filter}")
        
        for key, value in store_message.items():
            if key == "isCouleur":
                input_message += " [couleur]"
            elif key == "isNumber":
                input_message += " [nombre]"
            elif key == "isSiege":
                input_message += " [siege]"
            elif key == "isCreneau" and value == True:
                input_message += " [creneau]"
            elif key == "isDate" and value == True:
                input_message += " [date]"
            elif key == "isGenre" and value == True:
                input_message += " [genre]"
            elif key == "isType" and value == True:
                input_message += " [friandise]"
            elif key == "isQuantite" and value == True:
                input_message += " [taille]"

        chat_history += f"{clientId}: {input_message}<split>"
        
        if clientId == 1:
            clientId = 2
            placeholder = "Client B..."
        elif clientId == 2:
            clientId = 1
            placeholder = "Client A..."

        if len(chat_history) > 1:
            return chat_history, alert_message, alert_is_open, placeholder
    else:
        raise PreventUpdate

@app.callback(
    Output("store-message", "data"),
    Output("select", "value"),
    [Input("submit", "n_clicks"), Input("client", "value"),Input("select", "value"), Input("keep-answers", "data"),Input("user-input", "n_submit") ],
    [State("user-input", "value") ],
)
def send_message(n_clicks, client,selected_option ,survey_answers,enter,user_input):
    if ctx.args_grouping[0]["triggered"]==True and client or ctx.args_grouping[4]["triggered"]==True and client:
        message = {}
        if user_input:
            message["message"] = user_input
        else:
            message["message"] = ""
        if selected_option != None and selected_option !=[]:
            for type in selected_option:
                if type == "nombre":
                    message["isNumber"] = True
                elif type =="date":
                    message["isDate"] = True
                elif type == "couleur":
                    message["isCouleur"]=True
                elif type == "siege":
                    message["isSiege"]=True
                elif type == "creneau":
                    message["isCreneau"]=True
                elif type == "genre":
                    message["isGenre"]=True
                elif type == "type_friandise":
                    message["isType"]=True
                elif type == "taille_friandise":
                    message["isQuantite"]=True
                elif type =="message" and not user_input:
                    message={}

        message = json.dumps(message)
        print(f"Message sent : {message}")
        return message, "message"
    else:
        raise PreventUpdate

if __name__ == "__main__":
    app.run_server(debug=True)