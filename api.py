#!/usr/bin/env python
# coding: utf-8
# yc@2014/08/10

import urllib, urllib2, hashlib, hmac, time, json


class API(object):
  '''
  '''
  public_methods = ['ticker', 'trades', 'depth', 'test']
  private_methods = ['info', 'orders', 'transactions', 'trade', 'cancel']
  timeout = 30
  api_base = 'https://bitbays.com/api'

  def __init__(self, key, secret, wait_for_nonce=False):
    self._key = key
    self._secret = secret
    self._wait_for_nonce = wait_for_nonce
    self._methods = self.public_methods + self.private_methods

  def _nonce(self):
    if self._wait_for_nonce:
      time.sleep(1)
    return int(time.time())

  def _sign(self, params):
    return hmac.new(self._secret, params, digestmod=hashlib.sha512).hexdigest()

  def _api(self, uri, params, private=False):
    if private:
      params['nonce'] = self._nonce()
    params = urllib.urlencode(params)
    if private:
      req = urllib2.Request(self.api_base + uri, params, {
        'Key': self._key,
        'Sign': self._sign(params),
      })
    else:
      req = urllib2.Request('%s%s?%s' % (self.api_base, uri, params))
    return json.load(urllib2.urlopen(req, timeout=self.timeout))

  def __getattr__(self, name):
    if name in self._methods:
      return lambda **p: self._api('/%s/' % name, p, private=bool(name in self.private_methods))
    raise AttributeError(name)


if __name__ == '__main__':
  api = API(
    '2B-58D181C3-13E6053D-939BB278',
    '3F24705B90D351C490B7D21EF1B99C1504EF6227'
  )
  print api.test()
  print api.info()
