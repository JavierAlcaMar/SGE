from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    x_dni = fields.Char(string="DNI", size=9)
    x_nss = fields.Char(string="Nº Seguridad Social", size=12)

    @api.constrains("x_dni", "x_nss")
    def _check_dni_nss(self):
        for emp in self:
            # --- NSS ---
            if emp.x_nss:
                nss = emp.x_nss.strip().replace(" ", "")
                if len(nss) != 12 or not nss.isdigit():
                    raise ValidationError(
                        _("El NSS debe tener 12 dígitos (2 provincia + 8 identificativos + 2 control).")
                    )

            # --- DNI ---
            if emp.x_dni:
                dni = emp.x_dni.strip().upper().replace(" ", "")
                # Formato: 8 dígitos + 1 letra
                if not re.fullmatch(r"\d{8}[A-Z]", dni):
                    raise ValidationError(_("El DNI debe tener 8 dígitos y una letra (ej: 12345678Z)."))

                number = int(dni[:8])
                letter = dni[8]
                letters_map = "TRWAGMYFPDXBNJZSQVHLCKE"
                expected = letters_map[number % 23]
                if letter != expected:
                    raise ValidationError(
                        _("La letra del DNI no es correcta. Para %s debería ser %s.") % (dni[:8], expected)
                    )

