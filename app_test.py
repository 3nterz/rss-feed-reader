from argparse import ArgumentParser, Namespace
import unittest
import os
from argparse import ArgumentParser
from feedparser.util import FeedParserDict
from app import RSSFeedChannel, RSSFeedItem
from app import build_cli_parser, parse_rss_feed_urls_from_args
from app import get_list_of_rss_feed_urls, parse_rss_feed_by_url
from app import get_parsed_rss_feed_channel, get_parsed_rss_feed_item_list
from app import convert_html_content_to_text, strip_whitespace
from app import show_rss_feed_content, convert_parsed_rss_feed_item_to_rss_feed_item
from app import convert_parsed_rss_feed_to_rss_feed_channel, main

class TestRSSFeedDataClasses(unittest.TestCase):

    def test_build_rss_feed_item(self):
        actualRSSFeedItem = RSSFeedItem(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        expectedRSSFeedItem = RSSFeedItem(None,None,None)
        expectedRSSFeedItem.title = 'Some title'
        expectedRSSFeedItem.description = 'Some description here.'
        expectedRSSFeedItem.link = 'http://somelink.lnk'
        self.assertEqual(actualRSSFeedItem, expectedRSSFeedItem)

    def test_build_rss_feed_channel(self):
        items=list[RSSFeedItem]()
        items.append(RSSFeedItem('a','b','c'))
        actualRSSFeedChannel = RSSFeedChannel(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk',
            items=items
        )
        expectedRSSFeedChannel = RSSFeedChannel(None,None,None,None)
        expectedRSSFeedChannel.title = 'Some title'
        expectedRSSFeedChannel.description = 'Some description here.'
        expectedRSSFeedChannel.link = 'http://somelink.lnk'
        expectedRSSFeedChannel.items = items
        self.assertEqual(actualRSSFeedChannel, expectedRSSFeedChannel)

class TestRSSFeedMethods(unittest.TestCase):

    def test_build_cli_parser(self):
        self.assertTrue(isinstance(build_cli_parser(),ArgumentParser))

    def test_parse_rss_feed_urls_from_args(self):
        actual_instance_object = parse_rss_feed_urls_from_args(args=['--url','123','--url','456']) 
        expected_instance_object = Namespace(url=['123','456'])
        self.assertTrue(isinstance(actual_instance_object,Namespace))
        self.assertEquals(actual_instance_object, expected_instance_object)

    def test_get_list_of_rss_feed_urls(self):
        test_data = Namespace(url=[1,2])
        actual_result = get_list_of_rss_feed_urls(test_data)
        expected_result = [1,2]
        self.assertEquals(actual_result, expected_result)

    def test_get_list_of_rss_feed_urls_None(self):
        test_data = Namespace(url=None)
        actual_result = get_list_of_rss_feed_urls(test_data)
        expected_result = []
        self.assertEquals(actual_result, expected_result)

    def test_parse_rss_feed_by_url(self):
        actual_instance_object = parse_rss_feed_by_url('')
        self.assertTrue(isinstance(actual_instance_object,FeedParserDict))

    def template_test_check_dict_result(self, method, test_data, expected_result):
        actual_result = method(test_data)
        self.assertEquals(actual_result, expected_result)

    def test_get_parsed_rss_feed_channel(self):
        self.template_test_check_dict_result(
            get_parsed_rss_feed_channel, 
            test_data={'feed':'result'},
            expected_result='result'
        )

    def test_get_parsed_rss_feed_item_list(self):
        self.template_test_check_dict_result(
            get_parsed_rss_feed_item_list, 
            test_data={'entries':'result'},
            expected_result='result'
        )

    def test_convert_html_content_to_text(self):
        test_data = '<p>Paragraph</p>'
        actual_result = convert_html_content_to_text(test_data)
        expected_result = 'Paragraph'
        self.assertEquals(actual_result, expected_result)

    def test_strip_whitespace(self):
        test_data = ' 123 '
        actual_result = strip_whitespace(test_data)
        expected_result = '123'
        self.assertEquals(actual_result, expected_result)

    def test_show_rss_feed_content(self):
        test_data_item = RSSFeedItem('','','')
        test_data = RSSFeedChannel('','','',list[RSSFeedItem]())
        test_data.items.append(test_data_item)
        with open(os.devnull, 'w') as f:
            show_rss_feed_content(test_data, output_stream=f)

    def test_convert_parsed_rss_feed_item_to_rss_feed_item(self):
        test_data = dict(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        actual_result = convert_parsed_rss_feed_item_to_rss_feed_item(test_data)
        expected_result = RSSFeedItem(
            title='Some title',
            description='Some description here.',
            link='http://somelink.lnk'
        )
        self.assertEquals(actual_result, expected_result)

    def test_convert_parsed_rss_feed_to_rss_feed_channel(self):
        test_data = {
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
        actual_result = convert_parsed_rss_feed_to_rss_feed_channel(test_data)
        expected_result_item = RSSFeedItem(
            title='Some item title',
            description='Some item description here.',
            link='http://someitemlink.lnk'
        )
        expected_result_items = list[RSSFeedItem]()
        expected_result_items.append(expected_result_item)
        expected_result = RSSFeedChannel(
            title='Some feed title',
            description='Some feed description here.',
            link='http://somefeedlink.lnk',
            items=expected_result_items
        )
        self.assertEquals(actual_result, expected_result)

    def test_main_noop(self):
        with open(os.devnull, 'w') as f:
            main(output_stream=f, args=['--url','1'])