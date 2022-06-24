from django.views.generic import TemplateView
from app_manager import models
from django.template.defaulttags import register


class HomeAppView(TemplateView):
    template_name = "app_manager/index.html"

    listMails = models.get_mails()
    affine_ras = [sub['Subject'] for sub in listMails[0]]
    affine_erreur = [sub['Subject'] for sub in listMails[1]]

    def get_context_data(self, **kwargs):
        context = super(HomeAppView, self).get_context_data(**kwargs)
        context.update(
            {
                'ras': models.count_nb_mails().get('ras', 'En attente'),
                'erreur': models.count_nb_mails().get('erreur', 'En attente'),
                'manque': models.count_nb_mails().get('manque', 'En attente'),
                'lstSubjectError': self.affine_erreur,
                'lstSubjectRAS': self.affine_ras,
            }
        )
        return context


class AppMoreInfos(TemplateView):
    template_name = "app_manager/more_infos.html"

    listMails = models.get_mails()
    request = "ras"

    if request == "ras":
        lst_mails = listMails[0]
    elif request == "error":
        lst_mails = listMails[1]

    compt = len(lst_mails)

    def get_context_data(self, **kwargs):
        context = super(AppMoreInfos, self).get_context_data(**kwargs)
        context.update(
            {
                'compt': self.compt,
                'lst_mails': self.lst_mails,
                'all': models.get_mails()
            }
        )
        return context

