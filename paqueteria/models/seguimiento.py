from odoo import models, fields

class Seguimiento(models.Model):
    _name = "paqueteria.seguimiento"
    _description = "Actualización del estado del envío"

    paquete_id = fields.Many2one(
        "paqueteria.paquete",
        string="Paquete",
        required=True,
        ondelete="cascade",
    )

    fecha = fields.Datetime(
        string="Fecha de entrada",
        default=fields.Datetime.now,
        required=True,
    )

    estado = fields.Selection(
        [
            ("recibido", "Recibido en almacén"),
            ("en_camino", "En camino"),
            ("en_reparto", "En reparto"),
            ("entregado", "Entregado"),
            ("incidencia", "Incidencia detectada"),
        ],
        string="Estado",
        required=True,
    )

    notas = fields.Text(string="Notas adicionales")

