from OpenSSL import crypto

TYPE_RSA = crypto.TYPE_RSA
TYPE_DSA = crypto.TYPE_DSA

def createKeyPair(type, bits):
   """
      Create a public/private key pair.
      Arguments: type - Key type, must be one of TYPE_RSA and TYPE_DSA
           bits - Number of bits to use in the key
      Returns:   The public/private key pair in a PKey object
   """
   pkey = crypto.PKey()
   pkey.generate_key(type, bits)
   return pkey

def createCertRequest(pkey, digest="md5", **name):
   """
      Create a certificate request.
      Arguments: pkey   - The key to associate with the request
           digest - Digestion method to use for signing, default is md5
           **name - The name of the subject of the request, possible
                    arguments are:
                      C     - Country name
                      ST    - State or province name
                      L     - Locality name
                      O     - Organization name
                      OU    - Organizational unit name
                      CN    - Common name
                      emailAddress - E-mail address
      Returns:   The certificate request in an X509Req object
   """
   req = crypto.X509Req()
   subj = req.get_subject()

   for (key, value) in name.items():
       setattr(subj, key, value)

   req.set_pubkey(pkey)
   req.sign(pkey, digest)
   return req

def createCertificate(req, issuerCertKey, serial, validityPeriod,
                  digest="sha256"):

   """
       Generate a certificate given a certificate request.
       Arguments: req        - Certificate request to use
           issuerCert - The certificate of the issuer
           issuerKey  - The private key of the issuer
           serial     - Serial number for the certificate
           notBefore  - Timestamp (relative to now) when the certificate
                        starts being valid
           notAfter   - Timestamp (relative to now) when the certificate
                        stops being valid
           digest     - Digest method to use for signing, default is sha256
     Returns:   The signed certificate in an X509 object
  """
  issuerCert, issuerKey = issuerCertKey
  notBefore, notAfter = validityPeriod
  cert = crypto.X509()
  cert.set_serial_number(serial)
  cert.gmtime_adj_notBefore(notBefore)
  cert.gmtime_adj_notAfter(notAfter)
  cert.set_issuer(issuerCert.get_subject())
  cert.set_subject(req.get_subject())
  cert.set_pubkey(req.get_pubkey())
  cert.sign(issuerKey, digest)
  return cert


if __name__ == "__main__":
    cakey = createKeyPair(TYPE_RSA, 1024)
    careq = createCertRequest(cakey, CN='Certificate Authority')
    cacert = createCertificate(careq, (careq, cakey),0, (0, 60 * 60 * 24 * 365))  # one year
    open('clientkey.pem', 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, cakey,passphrase='12345678'))
    open('clientcert.pem', 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cacert))