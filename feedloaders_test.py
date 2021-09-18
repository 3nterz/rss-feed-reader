from typing import Any, Callable
import unittest
from model import RSSFeedChannel, RSSFeedItem
from feedloaders import _convert_html_content_to_text, _strip_whitespace
from feedloaders import FeedParserRSSFeedLoader

class TestRSSFeedParsers(unittest.TestCase):
    def test_convert_html_content_to_text(self) -> None:
        test_data: str = '<p>Paragraph</p>'
        actual_result: str = _convert_html_content_to_text(test_data)
        expected_result: str = 'Paragraph'
        self.assertEquals(actual_result, expected_result)

    def test_strip_whitespace(self) -> None:
        test_data: str = ' 123 '
        actual_result: str = _strip_whitespace(test_data)
        expected_result: str = '123'
        self.assertEquals(actual_result, expected_result)

    def test_parse_rss_feed_by_url(self) -> None:
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        actual_instance_object: dict[str, Any] = feedparser._parse_rss_feed_by_url('')
        self.assertIsNotNone(actual_instance_object)

    def template_test_check_dict_result(self, method: Callable[[dict[str, Any]], dict[str, Any]], test_data: dict[str, Any], expected_result: str) -> None:
        actual_result: dict[str, Any] = method(test_data)
        self.assertEquals(actual_result, expected_result)

    def test_get_parsed_rss_feed_channel(self) -> None:
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        self.template_test_check_dict_result(
            feedparser._get_parsed_rss_feed_channel,
            test_data={'feed':'result'},
            expected_result='result'
        )

    def test_get_parsed_rss_feed_item_list(self) -> None:
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        self.template_test_check_dict_result(
            feedparser._get_parsed_rss_feed_item_list, 
            test_data={'entries':'result'},
            expected_result='result'
        )

    def test_convert_parsed_rss_feed_item_to_rss_feed_item(self) -> None:
        feedparser: FeedParserRSSFeedLoader = FeedParserRSSFeedLoader('')
        test_data: dict[str, Any] = dict(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        actual_result: RSSFeedItem = feedparser._convert_parsed_rss_feed_item_to_rss_feed_item(test_data)
        expected_result: RSSFeedItem = RSSFeedItem(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        self.assertEquals(actual_result, expected_result)

    def test_convert_parsed_rss_feed_to_rss_feed_channel(self) -> None:
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
        actual_result: RSSFeedChannel = feedparser._convert_parsed_rss_feed_to_rss_feed_channel(test_data)
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
        self.assertEquals(actual_result, expected_result)
