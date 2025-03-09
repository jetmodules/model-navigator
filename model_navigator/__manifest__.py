# Copyright 2025 JetModules <jetmodules@gmail.com>
# License AGPL-3 (https://www.odoo.com/documentation/16.0/legal/licenses.html#odoo-apps).

{
    "name": "Model Navigator",
    "summary": "ir.model.view redirect",
    "description": "Extends ir.model.view to enable navigation to the views of the related model.",
    "version": "16.0.1.0.0",
    "category": "Tools",
    "author": "JetModules",
    "license": "AGPL-3",
    "images": ["static/description/banner.png"],
    "application": False,
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        "views/ir_model_view.xml",
    ],
}
