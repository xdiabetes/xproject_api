# common payment functions

from xapp.api_v1.consts import InvoiceConsts


def validate_invoice(invoice):
    return invoice.fake or invoice.status not in [InvoiceConsts.PAYED,
                                                  InvoiceConsts.INTERNAL,
                                                  InvoiceConsts.IN_PAYMENT] and invoice.amount >= 1000
