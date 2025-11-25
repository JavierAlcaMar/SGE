from odoo import models, fields

class Paquete(models.Model):
    _name = "paqueteria.paquete"
    _description = "Paquete transportado por la empresa"

    tracking = fields.Char(
        string="Número de seguimiento",
        required=True
    )

    remitente_id = fields.Many2one(
        "res.partner",
        string="Remitente",
        required=True
    )

    destinatario_id = fields.Many2one(
        "res.partner",
        string="Destinatario",
        required=True
    )

    # Dirección de entrega
    pais = fields.Char(string="País")
    region = fields.Char(string="Región")
    municipio = fields.Char(string="Municipio")
    calle = fields.Char(string="Calle")
    numero = fields.Char(string="Número")
    datos_adicionales = fields.Text(string="Datos adicionales")

    # Camión que transporta el paquete
    camion_id = fields.Many2one(
        "paqueteria.camion",
        string="Camión transportista"
    )

    # Actualizaciones de seguimiento
    actualizaciones_ids = fields.One2many(
        "paqueteria.seguimiento",
        "paquete_id",
        string="Actualizaciones del envío"
    )

