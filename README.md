# 🖥️ Gestión de Ordenadores

------------------------------------------------------------------------

## 🧩 Introducción

Este módulo ha sido desarrollado como parte de la **Tarea 10 -- Modelos
Avanzados** del módulo **Sistemas de Gestión Empresarial (2ºDAM)**.

Su objetivo es gestionar los ordenadores de la empresa, sus componentes,
los usuarios que los utilizan y diversas automatizaciones avanzadas.

------------------------------------------------------------------------

## 🎯 Funcionalidades principales

-   Registro de ordenadores y sus componentes\
-   Relación Many2one entre ordenadores y usuarios\
-   Relación Many2many entre ordenadores y componentes\
-   Validación: la fecha de última modificación no puede ser futura\
-   Campo calculado automático para el precio total\
-   Vistas completas (lista y formulario)\
-   Menús y acciones en la interfaz\
-   Permisos de acceso configurados\
-   BONUS: Sistema de tags para indicar sistemas operativos

------------------------------------------------------------------------

## 🏗️ Estructura del módulo

    pc_management/
    ├── __init__.py
    ├── __manifest__.py
    ├── controllers/
    ├── demo/
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
        ├── templates.xml
        └── views.xml

------------------------------------------------------------------------

## 📁 Archivos importantes

### 1️⃣ `__manifest__.py`

El archivo describe el módulo y los datos que carga:

```
\# -*- coding: utf-8 -*-

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
```

➡️ Se han eliminado del manifest los archivos no utilizados (views.xml, templates.xml, demo.xml).

### 2️⃣ Modelos

📦 models/componente.py

Define los componentes de hardware:

```
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
```
    

🖥️ models/ordenador.py

Modelo principal del módulo:

```
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
```
         
   
🧠 Funciones importantes

Validación (_comprobar_fecha): evita fechas futuras.
Cálculo automático (_compute_total): suma el precio de los componentes.

### 3️⃣ Vistas

📦 views/componente_views.xml

Vista completa de componentes:

```
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
```


🖥️ views/ordenador_views.xml

Vista de ordenadores:

```
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
```

### 4️⃣ Seguridad

```
security/ir.model.access.csv
Permisos:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_pc_componente,access_pc_componente,model_pc_componente,,1,1,1,1
access_pc_ordenador,access_pc_ordenador,model_pc_ordenador,,1,1,1,1
```


```
security/pc_management_security.xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Archivo de seguridad del módulo pc_management -->
</odoo>
```

---

## 🚀 Instalación

1.  Copiar el módulo a la carpeta de addons de Odoo.\
2.  Reiniciar el servidor.\
3.  Actualizar la lista de aplicaciones.\
4.  Instalar **Gestión de Ordenadores**.

---

## 📌 Conclusión

Este módulo cumple todos los requisitos de la Tarea 10, incluyendo
relaciones avanzadas, validaciones, cálculos automáticos y menús
completos.

-------------------------------------------------------------------------

# 🚚 Gestión de Paquetería y Camiones

Este módulo proporciona un sistema completo para gestionar **paquetes**, **camiones**, **conductores** y el **seguimiento detallado de envíos** dentro de una empresa de transportes. Está diseñado siguiendo las buenas prácticas de desarrollo en Odoo, ofreciendo trazabilidad, organización y una estructura clara.

---

## 📁 1. Estructura del Módulo

```
paqueteria/
├── models/
│   ├── paquete.py
│   ├── camion.py
│   ├── seguimiento.py
│   └── __init__.py
├── views/
│   ├── paquete_views.xml
│   ├── camion_views.xml
│   ├── seguimiento_views.xml
│   ├── menu_views.xml
│   ├── templates.xml
│   └── views.xml
├── security/
│   ├── ir.model.access.csv
│   ├── paqueteria_security.xml
│   └── security.xml
├── demo/
│   └── demo.xml
├── static/description/index.html
├── __manifest__.py
└── __init__.py
```

Cada carpeta incluye elementos clave como:
- **models** → Lógica de negocio y estructura de datos.
- **views** → Interfaces XML de listas, formularios y menús.
- **security** → Permisos y reglas de acceso.
- **demo** → Datos de ejemplo.
- **static** → Archivos visuales para la vista previa en la App Store de Odoo.

---

## 📦 2. Funcionalidades Principales

### ✔️ Gestión de Paquetes
Permite administrar:
- Número de seguimiento.
- Remitente y destinatario.
- Dirección de entrega.
- Peso y contenido.
- Camión asignado.
- Historial detallado del seguimiento del envío.

### ✔️ Gestión de Camiones
Incluye:
- Matrícula.
- Conductor actual.
- Historial de conductores anteriores.
- Fecha de ITV.
- Notas de mantenimiento.
- Paquetes relacionados.

### ✔️ Seguimiento de Envíos
Permite registrar:
- Fecha exacta del evento.
- Estado del paquete.
- Ubicación.
- Notas opcionales.
- Asociación directa con un paquete.

Los eventos se ordenan cronológicamente y permiten trazar el recorrido del paquete.

---

## 🧩 3. Modelos Explicados

### 📌 3.1 Modelo `paqueteria.paquete`

```python
tracking = fields.Char(required=True)
remitente_id = fields.Many2one("res.partner", required=True)
destinatario_id = fields.Many2one("res.partner", required=True)
direccion_entrega = fields.Char()
peso = fields.Float()
descripcion = fields.Text()
camion_id = fields.Many2one("paqueteria.camion")
actualizaciones_ids = fields.One2many("paqueteria.seguimiento", "paquete_id")
```

### 📝 Explicación
- **tracking**: Identificador único del envío.  
- **remitente/destinatario**: Integración directa con el módulo de contactos de Odoo.  
- **camion_id**: Permite asignar un vehículo al envío.  
- **actualizaciones_ids**: Registro cronológico del seguimiento.

### 🔧 Comportamiento
- Al crear un paquete, puedes asignarle un camión opcionalmente.
- El historial del envío se muestra como una lista inteligente dentro del formulario.

---

### 📌 3.2 Modelo `paqueteria.camion`

```python
matricula = fields.Char(required=True)
conductor_actual_id = fields.Many2one("hr.employee")
antiguos_conductores_ids = fields.Many2many("hr.employee")
fecha_itv = fields.Date()
notas_mantenimiento = fields.Text()
paquetes_ids = fields.One2many("paqueteria.paquete", "camion_id")
```

### 📝 Explicación
- Control de flota mediante matrícula y conductores.
- Historial de mantenimiento.
- Consulta rápida de paquetes transportados.

---

### 📌 3.3 Modelo `paqueteria.seguimiento`

```python
paquete_id = fields.Many2one("paqueteria.paquete", required=True, ondelete="cascade")
fecha = fields.Datetime(default=fields.Datetime.now)
ubicacion = fields.Char()
estado = fields.Selection([...], required=True)
notas = fields.Text()
```

### 📝 Explicación
- **fecha**: Se genera automáticamente.
- **estado**: Ciclo del paquete:
  - recibido  
  - en camino  
  - en reparto  
  - entregado  
  - incidencia  
- **ondelete="cascade"**: si se borra el paquete, se eliminan sus seguimientos.

Es un registro histórico del envío.

---

## 🖼️ 4. Vistas XML

### 📄 4.1 `paquete_views.xml`
Incluye:
- Vista listado (árbol).
- Vista formulario.
- Búsquedas.
- Acciones inteligentes.

Muestra campos clave como tracking, remitente, destinatario y estado del paquete.

---

### 🚚 4.2 `camion_views.xml`
Incluye:
- Lista con matrícula, conductor y ITV.
- Formulario del camión.
- Sección de paquetes asignados.

---

### 📍 4.3 `seguimiento_views.xml`
Permite gestionar:
- Nuevos eventos de seguimiento.
- Orden cronológico.
- Relación directa con el paquete.

---

### 📋 4.4 `menu_views.xml`
Define la estructura principal:

```
Paquetería
 ├── Paquetes
 ├── Camiones
 └── Seguimientos
```

---

## 🔐 5. Seguridad del Módulo

### ✔️ `ir.model.access.csv`
Define permisos de lectura, escritura, creación y eliminación.

Ejemplo:
```
paqueteria.paquete,access_paqueteria_paquete,model_paqueteria_paquete,base.group_user,1,1,1,1
```

### ✔️ `paqueteria_security.xml`
Define grupos y permisos adicionales.

### ✔️ `security.xml`
Reglas de acceso basadas en dominios si se aplican.

---

## ⚙️ 6. Manifest (`__manifest__.py`)

Contiene:
- Nombre del módulo  
- Autor  
- Descripción  
- Versionado  
- Dependencias  
- Vistas, modelos y seguridad cargada  
- Datos demo  
- Configuración como aplicación  

Es el archivo inicial que Odoo lee para cargar el módulo.

---

## 🧪 7. Datos Demo

Incluye ejemplos de:
- Paquetes
- Camiones
- Seguimientos

Útiles para pruebas iniciales.

---

## 🛠️ 8. Instalación

1. Copia la carpeta `paqueteria` a tu directorio de `addons`.
2. Reinicia Odoo:
```bash
sudo systemctl restart odoo
```
3. Activa modo desarrollador.
4. Actualiza lista de módulos.
5. Instala **Gestión de Paquetería y Camiones**.

---

# ✨ Autor
### Autor: **Javier Alcaraz Martín**

---
