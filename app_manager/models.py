from django.db import models
import datetime
import email
from email.header import decode_header, make_header
import imaplib
import environ

from mail_manager.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / "mail_manager" / ".env"))

# ----------------------------------------------------- #
#                Déclarations divers                    #
# ----------------------------------------------------- #
encoding = 'utf-8'

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
#                       Listes                          #
# ----------------------------------------------------- #
class LstStatus(models.Model):
    status = models.CharField(max_length=100)
    word = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Liste status"

    def __str__(self):
        return self.word


# ----------------------------------------------------- #
#                      Méthodes                         #
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


def create_list(status):
    """
    create_list permet de créer une liste de mot à partir de QuerySet reçu de la base de données pour la table
    LstStatus.

    :param status: Entrez une chaine de caractère correspondant au status de la table LstStatus
    :return: une liste de string
    """
    liste = list(LstStatus.objects.filter(status=status).values_list('word', flat=True))
    return liste


def get_mails(status):
    """
    get_mails est une fonction qui permet de récupérer les mails choisis pour les sortir dans un dico.

    :param status: Entrez un string "ras", "error" ou une autre chaine.
    :return: une liste de mails reçue dans le mois, la liste change selon le paramètre entrer
    """
    # Déclarations des variables utiles. Ne pas toucher
    final_list = []
    lst_mails = []
    lst_mails_ras = []
    lst_mails_error = []
    lst_ras = create_list("ras")
    lst_erreur = create_list("error")

    # Tri
    # result, data = m.search(None, '(FROM {msg_from} SENTSINCE {date})'.format(date=date, msg_from=msg_from))
    result, data = m.search(None, 'SENTSINCE {date}'.format(date=date))
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

        if status == "ras":
            if any(word in temp_dict['Subject'] for word in lst_ras):
                lst_mails.append(temp_dict)
        elif status == "error":
            if any(word in temp_dict['Subject'] for word in lst_erreur):
                lst_mails.append(temp_dict)
        else:
            if any(word in temp_dict['Subject'] for word in lst_ras):
                lst_mails_ras.append(temp_dict)

            if any(word in temp_dict['Subject'] for word in lst_erreur):
                lst_mails_error.append(temp_dict)

    if status == "ras" or status == "error":
        final_list = lst_mails
    else:
        final_list.append(lst_mails_ras)
        final_list.append(lst_mails_error)

    return final_list


def count_nb_mails():
    """
    count_nb_mails permet de compter le nombre de RAS et ERREUR.

    :return: une liste contenant 3 paramètres :
        - Le nombre de RAS
        - Le nombre d'erreurs
        - Le nombre de mails non reçus
    """
    # Déclarations des variables utiles. Ne pas toucher
    ras = erreur = 0
    lst_ras = create_list("ras")
    lst_erreur = create_list("error")

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

        if any(word in temp_dict['Subject'] for word in lst_ras):
            ras = ras + 1

        if any(word in temp_dict['Subject'] for word in lst_erreur):
            erreur = erreur + 1

    manque = len(id_list) - (ras + erreur)
    final_nbs = {
        'ras': ras,
        'erreur': erreur,
        'manque': manque
    }

    return final_nbs

