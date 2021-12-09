# Copyright NuoBiT Solutions - Eric Antones <eantones@nuobit.com>
# Copyright NuoBiT Solutions - Kilian Niubo <kniubo@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import _

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class SaleOrderExporter(Component):
    _name = "oxigesti.sale.order.exporter"
    _inherit = "oxigesti.exporter"

    _apply_on = "oxigesti.sale.order"

    def run_order_data(self, binding, clear=False):
        external_id = self.binder.to_external(binding)
        if not external_id:
            return _("Sale is not linked with a Oxigesti sales order")

        order_number, order_date = None, None
        if not clear:
            order_number = binding.name

            order_date = binding.date_order

        values = {
            "Odoo_Numero_Albaran": order_number,
            "Odoo_Fecha_Generado_Albaran": order_date,
        }
        self.backend_adapter.write(external_id, values)

    def run_invoice_data(self, binding, invoice, clear=False):
        external_id = self.binder.to_external(binding)
        if not external_id:
            return _("Sale is not linked with a Oxigesti sales order")

        invoice_number, invoice_date = None, None
        if not clear:
            invoice_number = invoice.number
            invoice_date = invoice.date_invoice

        values = {
            "Odoo_Numero_Factura": invoice_number,
            "Odoo_Fecha_Generada_Factura": invoice_date,
        }
        self.backend_adapter.write(external_id, values)
