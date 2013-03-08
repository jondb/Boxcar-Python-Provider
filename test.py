#!/bin/python
# -*- coding:utf-8 -*-
"""
unit test for boxcar
"""

import unittest
from minimock import mock, restore, Mock, TraceTracker, assert_same_trace
#import google.appengine.api
import boxcar


class Response(object):
    """ responce of urlfetch """
    def __init__(self, code, *args, **kw):
        """ make dummy responce """
        self.status_code = code
        self.url = ''
        self.payload = ''


class Testboxcar(unittest.TestCase):
    """ test boxcar """
    def setUp(self):
        # create new instance
        self.boxcar = boxcar.BoxcarApi('xxxxxxxxxxxxxxxxxxxx',
                           'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                           'xxxxxxxxx@xxxxx.xxx')

    def tearDown(self):
        restore()


class TestiboxcarNormal(Testboxcar):
    """ normal cases class """
    def test_invite(self):
        # mock urlfetch
        trace = TraceTracker()
        response = Response(200) 
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # invite
        self.boxcar.invite('zzzzzzzz@zzzz.zzzz')
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications/subscribe',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='email=zzzzzzzz%40zzzz.zzzz')\n")

    def test_broadcast(self):
        # mock urlfetch
        trace = TraceTracker()
        response = Response(200) 
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # send a broadcast                   
        self.boxcar.broadcast('test_normal', 'broadcast message')
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications/broadcast',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='"
                         "notification%5Bfrom_screen_name%5D=test_normal&"
                         "notification%5Bicon_url%5D=xxxxxxxxx%40xxxxx.xxx&"
                         "notification%5Bmessage%5D=broadcast+message&"
                         "secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&"
                         "token=xxxxxxxxxxxxxxxxxxxx"
                         "')\n")

    def test_notify(self):
        # mock urlfetch
        trace = TraceTracker()
        response = Response(200) 
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # send a notification
        self.boxcar.notify('yyyyyyyy@yyyyy.yyy',
                           'test_normal',
                           'notification message',
                            message_id=200)
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='"
                         "email=yyyyyyyy%40yyyyy.yyy&"
                         "notification%5Bfrom_remote_service_id%5D=200&"
                         "notification%5Bfrom_screen_name%5D=test_normal&"
                         "notification%5Bicon_url%5D=xxxxxxxxx%40xxxxx.xxx&"
                         "notification%5Bmessage%5D=notification+message&"
                         "secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&"
                         "token=xxxxxxxxxxxxxxxxxxxx"
                         "')\n")


class TestiboxcarError(Testboxcar):
    """ error cases class """
    def test_invite(self):
        """ error cases class """
        # mock urlfetch
        response = Response(404) 
        trace = TraceTracker()
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # user not found(404)
        self.assertRaises(boxcar.BoxcarException, 
                          self.boxcar.invite, 'yyyyyyy@zzzz.zzzz')
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications/subscribe',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='email=yyyyyyy%40zzzz.zzzz')\n")

    def test_incorrect_parameter(self):
        # mock urlfetch
        response = Response(400) 
        trace = TraceTracker()
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # incorrect parameter(400)
        self.assertRaises(boxcar.BoxcarException, 
                          self.boxcar.notify, 'yyyyyyyy@yyyyy.yyy',
                                              'test_error',
                                              'notification error',
                                              message_id=400)
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='"
                         "email=yyyyyyyy%40yyyyy.yyy&"
                         "notification%5Bfrom_remote_service_id%5D=400&"
                         "notification%5Bfrom_screen_name%5D=test_error&"
                         "notification%5Bicon_url%5D=xxxxxxxxx%40xxxxx.xxx&"
                         "notification%5Bmessage%5D=notification+error&"
                         "secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&"
                         "token=xxxxxxxxxxxxxxxxxxxx"
                         "')\n")

    def test_request_failure(self):
        # mock urlfetch
        response = Response(401) 
        trace = TraceTracker()
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # request failure(401)
        self.assertRaises(boxcar.BoxcarException, 
                          self.boxcar.notify, 'yyyyyyyy@yyyyy.yyy',
                                              'test_error',
                                              'notification error',
                                              message_id=401)
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='"
                         "email=yyyyyyyy%40yyyyy.yyy&"
                         "notification%5Bfrom_remote_service_id%5D=401&"
                         "notification%5Bfrom_screen_name%5D=test_error&"
                         "notification%5Bicon_url%5D=xxxxxxxxx%40xxxxx.xxx&"
                         "notification%5Bmessage%5D=notification+error&"
                         "secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&"
                         "token=xxxxxxxxxxxxxxxxxxxx"
                         "')\n")

    def test_request_failure_403(self):
        # mock urlfetch
        response = Response(403) 
        trace = TraceTracker()
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # request failure(403)
        self.assertRaises(boxcar.BoxcarException, 
                          self.boxcar.notify, 'yyyyyyyy@yyyyy.yyy',
                                              'test_error',
                                              'notification error',
                                              message_id=403)
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='"
                         "email=yyyyyyyy%40yyyyy.yyy&"
                         "notification%5Bfrom_remote_service_id%5D=403&"
                         "notification%5Bfrom_screen_name%5D=test_error&"
                         "notification%5Bicon_url%5D=xxxxxxxxx%40xxxxx.xxx&"
                         "notification%5Bmessage%5D=notification+error&"
                         "secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&"
                         "token=xxxxxxxxxxxxxxxxxxxx"
                         "')\n")

    def test_unknown_error(self):
        # mock urlfetch
        response = Response(500) 
        trace = TraceTracker()
        boxcar.fetch = Mock('fetch',
                                returns=response, 
                                tracker=trace)
        # unknown error(500)
        self.assertRaises(boxcar.BoxcarException, 
                          self.boxcar.notify, 'yyyyyyyy@yyyyy.yyy',
                                              'test_error',
                                              'unknown error',
                                              message_id=500)
        assert_same_trace(trace,
            "Called fetch(\n"
            "    'http://boxcar.io/devices/providers/xxxxxxxxxxxxxxxxxxxx/notifications',\n"
            "    headers={'User-Agent': 'Boxcar_Client'},\n"

            "    payload='"
                         "email=yyyyyyyy%40yyyyy.yyy&"
                         "notification%5Bfrom_remote_service_id%5D=500&"
                         "notification%5Bfrom_screen_name%5D=test_error&"
                         "notification%5Bicon_url%5D=xxxxxxxxx%40xxxxx.xxx&"
                         "notification%5Bmessage%5D=unknown+error&"
                         "secret=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&"
                         "token=xxxxxxxxxxxxxxxxxxxx"
                         "')\n")


if __name__ == '__main__':
    unittest.main()
