"""feedparsers: contains one or more implementations of the RSSFeedLoader protocol
"""
from typing import Any
import feedparser
import html2text
from model import RSSFeedItem, RSSFeedChannel

def _strip_whitespace(text_content: str) -> str:
    """Return text_content with leading and trailing whitespace removed
    """
    output_content: str = str(text_content)
    if text_content is not None and len(text_content) > 0:
        output_content = text_content.strip()
    return output_content

def _convert_html_content_to_text(html_content: str) -> str:
    """Return html_content (expecting HTML content) as plain text with leading and
    trailing whitespace removed
    """
    text_content: str = html2text.html2text(html_content, bodywidth=0)
    return _strip_whitespace(text_content)

class FeedParserRSSFeedLoader:
    """Implements the RSSFeedLoader protocol using feedparser and html2text libraries
    """
    def __init__(self, url: str) -> None:
        """Build an instance of FeedParserRSSFeedLoader
        """
        self.url: str = url
        self.rss_feed_channel: RSSFeedChannel = RSSFeedChannel('','','', list[RSSFeedItem]())

    def load_rss_feed(self) -> None:
        """RSS feed content is loaded in this method
        """
        parsed_rss_feed: dict[str, Any] = self._parse_rss_feed_by_url(self.url)
        self.rss_feed_channel: RSSFeedChannel = self._convert_parsed_rss_feed_to_rss_feed_channel(
            parsed_rss_feed)

    def get_rss_feed_channel(self) -> RSSFeedChannel:
        """Returns RSS feed channel content as an instance of RSSFeedChannel"""
        return self.rss_feed_channel


    def _convert_parsed_rss_feed_to_rss_feed_channel(self,
    parsed_rss_feed: dict[str, Any]) -> RSSFeedChannel:
        parsed_rss_feed_channel: dict[str, Any] = self._get_parsed_rss_feed_channel(
            parsed_rss_feed)
        parsed_rss_feed_item_list: dict[str, Any] = self._get_parsed_rss_feed_item_list(
            parsed_rss_feed)
        rss_feed_item_list: list[RSSFeedItem] = list[RSSFeedItem]()
        parsed_rss_feed_item: Any
        for parsed_rss_feed_item in parsed_rss_feed_item_list:
            rss_feed_item: RSSFeedItem = self._convert_parsed_rss_feed_item_to_rss_feed_item(
                parsed_rss_feed_item)
            rss_feed_item_list.append(rss_feed_item)

        whitespace_stripped_title: str = _strip_whitespace(
            parsed_rss_feed_channel.get('title', 'No title'))
        whitespace_stripped_description: str = _convert_html_content_to_text(
            parsed_rss_feed_channel.get('description', 'No description'))
        whitespace_stripped_link: str = _strip_whitespace(
            parsed_rss_feed_channel.get('link', 'No link'))

        return RSSFeedChannel(
            title=whitespace_stripped_title,
            description=whitespace_stripped_description,
            link=whitespace_stripped_link,
            items=rss_feed_item_list
        )

    @staticmethod
    def _parse_rss_feed_by_url(url: str) -> dict[str, Any]:
        return feedparser.parse(url)

    @staticmethod
    def _get_parsed_rss_feed_channel(parsed_rss_feed: dict[str, Any]) -> dict[str, Any]:
        return parsed_rss_feed.get('feed', {})

    @staticmethod
    def _get_parsed_rss_feed_item_list(parsed_rss_feed: dict[str, Any]) -> dict[str, Any]:
        return parsed_rss_feed.get('entries', {})

    @staticmethod
    def _convert_parsed_rss_feed_item_to_rss_feed_item(
        parsed_rss_feed_item: dict[str, Any]) -> RSSFeedItem:

        whitespace_stripped_title: str = _strip_whitespace(
            parsed_rss_feed_item.get('title', 'No title'))
        whitespace_stripped_description: str = _convert_html_content_to_text(
            parsed_rss_feed_item.get('description', 'No description'))
        whitespace_stripped_link: str = _strip_whitespace(
            parsed_rss_feed_item.get('link', 'No link'))

        return RSSFeedItem(
            title=whitespace_stripped_title,
            description=whitespace_stripped_description,
            link=whitespace_stripped_link
        )
