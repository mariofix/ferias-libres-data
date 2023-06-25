from flask import redirect, request, url_for
from flask_admin import Admin
from flask_admin.consts import ICON_TYPE_FONT_AWESOME
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_babel import lazy_gettext as _

from ..database import db
from ..models import Comuna, Feria, Role, User
from .views import ComunaAdmin, FeriaAdmin, RoleAdmin, UserAdmin

admin_site = Admin(
    name="Ferias Libres",
    template_mode="bootstrap4",
    url="/admin.site",
)


admin_site.add_view(
    UserAdmin(
        User,
        db.session,
        category=_("System"),
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-solid fa-user",
    )
)
admin_site.add_view(
    RoleAdmin(
        Role,
        db.session,
        category=_("System"),
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-solid fa-list",
    )
)


admin_site.add_view(
    ComunaAdmin(
        Comuna,
        db.session,
        category=_("Ferias Libres"),
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-solid fa-list",
    )
)


admin_site.add_view(
    FeriaAdmin(
        Feria,
        db.session,
        category=_("Ferias Libres"),
        menu_icon_type=ICON_TYPE_FONT_AWESOME,
        menu_icon_value="fa-solid fa-list",
    )
)
