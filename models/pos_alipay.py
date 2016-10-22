# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)



class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
        ('credit', _('Credit Card'))
    ])

#joray start del
#class PosAlipayConfiguration(models.Model):
#    _name = 'pos_alipay.configuration'
#
#    name = fields.Char(required=True, help='Name of this Alipay configuration')
#    merchant_id = fields.Char(string='Merchant ID', required=True, help='ID of the merchant to authenticate him on the payment provider server')
#    merchant_pwd = fields.Char(string='Merchant Password', required=True, help='Password of the merchant to authenticate him on the payment provider server')
#joray end del
#joray start
class PosAlipayConfiguration(models.Model):
    _name = 'pos_alipay.configuration'

    name = fields.Char(required=True, help='Name of this alipay configuration')
    alipay_partner_account = fields.Char(string='alipay partner account', required=True, help='alipay config1')
    alipay_partner_key = fields.Char(string='alipay partner key', required=True, help='alipay config2')
    alipay_seller_email = fields.Char(string='alipay seller email', required=True, help='alipay config3')
    alipay_interface_type = fields.Char(string='alipay interface type', required=True, help='alipay config4')
#joray end

class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    alipay_card_number = fields.Char(string='Card Number', help='The last 4 numbers of the card used to pay')
    alipay_prefixed_card_number = fields.Char(string='Card Number', compute='_compute_prefixed_card_number', help='The card number used for the payment.')
    alipay_card_brand = fields.Char(string='Card Brand', help='The brand of the payment card (e.g. Visa, AMEX, ...)')
    alipay_card_owner_name = fields.Char(string='Card Owner Name', help='The name of the card owner')
    alipay_ref_no = fields.Char(string='Alipay reference number', help='Payment reference number from Alipay Pay')
    alipay_record_no = fields.Char(string='Alipay record number', help='Payment record number from Alipay Pay')
    alipay_invoice_no = fields.Char(string='Alipay invoice number', help='Invoice number from Alipay Pay')

    @api.one
    def _compute_prefixed_card_number(self):
        if self.alipay_card_number:
            self.alipay_prefixed_card_number = "********" + self.alipay_card_number
        else:
            self.alipay_prefixed_card_number = ""


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    pos_alipay_config_id = fields.Many2one('pos_alipay.configuration', string='Alipay configuration', help='The configuration of Alipay used for this journal')


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _payment_fields(self, ui_paymentline):
        fields = super(PosOrder, self)._payment_fields(ui_paymentline)

        fields.update({
            'card_number': ui_paymentline.get('alipay_card_number'),
            'card_brand': ui_paymentline.get('alipay_card_brand'),
            'card_owner_name': ui_paymentline.get('alipay_card_owner_name'),
            'ref_no': ui_paymentline.get('alipay_ref_no'),
            'record_no': ui_paymentline.get('alipay_record_no'),
            'invoice_no': ui_paymentline.get('alipay_invoice_no')
        })

        return fields

    def add_payment(self, data):
        statement_id = super(PosOrder, self).add_payment(data)
        statement_lines = self.env['account.bank.statement.line'].search([('statement_id', '=', statement_id),
                                                                         ('pos_statement_id', '=', self.id),
                                                                         ('journal_id', '=', data['journal']),
                                                                         ('amount', '=', data['amount'])])

        # we can get multiple statement_lines when there are >1 credit
        # card payments with the same amount. In that case it doesn't
        # matter which statement line we pick, just pick one that
        # isn't already used.
        for line in statement_lines:
            if not line.alipay_card_brand:
                line.alipay_card_brand = data.get('card_brand')
                line.alipay_card_number = data.get('card_number')
                line.alipay_card_owner_name = data.get('card_owner_name')

                line.alipay_ref_no = data.get('ref_no')
                line.alipay_record_no = data.get('record_no')
                line.alipay_invoice_no = data.get('invoice_no')

                break

        return statement_id


class AutoVacuum(models.AbstractModel):
    _inherit = 'ir.autovacuum'

    @api.model
    def power_on(self, *args, **kwargs):
        self.env['pos_alipay.alipay_transaction'].cleanup_old_tokens()
        return super(AutoVacuum, self).power_on(*args, **kwargs)
