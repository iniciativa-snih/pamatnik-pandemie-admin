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
    form_widget_args = {"story": {"rows": 2}}

    form_choices = {
        "statue": [
            ("man_calling", "Volající muž"),
            ("man_walking", "Jdoucí muž"),
            ("man_with_dog", "Muž se psem"),
            ("grandma_standing", "Stojící babička"),
            ("woman_standing", "Stojící žena"),
            ("kid", "Dítě"),
            ("woman_reading", "Čtoucí žena"),
            ("granddad_walking", "Jdoucí dědeček"),
            ("fat_man", "Obézní muž"),
            ("grandma_with_dog", "Babi se psem"),
            ("man_with_cap", "Muž v čepici"),
            ("walking_pair", "Jdoucí pár"),
            ("man_lifting", "Muž s činkami"),
            ("man_on_wheelchair", "Muž na vozíku"),
            ("woman_with_dog", "Žena se psem"),
            ("woman_teacher", "Učitelka"),
            ("man_teacher", "Učitel"),
        ]
    }

    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role("user")


class MessageModelView(AdminModelView):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role("user")
