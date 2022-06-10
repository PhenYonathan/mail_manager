import datetime
import email
from email.header import Header, decode_header, make_header
import imaplib
import environ
from django.views.generic import TemplateView

from mail_manager.settings import BASE_DIR
env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / "mail_manager" / ".env"))

##########################
# Récupération des mails #
##########################
username = env("USERMAIL")
password = env("MDPMAIL")

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(username, password)

# Boite
m.select("inbox")
m.list()


##########################


class HomeAppView(TemplateView):
    template_name = "app_manager/index.html"

    # Déclarations des variables utiles. Ne pas toucher
    encoding = 'utf-8'
    final_list = []
    ras = erreur = 0
    lstSubjectRAS = []
    lstSubjectError = []

    # Listes des mots de RAS
    lst_RAS = [
        "ras",
        "réussi ",
        "terminée",
        "terminé"
    ]

    # Liste des mot d'erreurs
    lst_ERREUR = [
        "error",
        "erreur",
        "échoué"
    ]

    # Déclarations
    attendu = 10
    date = (datetime.date.today() - datetime.timedelta(30)).strftime("%d-%b-%Y")
    msg_from = '"Yonathan Cardoso"'

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
        s = temp_dict['Subject'] = mail["Subject"]
        temp_dict['Date'] = mail["Date"]
        pos = temp_dict['Subject'].find('serveur')

        if "[RAS]" in temp_dict['Subject']:
            ras = ras + 1
            lstSubjectRAS.append(temp_dict['Subject'][pos:])

        if "[ERREUR]" in temp_dict['Subject']:
            erreur = erreur + 1
            lstSubjectError.append(temp_dict['Subject'][pos:])

        # print(temp_dict)
        final_list.append(temp_dict)

    manque = attendu - (ras + erreur)
    print(ras)

    def get_context_data(self, **kwargs):
        context = super(HomeAppView, self).get_context_data(**kwargs)
        context.update(
            {
                'ras': self.ras,
                'erreur': self.erreur,
                'manque': self.manque,
                'lstSubjectError': self.lstSubjectError,
                'lstSubjectRAS': self.lstSubjectRAS,
            }
        )
        return context


class AppMoreInfos(TemplateView):
    template_name = "app_manager/more_infos.html"
