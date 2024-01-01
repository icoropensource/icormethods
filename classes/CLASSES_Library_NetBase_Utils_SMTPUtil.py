# -*- coding: windows-1250 -*-
# saved: 2020/11/02 21:15:56

import smtplib
import base64

def encode_base64(s,eol=None):
   return "".join(base64.encodestring(s).split("\n"))

class AuthSMTP(smtplib.SMTP):
   def login(self, user, password):
      def encode_cram_md5(challenge, user, password):
         import hmac
         challenge=base64.decodestring(challenge)
         response=user+" "+hmac.HMAC(password, challenge).hexdigest()
         return encode_base64(response, eol="")
      def encode_plain(user, password):
         return encode_base64("%s\0%s\0%s" % (user, user, password), eol="")
      AUTH_PLAIN = "PLAIN"
      AUTH_CRAM_MD5 = "CRAM-MD5"
      AUTH_LOGIN = "LOGIN"
      if self.helo_resp is None and self.ehlo_resp is None:
         if not (200 <= self.ehlo()[0] <= 299):
             (code, resp) = self.helo()
             if not (200 <= code <= 299):
                raise smtplib.SMTPHeloError(code, resp)
      if not self.has_extn("auth"):
         raise smtplib.SMTPException("Rozszerzenie SMTP AUTH nie jest wspierane przez serwer.")
      authlist = self.esmtp_features["auth"].split()
      preferred_auths = [AUTH_PLAIN, AUTH_LOGIN, AUTH_CRAM_MD5]
      authmethod = None
      for method in preferred_auths:
         if method in authlist:
            authmethod = method
            break
      if authmethod == AUTH_CRAM_MD5:
         (code, resp) = self.docmd("AUTH", AUTH_CRAM_MD5)
         if code == 503:
            return (code, resp)
         (code, resp) = self.docmd(encode_cram_md5(resp, user, password))
      elif authmethod == AUTH_PLAIN:
         (code, resp) = self.docmd("AUTH",
             AUTH_PLAIN + " " + encode_plain(user, password))
      elif authmethod == AUTH_LOGIN:
         (code, resp) = self.docmd("AUTH",
            "%s %s" % (AUTH_LOGIN, encode_base64(user, eol="")))
         if code != 334:
            raise smtplib.SMTPAuthenticationError(code, resp)
         (code, resp) = self.docmd(encode_base64(password, eol=""))
      elif authmethod == None:
         raise smtplib.SMTPException("Nie znaleziono dostepnej metody autentykacji.")
      if code not in [235, 503]:
         raise smtplib.SMTPAuthenticationError(code, resp)
      return (code, resp)



