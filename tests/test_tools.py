import unittest

import requests
import responses

from tools import scrape, utils


class TestScrapeMethods(unittest.TestCase):
    @responses.activate
    def test_get_page_text_successful_response(self):
        """
        Positive test case, method should return page text
        """
        responses.add(
            responses.GET, "http://example.com", body="Super Method", status=200
        )
        res = scrape._get_page_text("http://example.com")
        self.assertEqual(res, "Super Method")

    @responses.activate
    def test_get_page_text_unsuccessful_response(self):
        """
        Negative test case, inner method should raise exception and text should not be returned
        """
        responses.add(responses.GET, "http://example.com", body="Error", status=400)
        with self.assertRaises(requests.exceptions.HTTPError):
            res = scrape._get_page_text("http://example.com")
            self.assertNotEqual(res, "Error")

    @responses.activate
    def test_get_page_bytes_successful_response(self):
        """
        Positive test case, method should return bytes data
        """
        responses.add(
            responses.GET, "http://example.com", body="Super Method", status=200
        )
        res = scrape._get_page_bytes("http://example.com")
        self.assertEqual(res.decode(), "Super Method")

    @responses.activate
    def test_get_page_bytes_unsuccessful_response(self):
        """
        Negative test case, inner method should raise exception and bytes should not be returned
        """
        responses.add(responses.GET, "http://example.com", body="Error", status=400)
        with self.assertRaises(requests.exceptions.HTTPError):
            res = scrape._get_page_bytes("http://example.com")
            self.assertNotEqual(res.decode(), "Error")


class TestUtilsMethods(unittest.TestCase):
    def test_fix_url_with_http(self):
        """
        Test case where input url starts with http,
        returned result should be equal to input url
        """
        test_url = "https://example.com"
        res = utils.fix_url_http(test_url)
        self.assertEqual(res, test_url)\

    
    def test_fix_url_with_www(self):
        """
        Test case where input url starts with www.,
        returned result should start with `http://`
        """
        test_url = "www.example.com"
        res = utils.fix_url_http(test_url)
        self.assertEqual(res, 'http://example.com')

    def test_fix_url_no_http(self):
        """
        Test case where input has no http at the beggining,
        returned result should have added `http://`
        """
        test_url = "example.com"
        res = utils.fix_url_http(test_url)
        self.assertEqual(res, "http://" + test_url)

    def test_get_resource_full_url_complete(self):
        """
        Test case where resource url contains full path,
        should return resource url in process
        """
        base_url = "https://example.com"
        resource_url = "https://example.com/static/img/image.png"
        res = utils.get_resource_full_url(base_url, resource_url)
        self.assertEqual(res, resource_url)

    def test_get_resource_full_url_slash_ending(self):
        """
        Test case where resource url is missing base url
        and base url is ending with slash
        """
        base_url = "https://example.com/"
        resource_url = "/static/img/image.png"
        res = utils.get_resource_full_url(base_url, resource_url)
        self.assertEqual(res, "https://example.com/static/img/image.png")

    def test_get_resource_full_url_no_slash_ending(self):
        """
        Test case where resource url is missing base url
        and base url is not ending with slash
        """
        base_url = "https://example.com"
        resource_url = "/static/img/image.png"
        res = utils.get_resource_full_url(base_url, resource_url)
        self.assertEqual(res, base_url + resource_url)

    def test_get_resource_full_url_both_no_slashes(self):
        """
        Test case where resource url is missing base url
        and both urls are missing slashes
        """
        base_url = "https://example.com"
        resource_url = "static/img/image.png"
        res = utils.get_resource_full_url(base_url, resource_url)
        self.assertEqual(res, base_url + "/" + resource_url)
