
import os
import time
import json
import dash
import json
from dash import Dash, html, Input, Output, ctx, callback, State, dcc, MATCH, ALL, Patch
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from layout import app, textbox

#Ne pas oublier de creer une fonction qui peuple le select menu

# Pour updater les bulles de conversation
@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    """Modifie the conversation display with the chat history.
    :param chat_history:
    :return:
        list: la liste des bulles de conversation
    """

    return [textbox(x.split(": ")[1], int(x.split(": ")[0][-1])) for x in chat_history.split("<split>")[:-1]]

# Pour effacer le champ de texte
@app.callback(
    Output("user-input", "value"),
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
)
def clear_input(n_clicks, n_submit):
    """
    Clear the input field after the user has submitted a message.
    :param n_clicks: quand on clique sur le bouton submit
    :param n_submit: quand on appuie sur la touche entrer
    :return:
    """
    return ""

@app.callback(
    Output("store-conversation", "data"),
    [Input("store-message", "data"),Input("submit", "n_clicks"), Input("client", "value"),Input("user-input", "n_submit")],
    State("store-conversation", "data")
)
def update_conversation(store_message,n_clicks, client, enter,chat_history):
    """
    Update the conversation history with the new message.
    :param store_message: le message à ajouter
    :param n_clicks: quand on clique sur le bouton submit
    :param client: le client qui a envoyé le message
    :param enter: quand on appuie sur la touche entrer
    :param chat_history:  l'historique de la conversation
    :return:
    l'historique de la conversation
    """

    if ctx.args_grouping[1]["triggered"]==True and client or  ctx.args_grouping[3]["triggered"]==True and client:
        store_message=json.loads(store_message)
        input_message = store_message["message"]
        if len(store_message)==1:
            chat_history += f"{client}: {input_message}<split>"
        else:
            for key, value in store_message.items():
                if key == "message":
                    chat_history += f"{client}: {input_message}<split>"
                if key =="sondage":
                    sondage_message = f"{client}: Sondage"
                    sondage_answers = store_message["sondage"]
                    for answer in sondage_answers.values():
                        sondage_message += f"{answer} \n"
                    sondage_message = sondage_message[:-2]
                    chat_history += f"{sondage_message}<split>"

                elif key =="isNumber" :
                    chat_history += f"{client}: Choisis un nombre<split>"
                elif key =="isSiege":
                    chat_history += f"{client}: Quel Siège<split>"
                elif key =="isCreneau" and value==True:
                    chat_history += f"{client}: Quel Créneau<split>"
                elif key =="isDate" and value==True:
                    chat_history += f"{client}: Quel Date<split>"
                elif key =="isGenre" and value==True:
                    chat_history += f"{client}: Quel Genre<split>"
                elif key =="isType" and value==True:
                    chat_history += f"{client}: Quel friandise<split>"
                elif key =="isQuantite" and value==True:
                    chat_history += f"{client}: Quel quantité Friandise<split>"

    return chat_history

@app.callback(
    Output("store-message", "data"),
    [Input("submit", "n_clicks"), Input("client", "value"),Input("select", "value"), Input("keep-answers", "data"),Input("user-input", "n_submit") ],
    [State("user-input", "value")],
)
def keep_message(n_clicks, client,selected_option ,survey_answers,enter,user_input):
    """
    Keep the message in a json format : A UTILISER PLUS TARD POUR CLIENT B > A , c'est ici qu'on fait les messages en json format
    :param n_clicks: quand on clique sur le bouton submit
    :param client: le client qui a envoyé le message
    :param selected_option: l'option selectionnée
    :param survey_answers: les réponses du sondage
    :param enter: quand on appuie sur la touche entrer
    :param user_input: le message de l'utilisateur (input)
    :return:
    le message en json
    """

    if user_input and ctx.args_grouping[0]["triggered"]==True and client or ctx.args_grouping[4]["triggered"]==True and client:
        message = {}
        message["message"] = user_input
        if selected_option != None or selected_option !="0":
            if selected_option == "1":
                message["isDate"]=True
            elif selected_option == "2" and survey_answers:
                survey_answers=json.loads(survey_answers)
                message["sondage"]=survey_answers
            elif selected_option == "3":
                message["isNumber"]=True
            elif selected_option == "4":
                message["isSiege"]=True
            elif selected_option == "5":
                message["isCreneau"]=True
            elif selected_option == "6":
                message["isGenre"]=True
            elif selected_option == "7":
                message["isType"]=True
            elif selected_option == "8":
                message["isQuantite"]=True
            return json.dumps(message)
            #chat_history += f"{client}: {user_input}<split>"
    else:
        raise PreventUpdate


#survey
@app.callback(
    Output("survey-container", "hidden"),
    Input("select", "value"),
    [Input("client", "value")],
)
def display_survey_form(selected_option,client):
    """
    Display the survey form (car il était caché)
    :param selected_option: l'option "Sondage" selectionnée
    :param client: le client qui a envoyé le message
    :return: True et affiche si l'option "Sondage" est selectionnée, False sinon et cache
    """
    if client and selected_option != None:
        if selected_option == "2":
            return False
    return True


# Callback to add new item to list
@callback(
    Output("list-container-div", "children", allow_duplicate=True),
    Output("new-item-input", "value"),
    Input("add-btn", "n_clicks"),
    State("new-item-input", "value"),
    prevent_initial_call=True,
)
def add_item(button_clicked, value):
    """
    Add a new item to the survey
    :param button_clicked: quand on clique sur le bouton "Ajouter la réponse"
    :param value: la valeur de la réponse
    :return: la liste des réponses du sondage
    """
    patched_list = Patch()
    def new_checklist_item():
        return html.Div(
            [

                html.Div(
                    [value],
                    id={"index": button_clicked, "type": "output-str"},
                    style={"display": "inline", "margin": "10px"},
                ),
            ]
        )

    patched_list.append(new_checklist_item())
    return patched_list, ""



# Callback to keep survey
@callback(
    Output("keep-answers", "data"), Input("list-container-div", "children")
)
def keep_survey(answers):
    """
    Keep the survey answers in a json format
    :param answers: les réponses du sondage
    :return: les réponses du sondage en json
    """

    if answers is None:
        raise PreventUpdate
    result={}

    for (i, answer) in enumerate(answers):
        result[i]=answer['props']['children'][0]['props']['children'][0]

    result = json.dumps(result, indent = 2)
    return result

# Callback to delete survey
@callback(
    Output("list-container-div", "children", allow_duplicate=True),
    Input("clear-done-btn", "n_clicks"),
    prevent_initial_call=True,
)
def delete_items(n_clicks ):
    """
    Delete the survey items
    :param n_clicks: quand on clique sur le bouton
    :return: un container vide
    """
    return []


if __name__ == "__main__":
    app.run_server(debug=True)