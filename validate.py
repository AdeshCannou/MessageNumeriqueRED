from enum import Enum
import datetime
import json

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
        try:
            int(user_input)
            return True
        except ValueError:
            return False
    elif message_json.get("isDate"):
        try:
            datetime.datetime.strptime(user_input, "%d/%m/%Y")
            return True
        except ValueError:
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
        parts = [part.strip() for part in user_input.split(",")]
        if len(parts) != 3:
            return False
        siege, creneau, genre = parts
        try:
            int(siege)
            datetime.datetime.strptime(creneau, "%d/%m/%Y")
            if genre not in [g.value for g in Genre]:
                return False
            return True
        except ValueError:
            return False
    elif message_json.get("isFriandise"):
        parts = [part.strip() for part in user_input.split(",")]
        if len(parts) != 2:
            return False
        type_friandise, quantite = parts
        try:
            if type_friandise not in [t.value for t in TypeFriandise]:
                return False
            int(quantite)
            return True
        except ValueError:
            return False
    else:
        return False

# Exemples d'utilisation de la fonction

# message_json = {'sondage': {'0': 'qds', '1': 'qszzd', '2': 'qsddd'}}
# user_input = "qszzd"
# is_valid = validate_message(message_json, user_input)
# print(f"Le message est valide : {is_valid}")

# message_json = {"isFilm": True}
# user_input = "5,  25/12/2022,   Action"
# is_valid = validate_message(message_json, user_input)
# print(f"Le message de type 'film' est valide : {is_valid}")

# message_json = {"isFriandise": True}
# user_input = "Chocolat,  5"
# is_valid = validate_message(message_json, user_input)
# print(f"Le message de type 'friandise' est valide : {is_valid}")

