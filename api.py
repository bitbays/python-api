#!/usr/bin/env python
# coding: utf-8
# yc@2014/08/10

import urllib, urllib2, hashlib, hmac, time, json


class API(object):
  '''
  '''
  public_methods = ['ticker', 'trades', 'depth', 'test']
  private_methods = ['info', 'orders', 'transactions', 'trade', 'cancel', 'order']
  timeout = 30
  api_base = 'https://bitbays.com/api/'

  def __init__(self, key, secret, version='v1'):
    self._key = key
    self._secret = secret
    self._methods = self.public_methods + self.private_methods
    self._api_base = self.api_base + version
    self._counter = int(time.time() * 1000)

  def _nonce(self):
    self._counter += 1
    return self._counter

  def _sign(self, params):
    return hmac.new(self._secret, params, digestmod=hashlib.sha512).hexdigest()

  def _api(self, uri, params, private=False):
    if private:
      params['nonce'] = self._nonce()
    params = urllib.urlencode(params)
    if private:
      req = urllib2.Request(self._api_base + uri, params, {
        'Key': self._key,
        'Sign': self._sign(params),
      })
    else:
      req = urllib2.Request('%s%s?%s' % (self._api_base, uri, params))
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
  # public
  print api.test()
  # private
  print api.info()
  # with params
  print api.orders(catalog=0, since_id=1, count=20, order='DESC')
