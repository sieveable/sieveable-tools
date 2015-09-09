#!/usr/bin/env python2
import json
import os
from types import *
import unittest

from playlistingscraper.playlistingscraper import PlayListingScraper


class PlayListingScrapwerTest(unittest.TestCase):
    def setUp(self):
        listing_parser = PlayListingScraper()
        self.package_name = "com.google.android.youtube"
        self.version_code = "5021"
        out_dir = os.getcwd()
        self.json_file = os.path.join(out_dir,
                                      self.package_name + '-' +
                                      self.version_code + '.listing.json')
        listing_parser.scrape_remote_page(self.package_name,
                                          self.version_code, out_dir)
        with open(self.json_file) as data_file:
            self.app = json.load(data_file)

    def tearDown(self):
        os.remove(self.json_file)

    def test_file_exists(self):
        self.assertTrue(os.path.exists(self.json_file))

    def test_package_name(self):
        self.assertEqual(self.app["n"], self.package_name,
                         "Invalid package name")

    def test_title(self):
        self.assertGreater(len(self.app["t"]), 0, "title is empty")
        # assert type(self.app["t"]) is unicode, "t is not a string: %r" \
        #                                         % self.app["t"]
        self.assertTrue("youtube" in self.app["t"].lower(),
                        "Unknown app title")

    def test_description(self):
        self.assertGreater(len(self.app["desc"]), 0, "description is empty")

    def test_category(self):
        self.assertGreater(len(self.app["cat"]), 0, "category is empty")

    def test_price(self):
        self.assertGreater(len(self.app["pri"]), 0, "price is empty")
        self.assertEqual(self.app["pri"], "Free", "app is not Free")

    def test_date_published(self):
        self.assertGreater(len(self.app["dtp"]), 0, "date published is empty")

    def test_os_version(self):
        self.assertGreater(len(self.app["os"]), 0, "os version  is empty")

    def test_rating_count(self):
        assert type(
            self.app["rct"]) is IntType, "rating count is not an integer: %r" \
                                         % self.app["rct"]
        self.assertGreater(self.app["rct"], 0,
                           "rating count is not greater than zero")

    def test_rating(self):
        print(self.app["rate"])
        assert type(self.app[
                        "rate"]) is FloatType, "app rating is not a float number: %r" \
                                               % self.app["rate"]
        self.assertGreater(self.app["rate"], 0,
                           "app rating is not greater than zero")

    def test_content_rating(self):
        self.assertGreater(len(self.app["crat"]), 0, "content rating is empty")

    def test_creator(self):
        self.assertGreater(len(self.app["crt"]), 0, "creator is empty")

    def test_creator_address(self):
        self.assertGreater(len(self.app["cadd"]), 0, "creator address is empty")

    def test_creator_url(self):
        self.assertGreater(len(self.app["curl"]), 0, "creator url is empty")

    def test_install_size(self):
        self.assertGreater(len(self.app["sz"]), 0, "install size is empty")

    def test_download_count(self):
        assert type(
            self.app["dct"]) is IntType, "download count is not an integer: %r" \
                                         % self.app["dct"]
        self.assertGreater(self.app["dct"], 0,
                           "download count is not greater than zero")

    def test_download_count_text(self):
        self.assertGreater(len(self.app["dtxt"]), 0,
                           "download count text is empty")

    def test_privacy_url(self):
        self.assertGreater(len(self.app["purl"]), 0, "privacy url is empty")
        self.assertTrue(self.app["purl"].startswith("http"))

    def test_whats_new(self):
        self.assertGreater(len(self.app["new"]), 0, "whats new field is empty")


if __name__ == '__main__':
    unittest.main()
