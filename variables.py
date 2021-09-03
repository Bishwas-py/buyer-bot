import random
import string
from textwrap import wrap

class BESTBUY:
    NEWPASSWORD = "Aparb003$#@!"+random.choice(wrap(string.ascii_letters, 7))