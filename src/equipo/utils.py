############ Regex Test ############

import re

def email_regex(email):
    if not re.match(r"^[_A-Za-z0-9-]+@cpp\.edu$", email):
        return False
    else:
        return True
