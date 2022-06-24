from django.db import models
import datetime
import email
from email.header import decode_header, make_header
import imaplib
import environ
# from asgiref.sync import sync_to_async

from mail_manager.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / "mail_manager" / ".env"))

# ----------------------------------------------------- #
#                Déclarations divers                    #
# ----------------------------------------------------- #
encoding = 'utf-8'

# Listes des mots de RAS
lst_RAS = [
    "ras",
    "RAS",
    "réussi ",
    "terminée",
    "terminé"
]

# Liste des mot d'erreurs
lst_ERREUR = [
    "ERREUR",
    "error",
    "erreur",
    "échoué"
]

# ----------------------------------------------------- #
#                Récupération des mails                 #
# ----------------------------------------------------- #
username = env("USERMAIL")
password = env("MDPMAIL")

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(username, password)

# Boite
m.select("inbox")
m.list()

# Recherche
date = (datetime.date.today() - datetime.timedelta(30)).strftime("%d-%b-%Y")
msg_from = '"Yonathan Cardoso"'

# ----------------------------------------------------- #


def decode_str(word):
    """
    decode_str decode les chaines de caractère qui viennent des headers des mails.

    :param word: Entrez un string provenant d'un header de mail
    :return: un string décodé
    """
    h = make_header(decode_header(word))
    s = str(h)
    return s


# @sync_to_async
def get_mails():
    """
    get_mails est une fonction qui permet de récupérer les mails choisis pour les sortir dans un dico.

    :return: une liste contenant deux listes, une premiere de mails ras et une seconde d'erreurs. Chacune d'elle
    contient des dictionnaires avec toutes les informations nécessaires
    """
    # Déclarations des variables utiles. Ne pas toucher
    final_list = []
    lst_mails_ras = []
    lst_mails_erreurs = []

    # Tri
    result, data = m.search(None, '(FROM {msg_from} SENTSINCE {date})'.format(date=date, msg_from=msg_from))
    ids = str(data[0], encoding)

    # Création d'une liste de message par ids
    id_list = ids.split()

    for emailid in id_list:
        temp_dict = {}
        result, data = m.fetch(str(emailid), "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_bytes(email_body)

        temp_dict['Sender'] = mail["From"]
        temp_dict['Date'] = mail["Date"]
        s = mail["Subject"]
        temp_dict['Subject'] = decode_str(s)

        if any(word in temp_dict['Subject'] for word in lst_RAS):
            lst_mails_ras.append(temp_dict)

        if any(word in temp_dict['Subject'] for word in lst_ERREUR):
            lst_mails_erreurs.append(temp_dict)

    final_list.append(lst_mails_ras)
    final_list.append(lst_mails_erreurs)

    return final_list


# @sync_to_async
def count_nb_mails():
    """
    count_nb_mails permet de compter le nombre de RAS et ERREUR.

    :return: une liste contenant 3 paramétres :
        - Le nombre de RAS
        - Le nombre d'erreurs
        - Le nombre de mails non reçus
    """
    # Déclarations des variables utiles. Ne pas toucher
    ras = erreur = 0

    # Tri
    # result, data = m.search(None, '(FROM {msg_from} SENTSINCE {date})'.format(date=date, msg_from=msg_from))
    result, data = m.search(None, '(SENTSINCE {date})'.format(date=date))
    ids = str(data[0], encoding)

    # Création d'une liste de message par ids
    id_list = ids.split()

    for emailid in id_list:
        temp_dict = {}
        result, data = m.fetch(str(emailid), "(RFC822)")
        email_body = data[0][1]
        mail = email.message_from_bytes(email_body)
        s = mail["Subject"]
        temp_dict['Subject'] = decode_str(s)

        if any(word in temp_dict['Subject'] for word in lst_RAS):
            ras = ras + 1

        if any(word in temp_dict['Subject'] for word in lst_ERREUR):
            erreur = erreur + 1

    manque = 10 - (ras + erreur)
    final_nbs = {
        'ras': ras,
        'erreur': erreur,
        'manque': manque
    }

    return final_nbs

