import json
import math

import requests
from django.shortcuts import get_object_or_404
from django.urls import reverse

from xproject.secret import VANDAR_API_KEY, DEMO
from xapp.api_v1.consts import InvoiceConsts
from xapp.api_v1.modules.payment.common import validate_invoice
from xapp.models import Invoice


def vandar_prepare_for_payment(invoice, request):
    """
    :param invoice: invoice to be prepared for payment
    :param request: django http request object
    :return: on success: {'redirect_to': 'redirect_address', status: 200}
             on error : {'status': status_code, 'details': 'Error descriptions' }
    """

    from xapp.api_v1.modules.payment.index import VANDAR

    # validate invoice
    if not validate_invoice(invoice):
        return {'status': 400, 'details': ["Invalid Invoice", ]}

    # generate callback url

    callback = request.build_absolute_uri(
        reverse("payment_verify",
                kwargs={
                    'invoice_uuid': invoice.uuid,
                    'pg': VANDAR})
    )

    callback = callback.replace('http', 'https')

    if DEMO:
        callback = callback.replace('127.0.0.1:8000', 'xapp.app')

    result = requests.post(
        'https://ipg.vandar.io/api/v3/send',
        data={
            'api_key': VANDAR_API_KEY,
            'amount': math.ceil(invoice.amount) * 10,
            'callback_url': callback
        }
    )

    result_data = json.loads(result.text)

    if result_data['status'] != 1:
        return {'details': result_data['errors'], 'status': 503}

    # todo: change invoice status to in payment
    invoice.token = result_data['token']
    invoice.save()

    return {'redirect_to': 'https://ipg.vandar.io/v3/%s' % result_data['token'], 'status': 200}


def vandar_verify_payment(invoice):
    """Check payment verification"""

    result = requests.post(
        url="https://ipg.vandar.io/api/v3/verify",
        data={
            "api_key": VANDAR_API_KEY,
            "token": invoice.token
        }
    )
    result = json.loads(result.text)

    if result['status'] == 1:
        invoice.status = InvoiceConsts.PAYED
        invoice.transId = result['transId']
        invoice.card_number = result['cardNumber']
    else:
        invoice.status = InvoiceConsts.REJECTED

    invoice.save()

    if invoice.status == InvoiceConsts.PAYED:
        return True
    return False
