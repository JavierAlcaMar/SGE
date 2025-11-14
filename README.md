📘 Gestión de Ordenadores — Módulo Odoo
Autor: Javier Alcaraz Martín

🧩 Introducción
Este módulo ha sido desarrollado como parte de la Tarea 10 – Modelos Avanzados del módulo Sistemas de Gestión Empresarial (2ºDAM).
Su objetivo es gestionar los ordenadores de la empresa, sus componentes, los usuarios que los utilizan y diversas automatizaciones avanzadas pedidas en el enunciado.

🎯 Funcionalidades principales
✔ Registro de ordenadores y sus componentes
✔ Relación Many2one entre ordenadores y usuarios
✔ Relación Many2many entre ordenadores y componentes
✔ Validación: la fecha de última modificación no puede ser futura
✔ Campo calculado automático para el precio total
✔ Vistas completas (lista y formulario)
✔ Menús y acciones en la interfaz
✔ Permisos de acceso configurados
✔ BONUS: Sistema de tags para indicar sistemas operativos usando many2many_tags

🏗️ Estructura del módulo
pc_management/
├── __init__.py
├── __manifest__.py
├── controllers/         ← No se utiliza en este módulo
├── demo/                ← Datos demo generados por scaffold (no usados)
├── models/
│   ├── __init__.py
│   ├── componente.py
│   ├── ordenador.py
├── security/
│   ├── ir.model.access.csv
│   └── pc_management_security.xml
└── views/
    ├── componente_views.xml
    ├── ordenador_views.xml
    ├── templates.xml     ← No utilizado
    └── views.xml         ← No utilizado
Solo se describen los archivos modificados y necesarios.

📁 Archivos del módulo
1️⃣ __manifest__.py
El archivo describe el módulo y los datos que carga:
# -*- coding: utf-8 -*-
{
    'name': "Gestion de Ordenadores",

    'summary': "Registro de ordenadores, componentes y usuarios",

    'description': """
Long description of module's purpose
    """,

    'author': "Javier Alcaraz Martin",
    'website': "https://www.bembes.com",

    'category': 'IT',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/pc_management_security.xml',
        'security/ir.model.access.csv',
        'views/ordenador_views.xml',
        'views/componente_views.xml',
    ],

    'installable': True,
    'application': True,
}
➡️ Se han eliminado del manifest los archivos no utilizados (views.xml, templates.xml, demo.xml).

2️⃣ Modelos
📦 models/componente.py
Define los componentes de hardware:
from odoo import models, fields

class PcComponente(models.Model):
    _name = 'pc.componente'
    _description = 'Componente de ordenador'

    nombre = fields.Char(string="Nombre técnico", required=True)
    especificaciones = fields.Text(string="Especificaciones")
    precio = fields.Monetary(string="Precio", currency_field="currency_id")
    currency_id = fields.Many2one(
        'res.currency',
        string="Moneda",
        default=lambda self: self.env.company.currency_id
    )
    
🖥️ models/ordenador.py
Modelo principal del módulo:
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class PcOrdenador(models.Model):
    _name = 'pc.ordenador'
    _description = 'Ordenador de la empresa'

    numero_equipo = fields.Char(string="Número de equipo", required=True)
    user_id = fields.Many2one("res.users", string="Usuario")
    components_ids = fields.Many2many("pc.componente", string="Componentes")
    ultima_mod = fields.Date(string="Última modificación")
    precio_total = fields.Monetary(string="Precio total", compute="_compute_total", store=True)
    incidencias = fields.Text(string="Incidencias")
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id)
    tags = fields.Many2many('pc.tag', string="Sistemas operativos", widget="many2many_tags")

    @api.constrains('ultima_mod')
    def _comprobar_fecha(self):
        for record in self:
            if record.ultima_mod and record.ultima_mod > date.today():
                raise ValidationError("La fecha no puede ser futura")

    @api.depends("components_ids.precio")
    def _compute_total(self):
        for record in self:
            record.precio_total = sum(component.precio for component in record.components_ids)
            
🧠 Funciones importantes
Validación (_comprobar_fecha): evita fechas futuras.
Cálculo automático (_compute_total): suma el precio de los componentes.
Tags: BONUS de la práctica.

3️⃣ Vistas
📦 views/componente_views.xml
Vista completa de componentes:
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="view_componente_form" model="ir.ui.view">
        <field name="name">pc.componente.form</field>
        <field name="model">pc.componente</field>
        <field name="arch" type="xml">
            <form string="Componente">
                <sheet>
                    <group>
                        <field name="nombre"/>
                        <field name="especificaciones"/>
                        <field name="precio"/>
                        <field name="currency_id"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_componente_list" model="ir.ui.view">
        <field name="name">pc.componente.list</field>
        <field name="model">pc.componente</field>
        <field name="arch" type="xml">
            <list>
                <field name="nombre"/>
                <field name="precio"/>
                <field name="currency_id"/>
            </list>
        </field>
    </record>

    <record id="action_pc_componente" model="ir.actions.act_window">
        <field name="name">Componentes</field>
        <field name="res_model">pc.componente</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_pc_componente"
              name="Componentes"
              parent="menu_pc_management_root"
              action="action_pc_componente"
              sequence="10"/>

</odoo>

🖥️ views/ordenador_views.xml
Vista de ordenadores:
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="view_ordenador_form" model="ir.ui.view">
        <field name="name">pc.ordenador.form</field>
        <field name="model">pc.ordenador</field>
        <field name="arch" type="xml">
            <form string="Ordenador">
                <sheet>
                    <group>
                        <field name="numero_equipo"/>
                        <field name="user_id"/>
                        <field name="ultima_mod"/>
                        <field name="incidencias"/>
                        <field name="tags" widget="many2many_tags"/>
                    </group>
                    <group>
                        <field name="components_ids"/>
                        <field name="precio_total" readonly="1"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_ordenador_list" model="ir.ui.view">
        <field name="name">pc.ordenador.list</field>
        <field name="model">pc.ordenador</field>
        <field name="arch" type="xml">
            <list>
                <field name="numero_equipo"/>
                <field name="user_id"/>
                <field name="precio_total"/>
                <field name="ultima_mod"/>
            </list>
        </field>
    </record>

    <record id="action_pc_ordenador" model="ir.actions.act_window">
        <field name="name">Ordenadores</field>
        <field name="res_model">pc.ordenador</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_pc_management_root"
              name="Gestión de Ordenadores"
              sequence="10"/>

    <menuitem id="menu_pc_ordenador"
              name="Ordenadores"
              parent="menu_pc_management_root"
              action="action_pc_ordenador"
              sequence="20"/>

</odoo>

4️⃣ Seguridad
security/ir.model.access.csv
Permisos:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_pc_componente,access_pc_componente,model_pc_componente,,1,1,1,1
access_pc_ordenador,access_pc_ordenador,model_pc_ordenador,,1,1,1,1
security/pc_management_security.xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Archivo de seguridad del módulo pc_management -->
</odoo>

🚀 Instalación
Copiar el módulo a la carpeta de addons de Odoo.
Reiniciar el servidor.
En el menú Aplicaciones, pulsar Actualizar lista.
Instalar Gestión de Ordenadores.

📌 Conclusión
Este módulo implementa todas las funcionalidades pedidas en la Tarea 10, incluyendo:
✔ Modelos avanzados
✔ Relaciones M2O y M2M
✔ Validaciones
✔ Campos calculados
✔ Vistas completas
✔ Menús operativos
✔ Permisos configurados
✔ BONUS: widget tags
