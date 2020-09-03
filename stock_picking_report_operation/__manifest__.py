# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': "Stock picking operation",
    'description': """Stock picking operation""",
    'version': '11.0.1.0.0',
    'author': 'NuoBiT Solutions, S.L., Eric Antones',
    'license': 'AGPL-3',
    'category': 'Warehouse',
    'website': 'https://github.com/nuobit',
    'depends': [
        'stock',
    ],
    'data': [
        'report/report.xml',
        'views/stock_picking_report_operation.xml.xml',
    ],
    'installable': True,
}
