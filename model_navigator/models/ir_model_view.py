# Copyright 2025 JetModules <jetmodules@gmail.com>
# License AGPL-3 (https://www.odoo.com/documentation/16.0/legal/licenses.html#odoo-apps).

from odoo import models, _, fields
from odoo.exceptions import UserError


class IrModel(models.Model):
    _inherit = "ir.model"

    menu_path = fields.Char(
        string="Menu Path",
        compute="_compute_menu_path",
        help="Navigation path to access this model through the menu",
    )

    def _compute_menu_path(self):
        """Compute the menu path to access the model"""
        for record in self:
            path = False
            if record.model:
                # Search for action windows related to this model
                action = self.env["ir.actions.act_window"].search(
                    [
                        ("res_model", "=", record.model),
                        (
                            "binding_model_id",
                            "=",
                            False,
                        ),  # In this case, the action is not tied to a particular model and can be called from anywhere in the system
                    ],
                    limit=1,
                )
                if action:
                    # Search for menu items that use this action
                    menu_item = self.env["ir.ui.menu"].search(
                        [("action", "=", f"ir.actions.act_window,{action.id}")], limit=1
                    )
                    if menu_item:
                        path_items = []
                        current_menu = menu_item
                        # Build path from bottom to top
                        while current_menu:
                            path_items.insert(0, current_menu.name)
                            current_menu = current_menu.parent_id
                        path = " / ".join(path_items) if path_items else False
            record.menu_path = path

    def action_open_related_model_view(self):
        self.ensure_one()
        if not self.model:
            raise UserError(_("This model has no technical name defined"))
        ActWindow = self.env["ir.actions.act_window"]
        # Check if the model is a transient model (wizard)
        is_wizard = self.transient
        # Try to find action in order of specificity
        domain = [("res_model", "=", self.model)]
        if is_wizard:
            domain.append(("target", "=", "new"))
        # We use the binding_model_id to find a model-specific action
        action = ActWindow.search(
            domain
            + [("binding_model_id", "!=", False), ("binding_type", "=", "action")],
            limit=1,
        ) or ActWindow.search(domain, limit=1)
        if action:
            result = action.read()[0]
            # Get existing context and update it
            context = dict(self.env.context)
            result["context"] = context
            # Handle wizard-specific configurations
            if is_wizard:
                result["target"] = "new"
                result["flags"] = {
                    "action_buttons": True,
                    "headless": False,
                }
            return result
        # Default action if none found
        default_action = {
            "type": "ir.actions.act_window",
            "name": self.name,
            "res_model": self.model,
            "view_mode": "tree,form",
            "target": "new" if is_wizard else "current",
            "views": [(False, "tree"), (False, "form")],
            "context": dict(self.env.context),
        }
        # Add specific configurations for wizards
        if is_wizard:
            default_action.update(
                {
                    "view_mode": "form",
                    "views": [(False, "form")],
                    "flags": {
                        "action_buttons": True,
                        "headless": False,
                    },
                }
            )
        return default_action
