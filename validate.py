from enum import Enum
import datetime
import json
import re

class Genre(Enum):
    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedy"
    ROMANCE = "Romance"
    HORROR = "Horror"

class TypeFriandise(Enum):
    CHOCOLAT = "Chocolat"
    BONBON = "Bonbon"
    GATEAU = "Gateau"
    GLACE = "Glace"

def validate_message(message_json, user_input):
    """
    Validate a message based on the specified type in the JSON and user input.
    
    Args:
    - message_json (dict): Le JSON contenant les types de message à valider (par exemple : {"isFilm": true, "isFriandise": true}).
    - user_input (str): L'entrée utilisateur à valider.
    - survey_answers (str): Les réponses du sondage (utilisé uniquement si le type de message est "sondage").

    Returns:
    - bool: True si le message est valide selon le type spécifié dans le JSON, False sinon.
    """
    
    if message_json.get("message"):
        try:
            if user_input:
                return True
            else:
                return False
        except ValueError:
            return False
    elif message_json.get("isNumber"):
        number_pattern = r'\b\d+\b'
        if re.search(number_pattern, user_input):
            return True
        else:
            return False
    elif message_json.get("isDate"):
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
        if re.search(date_pattern, user_input):
            return True
        else:
            return False
    elif "sondage" in message_json:
        try:
            sondage_data = message_json["sondage"]
            if user_input in sondage_data.values():
                return True
            else:
                return False
        except json.JSONDecodeError:
            return False
    elif message_json.get("isFilm"):
        parts = user_input.split()
        pattern = r"^[A-Z]\d+$"
        for part in parts:
            if re.match(pattern, part):
                # Si la partie respecte le format du siège, c'est le siège
                siege = part
            elif '/' in part:
                # Si le mot contient '/', c'est potentiellement une date
                try:
                    datetime.datetime.strptime(part, "%d/%m/%Y")
                    creneau = part
                except ValueError:
                    return False
            elif part in [g.value for g in Genre]:
                # Si le mot est un genre valide, c'est le genre
                genre = part
        try:
            siege
            creneau
            genre
            # print(f"Siege : {siege}, Creneau : {creneau}, Genre : {genre}")
            return True
        except NameError:
            return False
    elif message_json.get("isFriandise"):
        parts = user_input.split()
        for part in parts:
            if part.isdigit():
                # Si le mot est un nombre, c'est la quantité
                quantite = int(part)
            elif part in [t.value for t in TypeFriandise]:
                # Si le mot est un type de friandise valide, c'est le type de friandise
                type_friandise = part
        try:
            quantite
            type_friandise
            return True
        except NameError:
            return False
    else:
        return False

# Exemples d'utilisation de la fonction

# message_json = {'sondage': {'0': 'qds', '1': 'qszzd', '2': 'qsddd'}}
# user_input = "qszzd"
# is_valid = validate_message(message_json, user_input)
# print(f"Le message est valide : {is_valid}")

# message_json = {"isFilm": True}
# user_input = "Je veux le 29/03/2024 pour le type Action siege F9"
# is_valid = validate_message(message_json, user_input)
# print(f"Le message de type 'film' est valide : {is_valid}")

# message_json = {"isFriandise": True}
# user_input = "slkdj sdlkjsdljf 5 ksdj kjsqd kqsjhd kqjshd Chocolat"
# is_valid = validate_message(message_json, user_input)
# print(f"Le message de type 'friandise' est valide : {is_valid}")

