import unittest

import requests
import responses

from tools import scrape


class TestscrapeMethods(unittest.TestCase):

    @responses.activate
    def test_get_page_text_successful_response(self):
        responses.add(responses.GET, 'http://example.com',
                  body="Super Method", status=200)
        res = scrape._get_page_text('http://example.com')
        self.assertEqual(res, "Super Method")

    
    @responses.activate
    def test_get_page_text_unsuccessful_response(self):
        responses.add(responses.GET, 'http://example.com',
                  body="Error", status=400)
        with self.assertRaises(requests.exceptions.HTTPError):
            res = scrape._get_page_text('http://example.com')
            self.assertNotEqual(res, "Error")

    @responses.activate
    def test_get_page_bytes_successful_response(self):
        responses.add(responses.GET, 'http://example.com',
                  body="Super Method", status=200)
        res = scrape._get_page_bytes('http://example.com')
        self.assertEqual(res.decode(), "Super Method")

    
    @responses.activate
    def test_get_page_bytes_unsuccessful_response(self):
        responses.add(responses.GET, 'http://example.com',
                  body="Error", status=400)
        with self.assertRaises(requests.exceptions.HTTPError):
            res = scrape._get_page_bytes('http://example.com')
            self.assertNotEqual(res.decode(), "Error")