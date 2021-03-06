from django.views.generic import TemplateView
from app_manager import models


class HomeAppView(TemplateView):
    template_name = "app_manager/index.html"

    listMails = models.get_mails("all")

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        list_mails = models.get_mails(self.kwargs.get("status"))

        print(list_mails)

        context.update(
            {
                'compt': len(list_mails),
                'lst_mails': list_mails,
            }
        )
        return context

