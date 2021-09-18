"""Tests for module feedloaders
"""
from typing import Any, Callable
import unittest
from model import RSSFeedChannel, RSSFeedItem
from feedloaders import _convert_html_content_to_text, _strip_whitespace
from feedloaders import FeedParserRSSFeedLoader

class TestRSSFeedParsers(unittest.TestCase):
    """Tests for module feedloaders members including class FeedParserRSSFeedLoader
    """
    def test_convert_html_content_to_text(self) -> None:
        """Verify html entities in HTML content are removed when converted to plain text
        """
        test_data: str = '<p>Paragraph</p>'
        actual_result: str = _convert_html_content_to_text(test_data) #pylint: disable=protected-access
        expected_result: str = 'Paragraph'
        self.assertEqual(actual_result, expected_result)

    def test_strip_whitespace(self) -> None:
        """Verify leading and trailing whitespace are removed when invoking method
        """
        test_data: str = ' 123 '
        actual_result: str = _strip_whitespace(test_data) #pylint: disable=protected-access
        expected_result: str = '123'
        self.assertEqual(actual_result, expected_result)

    def test_parse_rss_feed_by_url(self) -> None:
        """Verify calling _parse_rss_feed_by_url with empty string does not return None
        """
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        actual_instance_object: dict[str, Any] = feedparser._parse_rss_feed_by_url('') #pylint: disable=protected-access
        self.assertIsNotNone(actual_instance_object)

    def template_test_check_dict_result(self,
    method: Callable[[dict[str, Any]], dict[str, Any]],
    test_data: dict[str, Any], expected_result: str) -> None:
        """Template method to perform invoke common set of code statements across
        multiple test methods.
        """
        actual_result: dict[str, Any] = method(test_data)
        self.assertEqual(actual_result, expected_result)

    def test_get_parsed_rss_feed_channel(self) -> None:
        """Verify specifying test data with key 'feed' correctly resolves the value
        """
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        self.template_test_check_dict_result(
            feedparser._get_parsed_rss_feed_channel, #pylint: disable=protected-access
            test_data={'feed':'result'},
            expected_result='result'
        )

    def test_get_parsed_rss_feed_item_list(self) -> None:
        """Verify specifying test data with key 'entries' correctly resolves the value
        """
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        self.template_test_check_dict_result(
            feedparser._get_parsed_rss_feed_item_list, #pylint: disable=protected-access
            test_data={'entries':'result'},
            expected_result='result'
        )

    def test_convert_parsed_rss_feed_item_to_rss_feed_item(self) -> None:
        """Verify dict is successfully converted to RSSFeedItem
        """
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        test_data: dict[str, Any] = dict(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        actual_result: RSSFeedItem = feedparser._convert_parsed_rss_feed_item_to_rss_feed_item( #pylint: disable=W0212
                test_data)
        expected_result: RSSFeedItem = RSSFeedItem(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        self.assertEqual(actual_result, expected_result)

    def test_convert_parsed_rss_feed_to_rss_feed_channel(self) -> None:
        """Verify dict is successfully converted to RSSFeedChannel
        """
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        test_data: dict[str, Any] = {
            'feed': {
                'title': 'Some feed title',
                'description': 'Some feed description here.',
                'link': 'http://somefeedlink.lnk'
            },
            'entries': [{
                'title': 'Some item title',
                'description': 'Some item description here.',
                'link': 'http://someitemlink.lnk'
            },]
        }
        actual_result: RSSFeedChannel =  feedparser._convert_parsed_rss_feed_to_rss_feed_channel( #pylint: disable=W0212
            test_data)
        expected_result_item: RSSFeedItem = RSSFeedItem(
            title='Some item title',
            description='Some item description here.',
            link='http://someitemlink.lnk'
        )
        expected_result_items: list[RSSFeedItem] = list[RSSFeedItem]()
        expected_result_items.append(expected_result_item)
        expected_result: RSSFeedChannel = RSSFeedChannel(
            title='Some feed title',
            description='Some feed description here.',
            link='http://somefeedlink.lnk',
            items=expected_result_items
        )
        self.assertEqual(actual_result, expected_result)
