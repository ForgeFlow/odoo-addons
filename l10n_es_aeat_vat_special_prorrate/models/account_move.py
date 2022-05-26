# Copyright NuoBiT - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def prorate_context(invoice):
    return {
        "date": invoice.date
        or invoice.invoice_date
        or fields.Date.context_today(invoice),
        "company_id": invoice.company_id.id,
    }


class AccountMove(models.Model):
    _inherit = "account.move"

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        self = self.with_context(prorate=prorate_context(self))
        return super(AccountMove, self)._recompute_tax_lines(
            recompute_tax_base_amount=recompute_tax_base_amount
        )

    @api.onchange("invoice_date", "date")
    def _onchange_dates(self):
        _logger.info(
            "A_onchange_dates: origin %s with %s invoice lines, invoice %s with invoice lines %s",
            self._origin,
            self._origin.invoice_line_ids,
            self,
            self.invoice_line_ids,
        )
        self.with_context(invoice_date_changed=True)._recompute_tax_lines()
        _logger.info(
            "B_onchange_dates: origin %s with %s invoice lines, invoice %s with invoice lines %s",
            self._origin,
            self._origin.invoice_line_ids,
            self,
            self.invoice_line_ids,
        )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def _get_price_total_and_subtotal_model(
        self,
        price_unit,
        quantity,
        discount,
        currency,
        product,
        partner,
        taxes,
        move_type,
    ):
        if taxes:
            taxes = taxes.with_context(prorate=prorate_context(self.move_id))
        return super()._get_price_total_and_subtotal_model(
            price_unit, quantity, discount, currency, product, partner, taxes, move_type
        )
