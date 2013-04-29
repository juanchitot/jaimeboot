#!/bin/env/python
# -*- coding: UTF-8 -*-

try:
    from json import loads as json_decode
except ImportError:
    try:
        from json import read as json_decode
    except ImportError:
        from simplejson import loads as json_decode
import urllib2
from urllib import urlencode
from hashlib import sha1
from time import time, sleep
from socket import gethostbyname

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


# API version
API_VERSION = 'DBC/Python v3.0'
SOFTWARE_VENDOR_ID = 0

# API server's absolute url
API_SERVER_URL = 'http://www.deathbycaptcha.com/api'

# Preferred API server's response content type, do not change
API_RESPONSE_CONTENT_TYPE = 'application/json'

# Maximum CAPTCHA image filesize, currently 128K
MAX_CAPTCHA_FILESIZE = 128 * 1024

POLLS_COUNT = 3
POLLS_PERIOD = 15
POLLS_INTERVAL = 5

# Default CAPTCHA timeout
DEFAULT_TIMEOUT = 60


class Client(object):
    """DeathByCaptha API Client"""

    def __init__(self, username, password):
        a = API_SERVER_URL.split('/', 3)
        a[2] = gethostbyname(a[2])
        self.server_url = '/'.join(a)
        self.userpwd = (username, sha1(password).hexdigest())
        self.connection = None
        self.is_verbose = False
        self.response = {}

    def _get_credentials(self):
        return {'username': self.userpwd[0],
                'password': self.userpwd[1],
                'is_hashed': 1}

    def _call(self, method, args=None, headers=None):
        self.response = {}
        if not headers:
            headers = {}
        headers['Accept'] = API_RESPONSE_CONTENT_TYPE
        headers['User-Agent'] = API_VERSION
        if isinstance(args, (dict, list, tuple)):
            if self.is_verbose:
                print '%d SEND: %s' % (time(), args)
            args = urlencode(args)
        try:
            self.response = json_decode(urllib2.urlopen(urllib2.Request(
                '%s/%s' % (self.server_url, method.strip('/')),
                args,
                headers
            )).read())
        except urllib2.HTTPError:
            pass
        except Exception:
            pass
        else:
            if self.is_verbose:
                print '%d RECV: %s' % (time(), self.response)
        return self.response

    def get_user(self):
        """Return the user's details (only ID and balance for now)."""
        return (self._call('user', self._get_credentials()) and
                {'user': int(self.response.get('user', 0)),
                 'balance': float(self.response.get('balance', 0.0))}) or {}

    def get_balance(self):
        """Return the user's balance (in US cents)."""
        return self.get_user().get('balance', None)

    def upload(self, captchafile):
        """Upload a CAPTCHA.

        Accepts CAPTCHA file names and file objects (StringIO is OK too).
        Returns int CAPTCHA ID on success

        """
        if not isinstance(captchafile, file):
            captchafile = open(captchafile, 'r')
            close_when_done = True
        else:
            close_when_done = False
        args = self._get_credentials()
        args.update((('captchafile', captchafile),
                     ('swid', SOFTWARE_VENDOR_ID)))
        body_generator, headers = multipart_encode(args)
        body = ''.join(body_generator)
        if close_when_done:
            captchafile.close()
        return self._call('captcha', body, headers).get('captcha', None) or None

    def get_text(self, id):
        """Check an uploaded CAPTCHA status and return its text, if solved."""
        return self._call('captcha/%d' % id).get('text') or None

    def report(self, id):
        """Report an incorrectly solved CAPTCHA to the system.

        Returns True if successfully reported, False otherwise.

        """
        resp = self._call('captcha/%d/report' % id, self._get_credentials())
        return (resp['captcha'] and not resp.get('is_correct', False)) or False

    def remove(self, id):
        """Remove an unsolved CAPTCHA.

        Returns True if successfully removed, False otherwise.

        """
        return not self._call('captcha/%d/remove' % id,
                              self._get_credentials()).get('captcha', 0);

    def decode(self, captchafile, timeout=DEFAULT_TIMEOUT):
        """Upload and try to solve a CAPTCHA with desired timeout.

        Accepts CAPTCHA file names and file objects (StringIO is OK too), and
        an optional timeout in seconds (defaults to 60).  Returns (ID, text)
        tuple on success.

        """
        id = self.upload(captchafile)
        if id:
            text = None
            attempt = 0
            deadline = time() + max(2 * POLLS_PERIOD, int(timeout))
            while deadline > time() and not text:
                attempt += 1
                sleep((1 == (attempt % POLLS_COUNT) and POLLS_PERIOD) or POLLS_INTERVAL)
                text = self.get_text(id)
            if text:
                return (id, text)
            self.remove(id)


register_openers()


if '__main__' == __name__:
    from sys import stderr, argv
    client = Client(argv[1], argv[2])
    client.is_verbose = True
    print 'Your balance is %s cents' % client.get_balance()
    try:
        # Put your CAPTCHA image file/file name and desired timeout here here
        id, text = client.decode(argv[3], 120)
    except Exception, e:
        stderr.write('%s\n' % str(e))
        id, text = 0, None
    if id:
        if text:
            # Report as incorrectly solved if needed
            print 'CAPTCHA #%d solved: %s' % (id, text)
            try:
                client.report(id)
            except Exception, e:
                stderr.write('%s\n' % str(e))
        else:
            print 'CAPTCHA #%d is not solved' % id
