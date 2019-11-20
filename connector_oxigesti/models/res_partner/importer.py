# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import re

from odoo import _

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import (
    mapping, external_to_m2o, only_create)


class ResPartnerBatchImporter(Component):
    """ Import the Oxigesti Partners.

    For every partner in the list, a delayed job is created.
    """
    _name = 'oxigesti.res.partner.delayed.batch.importer'
    _inherit = 'oxigesti.delayed.batch.importer'
    _apply_on = 'oxigesti.res.partner'


class ResPartnerImporter(Component):
    _name = 'oxigesti.res.partner.importer'
    _inherit = 'oxigesti.importer'
    _apply_on = 'oxigesti.res.partner'
