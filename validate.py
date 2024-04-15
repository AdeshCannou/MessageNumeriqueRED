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
    for key, value in message_json.items():
        if key == "message":
            try:
                if user_input:
                    continue
                else:
                    return False
            except ValueError:
                return False
        elif key == "isNumber" or key == "isQuantite":
            number_pattern = r'\b\d+\b'
            if not re.search(number_pattern, user_input):
                return False
        elif key == "isDate" or key == "isCreneau":
            date_pattern = r'\b\d{1,2}/\d{1,2}/\d{4}\b'
            if not re.search(date_pattern, user_input):
                return False
        elif key == "sondage":
            try:
                sondage_data = message_json["sondage"]
                if user_input not in sondage_data.values():
                    return False
            except json.JSONDecodeError:
                return False
        elif key == "isSiege":
            pattern = r"^[A-Z]\d+$"
            parts = user_input.split()
            found_siege = False
            for part in parts:
                if re.match(pattern, part):
                    # Si la partie respecte le format du siège, on met found_siege à True et on continue la boucle
                    found_siege = True
                    break  # Sortir de la boucle une fois qu'un siège est trouvé
            if not found_siege:
                return False
        elif key == "isGenre":
            parts = user_input.split()
            if not any(part.lower() in [genre.value.lower() for genre in Genre] for part in parts):
                return False
        elif key == "isType":
            parts = user_input.split()
            if not any(part.lower() in [type.value.lower() for type in TypeFriandise] for part in parts):
                return False
        else:
            return False
    return True


# Exemples d'utilisation de la fonction

# Test pour isNumber
# message_json = {"isNumber": True}
# user_input = "ti 5d sdf 777 sdf  "
# print(validate_message(message_json, user_input))  # True

# Test pour isDate
# message_json = {"isDate": True}
# user_input = "papap 15/03/2024"
# print(validate_message(message_json, user_input))  # True

# Test pour sondage
# message_json = {"sondage": {"1": "Option 1", "2": "Option 2"}}
# user_input = "Option 1"
# print(validate_message(message_json, user_input))  # True

# Test pour isCreneau
# message_json = {"isCreneau": True}
# user_input = " qsdf 15/03/2024"
# print(validate_message(message_json, user_input))  # True

# Test pour isSiege
# message_json = {"isSiege": True}
# user_input = "sdf A1sd sdd B22"
# print(validate_message(message_json, user_input))  # True

# Test pour isGenre
# message_json = {"isGenre": True}
# user_input = " sdfsf sdf sq Drama sd sds5 55qsd5"
# print(validate_message(message_json, user_input))  # True

# Test pour isType
# message_json = {"isType": True}
# user_input = "dsf  ds f  chocolat sdfd  sdf"
# print(validate_message(message_json, user_input))  # True

# Test pour isQuantite
# message_json = {"isQuantite": True}
# user_input = "5"
# print(validate_message(message_json, user_input))  # True


# Test avec plusieurs propriétés
# message_json = {"isCreneau": True, "isGenre": True, "isSiege": True}
# user_input = "genre : drama  creneau : 12/03/2022  siege : A56"
# print(validate_message(message_json, user_input))  # True

