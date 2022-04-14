from random import choices
from string import ascii_letters, digits

def generate_invoice_id(max_digits=9):
    alpha_num = ascii_letters + digits
    return ''.join(choices(alpha_num, k=max_digits))
    