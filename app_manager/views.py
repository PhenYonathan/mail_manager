from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import Http404

from django.views.generic import TemplateView, ListView

import environ

from mail_manager.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(env_file=str(BASE_DIR / "mail_manager" / ".env"))


class HomeAppView(TemplateView):
    template_name = "app_manager/index.html"

    import imaplib
    import email

    server = "imap.gmail.com"
    imap = imaplib.IMAP4_SSL(server)

    username = env("USERMAIL")
    password = env("MDPMAIL")

    imap.login(username, password)

    res, messages = imap.select('"INBOX"')

    messages = int(messages[0])

    n = 10
    attendu = 8
    ras = 0
    erreur = 0
    lstSubjectRAS = []
    lstSubjectError = []

    for i in range(messages, messages - n, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                From = msg["From"]
                subject = msg["Subject"]
                pos = subject.find('serveur')

                if "[RAS]" in subject:
                    ras = ras + 1
                    lstSubjectRAS.append(subject[pos:])
                if "[ERREUR]" in subject:
                    erreur = erreur + 1
                    lstSubjectError.append(subject[pos:])

    nbInconnu = n - (ras + erreur)
    nbSI = attendu - (ras + erreur)

    def get_context_data(self, **kwargs):
        context = super(HomeAppView, self).get_context_data(**kwargs)
        context.update(
            {
                'ras': self.ras,
                'erreur': self.erreur,
                'nbInconnu': self.nbInconnu,
                'nbSI': self.nbSI,
                'lstSubjectError': self.lstSubjectError,
                'lstSubjectRAS': self.lstSubjectRAS,
            }
        )
        return context


class AppMoreInfos(TemplateView):
    template_name = "app_manager/more_infos.html"

