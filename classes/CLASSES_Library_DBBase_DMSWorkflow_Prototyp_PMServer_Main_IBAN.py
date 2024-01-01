# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:55

"""iban.py 0.3 - Create or check International Bank Account Numbers (IBAN).

Copyright (C) 2002-2003, Thomas Günther (toms-cafe.de)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

Usage as module:
    from iban import *

    code, bank, account = "DE", "12345678", "123456789"
    try:
        iban = create_iban(code, bank, account)
    except IBANError, err:
        print err
    else:
        print "  Correct IBAN: %s << %s ?? %s %s" % (iban, code, bank, account)

    iban = "de58123456780123456789".upper()
    try:
        code, checksum, bank, account = check_iban(iban)
    except IBANError, err:
        print err
    else:
        print "  Correct IBAN: %s >> %s %s %s %s" % (iban, code, checksum,
                                                     bank, account)
"""

__all__ = ["create_iban", "check_iban", "IBANError"]

usage = \
"""Create or check International Bank Account Numbers (IBAN).

Usage: iban <iban>
       iban <country> <bank/branch> <account>
       iban -h | -f | -e | -t

 e.g.: iban DE58123456780123456789
       iban DE 12345678 123456789

       <iban>         is the International Bank Account Number (IBAN)
       <country>      is the Country Code from ISO 3166
       <bank/branch>  is the Bank/Branch Code part of the IBAN from ISO 13616
       <account>      is the Account Number including check digits

       iban -h        prints this message
       iban -f        prints a table with the country specific iban format
       iban -e        prints an example for each country
       iban -t        prints some test data

Information about IBAN are from European Committee for Banking Standards
(www.ecbs.org/iban.htm). IBAN is an ISO standard (ISO 13616: 1997).
"""

class Country:
    """Class for country specific iban data."""

    def __init__(self, name, code, bank_form, acc_form):
        """Constructor for Country objects.

        Arguments:
            name      - Name of the country
            code      - Country Code from ISO 3166
            bank_form - Format of bank/branch code part (e.g. "0 4a 0 ")
            acc_form  - Format of account number part (e.g. "0  11  2n")
        """
        self.code = code
        self.name = name
        self.bank = self._decode_format(bank_form)
        self.acc  = self._decode_format(acc_form)

    def bank_lng(self):
        return reduce(lambda sum, part: sum + part[0], self.bank, 0)

    def acc_lng(self):
        return reduce(lambda sum, part: sum + part[0], self.acc, 0)

    def total_lng(self):
        return 4 + self.bank_lng() + self.acc_lng()

    def _decode_format(self, form):
        form_list = []
        for part in form.split(" "):
            if part:
                a_n = part[-1]
                if a_n in ("a", "n"):
                    part = part[:-1]
                else:
                    a_n = "an"
                lng = int(part)
                form_list.append((lng, a_n))
        return tuple(form_list)

# BBAN data from ISO 13616, Country codes from ISO 3166 (www.iso.org).
iban_data = (Country("Andorra",        "AD", "0  4n 4n", "0  12   0 "),
             Country("Austria",        "AT", "0  5n 0 ", "0  11n  0 "),
             Country("Belgium",        "BE", "0  3n 0 ", "0   7n  2n"),
             Country("Switzerland",    "CH", "0  5n 0 ", "0  12   0 "),
             Country("Czech Republic", "CZ", "0  4n 0 ", "0  16n  0 "),
             Country("Germany",        "DE", "0  8n 0 ", "0  10n  0 "),
             Country("Denmark",        "DK", "0  4n 0 ", "0   9n  1n"),
             Country("Spain",          "ES", "0  4n 4n", "2n 10n  0 "),
             Country("Finland",        "FI", "0  6n 0 ", "0   7n  1n"),
             Country("Faroe Islands",  "FO", "0  4n 0 ", "0   9n  1n"),
             Country("France",         "FR", "0  5n 5n", "0  11   2n"),
             Country("United Kingdom", "GB", "0  4a 6n", "0   8n  0 "),
             Country("Gibraltar",      "GI", "0  4a 0 ", "0  15   0 "),
             Country("Greenland",      "GL", "0  4n 0 ", "0   9n  1n"),
             Country("Greece",         "GR", "0  3n 4n", "0  16   0 "),
             Country("Hungary",        "HU", "0  3n 4n", "1  15   1 "),
             Country("Ireland",        "IE", "0  4a 6n", "0   8n  0 "),
             Country("Iceland",        "IS", "0  4n 0 ", "0  18n  0 "),
             Country("Italy",          "IT", "1a 5n 5n", "0  12   0 "),
             Country("Liechtenstein",  "LI", "0  5n 0 ", "0  12   0 "),
             Country("Luxembourg",     "LU", "0  3n 0 ", "0  13   0 "),
             Country("Latvia",         "LV", "0  4a 0 ", "0  13   0 "),
             Country("Monaco",         "MC", "0  5n 5n", "0  11   2n"),
             Country("Netherlands",    "NL", "0  4a 0 ", "0  10n  0 "),
             Country("Norway",         "NO", "0  4n 0 ", "0   6n  1n"),
             Country("Poland",         "PL", "0  8n 0 ", "0  16   0 "),
             Country("Portugal",       "PT", "0  4n 4n", "0  11n  2n"),
             Country("Sweden",         "SE", "0  3n 0 ", "0  16n  1n"),
             Country("Slovenia",       "SI", "0  5n 0 ", "0   8n  2n"),
             Country("San Marino",     "SM", "1a 5n 5n", "0  12   0 "))

def country_data(code):
    """Search the country code in the iban_data list."""
    for country in iban_data:
        if country.code == code:
            return country
    return None

def mod97(digit_string):
    """Modulo 97 for huge numbers given as digit strings.

    This function is a prototype for a JavaScript implementation.
    In Python this can be done much easier: long(digit_string) % 97.
    """
    m = 0
    for d in digit_string:
        m = (m * 10 + int(d)) % 97
    return m

def fill0(s, l):
    """Fill the string with leading zeros until length is reached."""
    import string
    return string.zfill(s, l)

def checksum_iban(iban):
    """Calculate 2-digit checksum of an IBAN."""
    code     = iban[:2]
    checksum = iban[2:4]
    bban     = iban[4:]

    # Assemble digit string
    digits = ""
    for ch in bban:
        if ch.isdigit():
            digits += ch
        else:
            digits += str(ord(ch) - ord("A") + 10)
    for ch in code:
        digits += str(ord(ch) - ord("A") + 10)
    digits += checksum

    # Calculate checksum
    checksum = 98 - mod97(digits)
    return fill0(str(checksum), 2)

def fill_account(country, account):
    """Fill the account number part of IBAN with leading zeros."""
    return fill0(account, country.acc_lng())

def invalid_part(form_list, iban_part):
    """Check if syntax of the part of IBAN is invalid."""
    for lng, a_n in form_list:
        if lng > len(iban_part):
            lng = len(iban_part)
        for ch in iban_part[:lng]:
            a = ("A" <= ch <= "Z")
            n = ch.isdigit()
            if (not a and not n) or \
               (not a and a_n == "a") or \
               (not n and a_n == "n"):
                return 1
        iban_part = iban_part[lng:]
    return 0

def invalid_bank(country, bank):
    """Check if syntax of the bank/branch code part of IBAN is invalid."""
    return len(bank) != country.bank_lng() or \
           invalid_part(country.bank, bank)

def invalid_account(country, account):
    """Check if syntax of the account number part of IBAN is invalid."""
    return len(account) > country.acc_lng() or \
           invalid_part(country.acc, fill_account(country, account))

def calc_iban(country, bank, account):
    """Calculate the checksum and assemble the IBAN."""
    account = fill_account(country, account)
    checksum = checksum_iban(country.code + "00" + bank + account)
    return country.code + checksum + bank + account

def iban_okay(iban):
    """Check the checksum of an IBAN."""
    return checksum_iban(iban) == "97"

class IBANError(Exception):
    def __init__(self, errmsg):
        Exception.__init__(self, errmsg)

def create_iban(code, bank, account):
    """Check the input, calculate the checksum and assemble the IBAN.

    Return the calculated IBAN.
    Raise an IBANError exception if the input is not correct.
    """
    err = None
    country = country_data(code)
    if not country:
        err = "Unknown Country Code: %s" % code
    elif len(bank) != country.bank_lng():
        err = "Bank/Branch Code length %s is not correct for %s (%s)" % \
              (len(bank), country.name, country.bank_lng())
    elif invalid_bank(country, bank):
        err = "Bank/Branch Code %s is not correct for %s" % \
              (bank, country.name)
    elif len(account) > country.acc_lng():
        err = "Account Number length %s is not correct for %s (%s)" % \
              (len(account), country.name, country.acc_lng())
    elif invalid_account(country, account):
        err = "Account Number %s is not correct for %s" % \
              (account, country.name)
    if err:
        raise IBANError(err)
    return calc_iban(country, bank, account)

def check_iban(iban):
    """Check the syntax and the checksum of an IBAN.

    Return the parts of the IBAN: Country Code, Checksum, Bank/Branch Code and
    Account number.
    Raise an IBANError exception if the input is not correct.
    """
    err = None
    code     = iban[:2]
    checksum = iban[2:4]
    bban     = iban[4:]
    country = country_data(code)
    if not country:
        err = "Unknown Country Code: %s" % code
    elif len(iban) != country.total_lng():
        err = "IBAN length %s is not correct for %s (%s)" % \
              (len(iban), country.name, country.total_lng())
    else:
        bank_lng = country.bank_lng()
        bank     = bban[:bank_lng]
        account  = bban[bank_lng:]
        if invalid_bank(country, bank):
            err = "Bank/Branch Code %s is not correct for %s" % \
                  (bank, country.name)
        elif invalid_account(country, account):
            err = "Account Number %s is not correct for %s" % \
                  (account, country.name)
        elif not iban_okay(iban):
            err = "Incorrect IBAN: %s >> %s %s %s %s" % \
                  (iban, code, checksum, bank, account)
    if err:
        raise IBANError(err)
    return code, checksum, bank, account



