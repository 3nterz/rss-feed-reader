"""Tests for the app module
"""
import unittest
import os
from argparse import Namespace
from typing import Any, TextIO
from rssfeedreader import RSSFeedReader
from model import RSSFeedChannel, RSSFeedItem
from cli import CLIParser
from app import get_default_feedreader
from app import main

class TestRSSFeedDataClasses(unittest.TestCase):
    """Tests for data model of RSS feed reader
    """
    def test_build_rss_feed_item(self) -> None:
        """Verify construction method
        """
        actual_rss_feed_ttem: RSSFeedItem = RSSFeedItem(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        expected_rss_feed_item: RSSFeedItem = RSSFeedItem('','','')
        expected_rss_feed_item.title = 'Some title'
        expected_rss_feed_item.description = 'Some description here.'
        expected_rss_feed_item.link = 'http://somelink.lnk'
        self.assertEqual(actual_rss_feed_ttem, expected_rss_feed_item)

    def test_build_rss_feed_channel(self) -> None:
        """Verify construction method
        """
        items: list[RSSFeedItem] = list[RSSFeedItem]()
        items.append(RSSFeedItem('a','b','c'))
        actual_rss_feed_channel: RSSFeedChannel = RSSFeedChannel(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk',
            items=items
        )
        expected_rss_feed_channel: RSSFeedChannel = RSSFeedChannel('','','',list[RSSFeedItem]())
        expected_rss_feed_channel.title = 'Some title'
        expected_rss_feed_channel.description = 'Some description here.'
        expected_rss_feed_channel.link = 'http://somelink.lnk'
        expected_rss_feed_channel.items = items
        self.assertEqual(actual_rss_feed_channel, expected_rss_feed_channel)

class TestRSSFeedCLI(unittest.TestCase):
    """Tests for command line interface of RSS feed reader
    """
    def test_build_cli_parser(self) -> None:
        """Verify factory method for ArgumentParser
        """
        self.assertIsNotNone(CLIParser._build_argument_parser()) # pylint: disable=protected-access

    def test_invalid_url(self) -> None:
        """Verify invalid input URL raises ValueError
        """
        self.assertRaises(ValueError, CLIParser._uri, 'invalidurl') # pylint: disable=protected-access

    def test_get_parsed_namespace_from_args(self) -> None:
        """Verify conversion from command line arguments to Namespace instance
        """
        cli_parser: CLIParser = CLIParser()
        actual_instance_object: Namespace = cli_parser._get_parsed_namespace_from_args( # pylint: disable=protected-access
            args=['--url','http://123.lnk','--url','http://456.lnk'])
        expected_instance_object: Namespace = Namespace(url=['http://123.lnk','http://456.lnk'])
        self.assertIsNotNone(actual_instance_object)
        self.assertEqual(actual_instance_object, expected_instance_object)

    def test_get_list_of_rss_feed_urls_from_parsed_args(self) -> None:
        """Verify conversion from Namespace instance to list of object values
        """
        test_data: Namespace = Namespace(url=[1,2])
        actual_result: list[Any] = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(test_data) # pylint: disable=protected-access
        expected_result: list[Any] = [1,2]
        self.assertEqual(actual_result, expected_result)

    def test_get_list_of_rss_feed_urls_from_parsed_args_none(self) -> None:
        """Verify conversion from Namespace instance to empty list when a given value is None
        """
        test_data: Namespace = Namespace(url=None)
        actual_result: list[Any] = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(test_data) # pylint: disable=protected-access
        expected_result: list[Any] = []
        self.assertEqual(actual_result, expected_result)

    def test_get_list_of_rss_feed_urls_from_parsed_args_not_list(self) -> None:
        """Verify conversion from Namespace instance to empty list when a given value is not a list
        """
        test_data: Namespace = Namespace(url=1)
        actual_result: list[Any] = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(test_data) # pylint: disable=protected-access
        expected_result: list[Any] = []
        self.assertEqual(actual_result, expected_result)

    @staticmethod
    def test_show_rss_feed_content() -> None:
        """Verify code statements run successfully when invoking show_rss_feed_content method of
        default RSSFeedReader
        """
        test_data_item: RSSFeedItem = RSSFeedItem('','','')
        test_data: RSSFeedChannel = RSSFeedChannel('','','',list[RSSFeedItem]())
        test_data.items.append(test_data_item)
        devnull_file: TextIO
        with open(file=os.devnull, mode='w', encoding='utf-8') as devnull_file:
            cli_writer: RSSFeedReader = get_default_feedreader(file=devnull_file)
            cli_writer.show_rss_feed_content(test_data)

class TestRSSFeedMethods(unittest.TestCase):
    """Tests for entry point module of RSS feed reader
    """
    @staticmethod
    def mock_uri_method(url: Any) -> Any:
        """Mock method for type of ArgumentParser used to validate URLs.
        Used for testing purposes."""
        return url

    @staticmethod
    def test_main_noop() -> None:
        """Verify code statements successful when no arguments provided
        """
        devnull_file: TextIO
        with open(file=os.devnull, mode='w', encoding='utf-8') as devnull_file:
            main(output_stream=devnull_file, args=[])

    @staticmethod
    def test_main_with_arg() -> None:
        """Verify code statements successful when one argument provided
        """
        CLIParser._uri = TestRSSFeedMethods.mock_uri_method # pylint: disable=protected-access
        devnull_file: TextIO
        with open(file=os.devnull, mode='w', encoding='utf-8') as devnull_file:
            main(output_stream=devnull_file, args=['--url', 'testing'])
