from __future__ import print_function
################################################################################
# RelMon: a tool for automatic Release Comparison                              
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/RelMon
#
# This is a code manipulation of a component of the DQMCompare tool of 
# Marco Rovere and Luca Malgeri.
#
#
#                                                                              
# Danilo Piparo CERN - danilo.piparo@cern.ch                                   
# update : Arnaud ChironLLR - arnaud.chiron@llr.in2p3.fr                       
#                                                                              
################################################################################

from os import getenv
from os.path import exists
#from httplib import HTTPSConnection

try:
  from httplib import HTTPSConnection
except ImportError:
  from http.client import HTTPSConnection

#from urllib2  import AbstractHTTPHandler
try:
    import urllib2
    from urllib2  import AbstractHTTPHandler
except ImportError:
    import urllib
    from urllib.request  import AbstractHTTPHandler

#-------------------------------------------------------------------------------  

class X509CertAuth(HTTPSConnection):
  '''Class to authenticate via Grid Certificate'''
  def __init__(self, host, *args, **kwargs):
    key_file = None
    cert_file = None

    x509_path = getenv("X509_USER_PROXY", None)
    if x509_path and exists(x509_path):
      key_file = cert_file = x509_path

    if not key_file:
      x509_path = getenv("X509_USER_KEY", None)
      if x509_path and exists(x509_path):
        key_file = x509_path

    if not cert_file:
      x509_path = getenv("X509_USER_CERT", None)
      if x509_path and exists(x509_path):
        cert_file = x509_path

    if not key_file:
      x509_path = getenv("HOME") + "/.globus/userkey.pem"
      if exists(x509_path):
        key_file = x509_path

    if not cert_file:
      x509_path = getenv("HOME") + "/.globus/usercert.pem"
      if exists(x509_path):
        cert_file = x509_path

    if not key_file or not exists(key_file):
      print("No certificate private key file found", file=stderr)
      exit(1)

    if not cert_file or not exists(cert_file):
      print("No certificate public key file found", file=stderr)
      exit(1)

    #print "Using SSL private key", key_file
    #print "Using SSL public key", cert_file
    
    HTTPSConnection.__init__(self, 
                              host,
                              key_file = key_file,
                              cert_file = cert_file,
                              **kwargs)

#-----------------------------------------------------------------------------

class X509CertOpen(AbstractHTTPHandler):
  def default_open(self, req):
    return self.do_open(X509CertAuth, req)