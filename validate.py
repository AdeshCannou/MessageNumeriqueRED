from enum import Enum
import json
import re
import calendar

class Genre(Enum):
    ACTION = "Action"
    DRAMA = "Drama"
    COMEDY = "Comedie"
    ROMANCE = "Romance"
    HORROR = "Horreur"

class TypeFriandise(Enum):
    CHOCOLAT = "Chocolat"
    BONBON = "Bonbon"
    GATEAU = "Gateau"
    GLACE = "Glace"
    
class TypeCouleur(Enum):
    ROUGE = "Rouge"
    BLEU = "Bleu"
    VERT = "Vert"
    JAUNE = "Jaune"
    ORANGE = "Orange"
    VIOLET = "Violet"
    BLANC = "Blanc"
    NOIR = "Noir"

class TypeTailleFriandise(Enum):
    M = "M"
    L = "L"
    XL = "XL"

def validate_message(message_json, user_input):
    for key, value in message_json.items():
        print("Key: " + key)
        if key == "message":
            try:
                if user_input:
                    continue
                else:
                    return False
            except ValueError:
                return False
        elif key == "isNumber":
            parts = user_input.split()
            if not any(part.isdigit() for part in parts):
                return False
        elif key == "isDate":
            date_pattern = r'\b(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/((19|20)\d{2})\b' 
            parts = user_input.split()
            date_found = False
            for part in parts:
                if re.match(date_pattern, part):
                    day, month, year = map(int, part.split('/'))
                    if day > calendar.monthrange(year, month)[1]:
                        return False 
                    date_found = True
                    break
            if not date_found:
                return False
        elif key == "isCouleur":
            parts = user_input.split()
            if not any(part.lower() in [couleur.value.lower() for couleur in TypeCouleur] for part in parts):
                return False
        elif key == "isSiege":
            pattern = r"^[A-Z]\d+$"
            parts = user_input.split()
            found_siege = False
            for part in parts:
                if re.match(pattern, part):
                    found_siege = True
                    break
            if not found_siege:
                return False
        elif key == "isGenre":
            parts = user_input.split()
            if not any(part.lower() in [genre.value.lower() for genre in Genre] for part in parts):
                return False
        elif key == "isCreneau":
            time_pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
            if not any(re.match(time_pattern, part) for part in user_input.split()):
                return False
        elif key == "isType":
            parts = user_input.split()
            if not any(part.lower() in [type.value.lower() for type in TypeFriandise] for part in parts):
                return False
        elif key == "isQuantite":
            parts = user_input.split()
            taille_friandise_values = [str(taille.value) for taille in TypeTailleFriandise]
            if not any(part in taille_friandise_values for part in parts):
                return False

    return True


# Exemples d'utilisation de la fonction

# Test pour isNumber
# message_json = {"isNumber": True}
# user_input = "5s sdf 5s sdf 5 dfdfs "
# print(validate_message(message_json, user_input))  # True

# Test pour isDate
# message_json = {"isDate": True}
# user_input = " 29/02/2026"
# print(validate_message(message_json, user_input))  # True

# Test pour isCreneau
# message_json = {"isCreneau": True}
# user_input = " qsdf 24:50 qsd"
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
# user_input = "5 sdf sdf M sdsmf"
# print(validate_message(message_json, user_input))  # True


# Test avec plusieurs propriétés
# message_json = {"isCreneau": True, "isGenre": True, "isSiege": True}
# user_input = "genre : drama  creneau : 2:50 siege : A56"
# print(validate_message(message_json, user_input))  # True

# Test avec plusieurs propriétés Date et Number
# message_json = {"isDate": True, "isNumber": True, "isSiege": True}
# user_input = "date : 05/12/1990  creneau : 2 siege : A5"
# print(validate_message(message_json, user_input))  # True

