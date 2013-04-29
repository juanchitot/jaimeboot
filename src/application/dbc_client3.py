#!/bin/env/python
# -*- coding: UTF-8 -*-

try:
    from json import loads as json_decode, dumps as json_encode
except ImportError:
    try:
        from json import read as json_decode, write as json_encode
    except ImportError:
        from simplejson import loads as json_decode, dumps as json_encode
from hashlib import sha1
from time import time, sleep
from random import choice
from select import select
from base64 import b64encode
import socket


# API version
API_VERSION = 'DBC/Python v3.0'
SOFTWARE_VENDOR_ID = 0

# API server's host & ports range
API_SERVER_HOST = socket.gethostbyname('deathbycaptcha.com')
API_SERVER_PORTS = range(8123, 8131)

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
        '''Instantiates a DBC API client with supplied credentials'''
        self.username = username
        self.password = sha1(password).hexdigest()
        self.is_verbose = False

    def _connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((API_SERVER_HOST, choice(API_SERVER_PORTS)))
        except Exception, e:
            raise Exception('Failed connecting to the API server (%s)' % str(e))
        sock.settimeout(0)
        return sock

    def _call(self, cmd, timeout=DEFAULT_TIMEOUT, **kw):
        kw['cmd'] = cmd
        kw['version'] = API_VERSION
        kw['swid'] = SOFTWARE_VENDOR_ID
        kw['username'] = self.username
        kw['password'] = self.password
        kw['is_hashed'] = True
        buff = json_encode(kw)
        if self.is_verbose:
            print '%d SEND: %s' % (time(), buff)
        sock = self._connect()
        sock.sendall(buff)
        deadline = time() + timeout
        response = None
        buff = ''
        while deadline > time() and not response:
            rd, _, ex = select([sock], [], [], timeout)
            if not rd:
                continue
            elif ex:
                break
            buff += rd[0].recv(4096)
            try:
                response = json_decode(buff)
            except Exception:
                pass
        sock.close()
        if self.is_verbose:
            print '%d RECV: %s' % (time(), response)
        if response:
            if 0x01 < response['status'] and 0x10 > response['status']:
                raise Exception('Login failed, check your credentials and/or balance')
            elif 0x10 <= response['status'] and 0x20 > response['status']:
                raise Exception('Failed uploading/fetching a CAPTCHA, check its ID')
            elif 0x00 != response['status']:
                raise Exception('Service error occured')
            return response
        raise Exception('Connection lost or timeout out')

    def get_user(self):
        """Return the user's details (only ID and balance for now)."""
        return self._call('get_user') or {}

    def get_balance(self):
        """Return the user's balance (in US cents)."""
        return self.get_user().get('balance', None)

    def upload(self, captchafile):
        """Upload a CAPTCHA.

        Accepts CAPTCHA file names and file objects (StringIO is OK too).
        Returns int CAPTCHA ID on success

        """
        if not isinstance(captchafile, file):
            captchafile = open(captchafile, 'rb')
            close_when_done = True
        else:
            close_when_done = False
        try:
            return self._call('upload',
                              captcha=b64encode(captchafile.read()),
                              swid=SOFTWARE_VENDOR_ID).get('captcha', 0)
        except Exception, e:
            raise e
        finally:
            if close_when_done:
                captchafile.close()

    def get_text(self, captcha_id):
        """Check an uploaded CAPTCHA status and return its text, if solved."""
        return self._call('get_text',
                          captcha=captcha_id).get('text', '') or None

    def report(self, captcha_id):
        """Report an incorrectly solved CAPTCHA to the system.

        Returns True if successfully reported, False otherwise.

        """
        resp = self._call('report', captcha=captcha_id)
        return (resp['captcha'] and not resp.get('is_correct', False)) or False

    def remove(self, captcha_id):
        """Remove an unsolved CAPTCHA.

        Returns True if successfully removed, False otherwise.

        """
        return not self._call('remove', captcha=captcha_id).get('captcha', 0)

    def decode(self, captchafile, timeout=DEFAULT_TIMEOUT):
        """Upload and try to solve a CAPTCHA with desired timeout.

        Accepts CAPTCHA file names and file objects (StringIO is OK too), and
        an optional timeout in seconds (defaults to 60).  Returns (ID, text)
        tuple on success.

        """
        id = self.upload(captchafile) or 0
        if id:
            text = ''
            attempt = 0
            deadline = time() + max(2 * POLLS_PERIOD, int(timeout))
            while deadline > time() and not text:
                attempt += 1
                sleep((1 == (attempt % POLLS_COUNT) and POLLS_PERIOD) or POLLS_INTERVAL)
                text = self.get_text(id)
            if text:
                return (id, text)
            self.remove(id)


if '__main__' == __name__:
    from sys import stderr, argv
    client = Client(argv[1], argv[2])
    client.is_verbose = False
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
            #try:
            #    client.report(id)
            #except Exception, e:
            #    stderr.write('%s\n' % str(e))
        else:
            print 'CAPTCHA #%d is not solved' % id
