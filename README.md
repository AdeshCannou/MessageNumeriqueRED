# Projet Représentation et échange de données : Communication numerique par messages structurés

Ce projet vise à améliorer la communication numérique en proposant une approche structurée des messages. Il utilise Dash, un framework Python pour créer un client de messagerie interactif, permettant la gestion de messages structurés.

## Cloner le projet

Pour cloner ce projet, exécutez la commande suivante dans votre terminal :
```
git clone https://github.com/AdeshCannou/MessageNumeriqueRED.git
```

## Installation des dépendances

Pour exécuter ce projet, vous devez disposer de Python 3.x installé sur votre système. Vous pouvez ensuite installer les dépendances en exécutant la commande suivante :

```bash
python -m venv venv
source venv/bin/activate  # Windows: \venv\scripts\activate
pip install -r requirements.txt
```

## Lancer le serveur Dash

Lancement du serveur Dash
Pour lancer le serveur Dash, exécutez la commande suivante dans votre terminal :

```bash
python main.py
```

Cela démarrera le serveur sur le port 8050 de votre machine locale. Vous pouvez accéder à l'application en visitant l'URL http://localhost:8050/ dans votre navigateur.

## Structure du projet

- `main.py`: Code principal de l'application utilisant le framework Dash.
- `layout.py`: Elements de mise en page de l'application.
- `validate.py`: Fonctions de validation des messages.
- `README.md`: Ce fichier README contenant des informations sur le projet.
- `requirements.txt`: Fichier contenant les dépendances Python requises pour exécuter le projet.

## Utilisation de l'application

- Choisir les plugins requis en utilisant le panneau "Choix des plugins".
- Le client A commence la conversation en saisissant un message dans la zone de texte prévue.
- Sélectionner le type de message désiré à l'aide de la liste déroulante en dessous de la zone de texte. Plusieurs options peuvent être choisies simultanément.
- Cliquer sur le bouton "Submit" pour envoyer le message.
- Automatiquement, la conversation passe au client B qui doit répondre.
- Si le message de réponse est valide, il est envoyé. Sinon, un message d'erreur est renvoyé.
- Le client B peut également choisir le type de message attendu par le client A.

## Spécifications des messages

Les messages structurés sont définis par un type et un contenu. Les types de messages disponibles sont les suivants :

Noyau :
- `Message`: Message texte simple.
- `Date`: Date au format "jj/mm/aaaa" (ex: 01/01/2022)
- `Couleur`: Nom de couleur (Rouge, Bleu, Vert, Jaune, Orange, Violet, Blanc, Noir)
- `Nombre`: Nombre entier

Film :
- `Siège`: Format de siège valide, Lettre Majuscule suivi d'un nombre (ex: A1, B2, etc.)
- `Créneau`: Date au format "HH:MM" (ex: 12:50) 
- `Genre`: Genre de film (Action, Drame, Comedie, Romance, Horreur)

Friandise :
- `Type Friandise`: Type de friandise (Chocolat, Bonbon, Gâteau, Glace)
- `Taille Friandise`: Quantité de Friandise (M, L ou XL)