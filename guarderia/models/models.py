# -*- coding: utf-8 -*-
from odoo import fields, models


class GuarderiaServicio(models.Model):
    _name = "guarderia.servicio"
    _description = "Servicio de Guardería"

    # Multiherencia por delegación
    _inherits = {
        "hr.employee": "employee_id",
        "calendar.event": "event_id",
    }

    # Enlaces a los modelos delegados
    employee_id = fields.Many2one(
        "hr.employee",
        string="Monitor (Empleado)",
        required=True,
        ondelete="cascade",
        index=True,
        auto_join=True,
    )

    event_id = fields.Many2one(
        "calendar.event",
        string="Evento (Horario)",
        required=True,
        ondelete="cascade",
        index=True,
        auto_join=True,
    )

    # Campos propios del servicio
    description = fields.Text(string="Descripción")

    age_range = fields.Selection(
        [
            ("0_2", "0-2"),
            ("3_5", "3-5"),
            ("6_8", "6-8"),
            ("9_11", "9-11"),
        ],
        string="Rango de edad",
        required=True,
        default="0_2",
    )

