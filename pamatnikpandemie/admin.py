from flask_security import current_user

from flask import url_for, redirect, request, abort
from flask_admin.contrib import sqla


class AdminModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role("superuser")

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for("security.login", next=request.url))


class StoryModelView(AdminModelView):
    form_widget_args = {"story": {"rows": 5}}

    form_choices = {
        "statue": [
            ("postava_babi", "Babička 1"),
            ("postava_babi2", "Babička 2"),
            ("postava_chlapec", "Chlapec"),
            ("postava_deda", "Děda 1"),
            ("postava_deda2", "Děda 2"),
            ("postava_doktor", "Doktor"),
            ("postava_hudebnik", "Hudebník"),
            ("postava_kracejici_muz", "Kráčející muž"),
            ("postava_muz_se_psem", "Muž se psem"),
            ("postava_muz1", "Muž 1"),
            ("postava_muz2", "Muž 2"),
            ("postava_obezni_muz", "Obézní muž"),
            ("postava_pani_se_psem", "Paní se psem"),
            ("postava_par", "Pár"),
            ("postava_sestra", "Sestra"),
            ("postava_svalovec", "Svalovec"),
            ("postava_telefonujici_muz", "Telefonující muž"),
            ("postava_ucitelka", "Učitelka"),
            ("postava_vozickar", "Vozíčkář"),
            ("postava_zena_s_kockou", "Žena s kočkou"),
            ("postava_zena", "Žena 1"),
            ("postava_zena2", "Žena 2"),
            ("postava_zena3", "Žena 3"),
        ]
    }

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role("user")


class MessageModelView(AdminModelView):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role("user")
