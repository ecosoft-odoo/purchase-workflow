# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class PurchaseCreateInvoicePlan(models.TransientModel):
    _inherit = "purchase.create.invoice.plan"

    advance = fields.Boolean(
        string="Deposit on 1st Invoice",
        default=False,
    )

    def purchase_create_invoice_plan(self):
        self = self.with_context(advance=self.advance)
        return super().purchase_create_invoice_plan()
