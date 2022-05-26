# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    # def write(self, vals):
    #     old_vals = {move.id: (move.state, move.ref, move.payment_reference) for move in self}
    #     res = super().write(vals)
    #     new_vals = {move.id: (move.state, move.ref, move.payment_reference) for move in self}
    #     for move in self:
    #         if move.state == 'draft' and old_vals[move.id][1] and not new_vals[move.id][1]:
    #             raise Exception()
    #     return res

    @api.onchange("invoice_date", "highest_name", "company_id")
    def _onchange_invoice_date(self):
        super().with_context(invoice_date_changed=True)._onchange_invoice_date()

    @api.onchange(
        "line_ids",
        "invoice_payment_term_id",
        "invoice_date_due",
        "invoice_cash_rounding_id",
        "invoice_vendor_bill_id",
    )
    def _onchange_recompute_dynamic_lines(self):
        super().with_context(
            invoice_date_due_changed=True
        )._onchange_recompute_dynamic_lines()

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_line_ids(self):
        current_invoice_lines = self.line_ids.filtered(
            lambda line: not line.exclude_from_invoice_tab
        )
        others_lines = self.line_ids - current_invoice_lines
        _logger.info(
            "Number of invoice_line_ids has changed. Now has %s invoice lines, %s other lines",
            len(current_invoice_lines),
            len(others_lines),
        )
        super()._onchange_invoice_line_ids()

    @api.onchange("line_ids")
    def _onchange_lines(self):
        current_invoice_lines = self.line_ids.filtered(
            lambda line: not line.exclude_from_invoice_tab
        )
        others_lines = self.line_ids - current_invoice_lines
        _logger.info(
            "Number of line_ids has changed. Now has %s invoice lines, %s other lines",
            len(current_invoice_lines),
            len(others_lines),
        )
        if len(current_invoice_lines) > 1:
            raise Exception()

    def _preprocess_taxes_map(self, taxes_map):
        _logger.info("We are in preprocess of taxes map HEHE")
        return super()._preprocess_taxes_map(taxes_map)

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        current_invoice_lines = self.line_ids.filtered(
            lambda line: not line.exclude_from_invoice_tab
        )
        if len(current_invoice_lines) > 1:
            raise Exception()
        if self._context.get("invoice_date_changed", False):
            _logger.info("Recomputing tax lines due to invoice_date changed.")
        elif self._context.get("invoice_date_due_changed", False):
            _logger.info("Recomputing tax lines due to invoice_date_due changed.")
        res = super()._recompute_tax_lines(recompute_tax_base_amount)
        current_invoice_lines = self.line_ids.filtered(
            lambda line: not line.exclude_from_invoice_tab
        )
        if len(current_invoice_lines) > 1:
            raise Exception()
        return res

    def _recompute_dynamic_lines(
        self, recompute_all_taxes=False, recompute_tax_base_amount=False
    ):
        for invoice in self:
            # Dispatch lines and pre-compute some aggregated values like taxes.
            if (
                recompute_all_taxes
                or any(line.recompute_tax_line for line in invoice.line_ids)
                or invoice.line_ids.tax_ids.flatten_taxes_hierarchy()._origin
                > invoice.line_ids.tax_line_id._origin
            ):
                invoice.line_ids.recompute_tax_line = False
                invoice._recompute_tax_lines()
            if recompute_tax_base_amount:
                invoice._recompute_tax_lines(recompute_tax_base_amount=True)
            if invoice.is_invoice(include_receipts=True):
                # Compute cash rounding.
                invoice._recompute_cash_rounding_lines()
                # Compute payment terms.
                invoice._recompute_payment_terms_lines()
                # Only synchronize one2many in onchange.
                _logger.info(
                    "C_recompute_dynamic_lines: origin %s with %s invoice lines, invoice %s with invoice lines %s",
                    invoice._origin,
                    invoice._origin._onchange_invoice_line_ids,
                    invoice,
                    invoice.invoice_line_ids,
                )
                if invoice != invoice._origin:
                    _logger.info(
                        "A_recompute_dynamic_lines: origin %s with %s invoice lines, invoice %s with invoice lines %s",
                        invoice._origin,
                        invoice._origin._onchange_invoice_line_ids,
                        invoice,
                        invoice.invoice_line_ids,
                    )
                    invoice.invoice_line_ids = invoice.line_ids.filtered(
                        lambda line: not line.exclude_from_invoice_tab
                    )
                    _logger.info(
                        "B_recompute_dynamic_lines: origin %s with %s invoice lines, invoice %s with invoice lines %s",
                        invoice._origin,
                        invoice._origin._onchange_invoice_line_ids,
                        invoice,
                        invoice.invoice_line_ids,
                    )


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange("exclude_from_invoice_tab")
    def _onchange_tab(self):
        raise Exception()
