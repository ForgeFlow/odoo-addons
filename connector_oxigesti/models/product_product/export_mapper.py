# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import re

from odoo import _

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (
    mapping, external_to_m2o, only_create, changed_by)


def nullif(field):
    def modifier(self, record, to_attr):
        value = record[field]
        return value and value.strip() or None

    return modifier


class ProductProductExportMapper(Component):
    _name = 'oxigesti.product.product.export.mapper'
    _inherit = 'oxigesti.export.mapper'

    _apply_on = 'oxigesti.product.product'

    direct = [
        ('id', 'Id'),
        (nullif('barcode'), 'CodigoAlternativo'),
        ('list_price', 'Importe'),
    ]

    @mapping
    def Articulo(self, record):
        default_code = (record.default_code and
                        record.default_code.strip() and
                        record.default_code or None)
        if not default_code:
            raise AssertionError("The Odoo product with ID %i and Name '%s' "
                                 "has no Internal reference. "
                                 "Please assign one and requeue the job." % (record.id, record.name))

        return {'Articulo': default_code}

    @changed_by('name')
    @mapping
    def DescripcionArticulo(self, record):
        return {'DescripcionArticulo': record.name[:250]}

    @mapping
    def Familia(self, record):
        return {'Familia': 0}
