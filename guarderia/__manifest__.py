# -*- coding: utf-8 -*-
{
    "name": "Guardería",
    "summary": "Servicio de guardería con delegación (Empleado + Evento)",
    "description": """
Crea un modelo Servicio de Guardería usando multiherencia por delegación:
- Delegación a hr.employee (monitor)
- Delegación a calendar.event (horario / evento)
Incluye descripción y rango de edad.
""",
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    "category": "Human Resources",
    "version": "1.0.0",
    "depends": ["base", "hr", "calendar"],
    "data": [
        "security/ir.model.access.csv",
        "views/views.xml",
        # "views/templates.xml",  # opcional, no necesario para la tarea
    ],
    # "demo": [
    #     "demo/demo.xml",
    # ],
    "installable": True,
    "application": True,
}

