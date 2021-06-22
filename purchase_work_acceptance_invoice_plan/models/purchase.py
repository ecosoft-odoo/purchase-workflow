# Copyright 2020 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _get_product_qty(self):
        installment_id = self._context.get("installment_id", False)
        if installment_id:
            installment = self.env["purchase.invoice.plan"].browse(installment_id)
            return self.product_qty * (installment.percent / 100)
        return super()._get_product_qty()

    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=move)
        # With wa_id, make correction to the deposit line too (the -qty)
        wa_id = self.env.context.get("wa_id")
        if wa_id:
            wa = self.env["work.acceptance"].browse(wa_id)
            percent = wa.installment_id.percent
            if res.get("quantity", 0) < 0:
                res["quantity"] = res["quantity"] * percent / 100
        return res


class PurchaseInvoicePlan(models.Model):
    _inherit = "purchase.invoice.plan"

    def name_get(self):
        result = []
        for rec in self:
            result.append(
                (
                    rec.id,
                    "%s %s : %s -- %s %s"
                    % (
                        "Invoice Plan",
                        rec.installment,
                        rec.plan_date,
                        rec.percent,
                        "%",
                    ),
                )
            )
        return result
