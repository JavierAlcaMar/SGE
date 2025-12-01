from odoo import models, fields, api
from odoo.exceptions import ValidationError


# --------------------------------------------------------------------------
#                         MODELO PRINCIPAL: NÓMINA
# --------------------------------------------------------------------------
class Nomina(models.Model):
    _name = "sge.nomina"
    _description = "Nómina de empleado"

    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True)
    fecha = fields.Date(string="Fecha", default=fields.Date.context_today, required=True)

    sueldo_base = fields.Float(string="Sueldo base (€)", digits=(16, 2), required=True)
    irpf = fields.Float(string="IRPF (%)", digits=(3, 2), required=True)

    irpf_pagado = fields.Float(
        string="IRPF pagado (€)",
        digits=(16, 2),
        compute="_compute_irpf",
        store=True,
        readonly=True
    )

    line_ids = fields.One2many(
        "sge.nomina.line",
        "nomina_id",
        string="Bonificaciones / Deducciones"
    )

    total_bonificaciones = fields.Float(compute="_compute_totales", store=True)
    total_deducciones = fields.Float(compute="_compute_totales", store=True)
    total_bruto = fields.Float(compute="_compute_totales", store=True)
    total_neto = fields.Float(compute="_compute_totales", store=True)

    pdf_justificante = fields.Binary(string="PDF justificante", attachment=True)

    state = fields.Selection(
        [
            ("draft", "Redactada"),
            ("confirm", "Confirmada"),
            ("paid", "Pagada"),
        ],
        default="draft",
        required=True
    )

    # -------------------- CÁLCULO IRPF --------------------
    @api.depends("sueldo_base", "irpf", "line_ids.importe", "line_ids.tipo")
    def _compute_irpf(self):
        for rec in self:
            bonificaciones = sum(
                rec.line_ids.filtered(lambda l: l.tipo == "bonificacion").mapped("importe")
            )
            base_irpf = rec.sueldo_base + bonificaciones
            rec.irpf_pagado = base_irpf * rec.irpf / 100 if rec.irpf else 0

    # -------------------- CÁLCULO TOTALES --------------------
    @api.depends("sueldo_base", "irpf_pagado", "line_ids")
    def _compute_totales(self):
        for rec in self:
            bon = sum(rec.line_ids.filtered(lambda l: l.tipo == "bonificacion").mapped("importe"))
            ded = sum(rec.line_ids.filtered(lambda l: l.tipo == "deduccion").mapped("importe"))

            rec.total_bonificaciones = bon
            rec.total_deducciones = ded

            rec.total_bruto = rec.sueldo_base + bon
            rec.total_neto = rec.total_bruto - ded - rec.irpf_pagado

    # -------------------- ACCIONES --------------------
    def action_confirm(self):
        self.state = "confirm"

    def action_paid(self):
        if not self.pdf_justificante:
            raise ValidationError("Debes adjuntar el justificante en PDF.")
        self.state = "paid"

    def action_set_draft(self):
        self.state = "draft"

    # -------------------- VALIDACIONES --------------------
    @api.constrains("sueldo_base")
    def _check_sueldo(self):
        for rec in self:
            if rec.sueldo_base <= 0:
                raise ValidationError("El sueldo base debe ser mayor que 0.")

    @api.constrains("irpf")
    def _check_irpf(self):
        for rec in self:
            if rec.irpf < 0 or rec.irpf > 45:
                raise ValidationError("El IRPF debe estar entre 0% y 45%.")

    @api.constrains("total_neto")
    def _check_neto(self):
        for rec in self:
            if rec.total_neto < 0:
                raise ValidationError("El sueldo neto no puede ser negativo.")


# --------------------------------------------------------------------------
#               MODELO HIJO: BONIFICACIÓN / DEDUCCIÓN
# --------------------------------------------------------------------------
class NominaLine(models.Model):
    _name = "sge.nomina.line"
    _description = "Línea de nómina (bonificación o deducción)"

    nomina_id = fields.Many2one("sge.nomina", string="Nómina", required=True)

    concepto = fields.Char(string="Concepto", required=True)
    importe = fields.Float(string="Importe (€)", digits=(16, 2), required=True)

    tipo = fields.Selection(
        [
            ("bonificacion", "Bonificación"),
            ("deduccion", "Deducción"),
        ],
        string="Tipo",
        required=True
    )

    @api.constrains("importe")
    def _check_importe(self):
        for rec in self:
            if rec.importe <= 0:
                raise ValidationError("El importe debe ser mayor que 0.")


# --------------------------------------------------------------------------
#               MODELO: DECLARACIÓN DE LA RENTA
# --------------------------------------------------------------------------
class DeclaracionRenta(models.Model):
    _name = "sge.declaracion.renta"
    _description = "Declaración anual de renta"

    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True)
    year = fields.Integer(string="Año", required=True)

    nomina_ids = fields.Many2many("sge.nomina", string="Nóminas incluidas")

    sueldo_bruto_total = fields.Float(compute="_compute_totales", store=True)
    impuestos_irpf_pagados = fields.Float(compute="_compute_totales", store=True)

    @api.depends("nomina_ids")
    def _compute_totales(self):
        for rec in self:
            rec.sueldo_bruto_total = sum(rec.nomina_ids.mapped("total_bruto"))
            rec.impuestos_irpf_pagados = sum(rec.nomina_ids.mapped("irpf_pagado"))

    @api.constrains("nomina_ids")
    def _check_nominas(self):
        for rec in self:
            if len(rec.nomina_ids) > 14:
                raise ValidationError("Una declaración solo puede tener 14 nóminas.")

            for nomina in rec.nomina_ids:
                if nomina.fecha.year != rec.year:
                    raise ValidationError("Todas las nóminas deben ser del mismo año.")

                if nomina.employee_id != rec.employee_id:
                    raise ValidationError("Todas deben ser del mismo empleado.")

