from xapp.api_v1.modules.payment.pep import pep_prepare_for_payment, pep_verify_payment, pep_refund_payment
from xapp.api_v1.modules.payment.vandar import vandar_prepare_for_payment, vandar_verify_payment

# payment gates
VANDAR = 'VANDAR'
PEP = 'PEP'
PAYPING = 'PAYPING'
LOCAL = 'LOCAL'

pg_displays = {
    VANDAR: 'وندار',
    PEP: 'پاسارگاد',
    PAYPING: 'پی پینگ',
    LOCAL: 'LOCAL'
}

pg_gates = ((VANDAR, 'وندار'),
            (PEP, 'پاسارگاد'),
            (LOCAL, 'لوکال'),
            (PAYPING, 'پی پینگ'))

pg_gates_array = [VANDAR, PEP, PAYPING, LOCAL]

# payment gate prepare_for_payment and verify_payment functions
pg_functions = {
    VANDAR: {
        'prepare_for_payment': vandar_prepare_for_payment,
        'verify_payment': vandar_verify_payment,
        'refund_payment': None
    },
    PEP: {
        'prepare_for_payment': pep_prepare_for_payment,
        'verify_payment': pep_verify_payment,
        'refund_payment': pep_refund_payment
    }
}