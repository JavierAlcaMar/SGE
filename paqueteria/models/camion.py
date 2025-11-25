from odoo import models, fields

class Camion(models.Model):
    _name = "paqueteria.camion"
    _description = "Camión que transporta los paquetes"

    matricula = fields.Char(
        string="Matrícula",
        required=True
    )

    conductor_actual_id = fields.Many2one(
        "hr.employee",
        string="Conductor actual"
    )

    antiguos_conductores_ids = fields.Many2many(
        "hr.employee",
        string="Antiguos conductores"
    )

    fecha_itv = fields.Date(string="Fecha de la última ITV")
    notas_mantenimiento = fields.Text(string="Notas de mantenimiento")

    paquetes_ids = fields.One2many(
        "paqueteria.paquete",
        "camion_id",
        string="Paquetes transportados"
    )

