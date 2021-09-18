from argparse import Namespace
from typing import Any, TextIO
from rssfeedreader import RSSFeedReader
import unittest
import os
from model import RSSFeedChannel, RSSFeedItem
from cli import CLIParser
from app import get_default_feedreader
from app import main

class TestRSSFeedDataClasses(unittest.TestCase):

    def test_build_rss_feed_item(self) -> None:
        actualRSSFeedItem: RSSFeedItem = RSSFeedItem(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        expectedRSSFeedItem: RSSFeedItem = RSSFeedItem('','','')
        expectedRSSFeedItem.title = 'Some title'
        expectedRSSFeedItem.description = 'Some description here.'
        expectedRSSFeedItem.link = 'http://somelink.lnk'
        self.assertEqual(actualRSSFeedItem, expectedRSSFeedItem)

    def test_build_rss_feed_channel(self) -> None:
        items: list[RSSFeedItem] = list[RSSFeedItem]()
        items.append(RSSFeedItem('a','b','c'))
        actualRSSFeedChannel: RSSFeedChannel = RSSFeedChannel(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk',
            items=items
        )
        expectedRSSFeedChannel: RSSFeedChannel = RSSFeedChannel('','','',list[RSSFeedItem]())
        expectedRSSFeedChannel.title = 'Some title'
        expectedRSSFeedChannel.description = 'Some description here.'
        expectedRSSFeedChannel.link = 'http://somelink.lnk'
        expectedRSSFeedChannel.items = items
        self.assertEqual(actualRSSFeedChannel, expectedRSSFeedChannel)

class TestRSSFeedCLI(unittest.TestCase):
    def test_build_cli_parser(self) -> None:
        self.assertIsNotNone(CLIParser._build_argument_parser())

    def test_invalid_URL(self) -> None:
        self.assertRaises(ValueError, CLIParser._URI, 'invalidurl') 

    def test_get_parsed_namespace_from_args(self) -> None:
        cli_parser: CLIParser = CLIParser()
        actual_instance_object: Namespace = cli_parser._get_parsed_namespace_from_args(args=['--url','http://123.lnk','--url','http://456.lnk']) 
        expected_instance_object: Namespace = Namespace(url=['http://123.lnk','http://456.lnk'])
        self.assertIsNotNone(actual_instance_object)
        self.assertEqual(actual_instance_object, expected_instance_object)

    def test_get_list_of_rss_feed_urls_from_parsed_args(self) -> None:
        test_data: Namespace = Namespace(url=[1,2])
        actual_result: list[Any] = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(test_data) 
        expected_result: list[Any] = [1,2]
        self.assertEqual(actual_result, expected_result)

    def test_get_list_of_rss_feed_urls_from_parsed_args_None(self) -> None:
        test_data: Namespace = Namespace(url=None)
        actual_result: list[Any] = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(test_data) 
        expected_result: list[Any] = []
        self.assertEqual(actual_result, expected_result)

    def test_get_list_of_rss_feed_urls_from_parsed_args_not_list(self) -> None:
        test_data: Namespace = Namespace(url=1)
        actual_result: list[Any] = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(test_data) 
        expected_result: list[Any] = []
        self.assertEqual(actual_result, expected_result)

    def test_show_rss_feed_content(self) -> None:
        test_data_item: RSSFeedItem = RSSFeedItem('','','')
        test_data: RSSFeedChannel = RSSFeedChannel('','','',list[RSSFeedItem]())
        test_data.items.append(test_data_item)
        f: TextIO
        with open(os.devnull, 'w') as f:
            cli_writer: RSSFeedReader = get_default_feedreader(file=f)
            cli_writer.show_rss_feed_content(test_data)

class TestRSSFeedMethods(unittest.TestCase):

    def test_main_noop(self) -> None:
        f: TextIO
        with open(os.devnull, 'w') as f:
            main(output_stream=f, args=[])

    @staticmethod
    def mock_URI_method(url: Any) -> bool:
        return url

    def test_main_with_arg(self) -> None:
        CLIParser._URI = TestRSSFeedMethods.mock_URI_method
        f: TextIO
        with open(os.devnull, 'w') as f:
            main(output_stream=f, args=['--url', 'testing'])
