"""Define the protocol for which all RSS Feed Loader implementations will follow
"""
from typing import Protocol
from model import RSSFeedChannel

class RSSFeedLoader(Protocol):
    """Protocol for which all RSS Feed Loader implementations will follow
    """
    def load_rss_feed(self) -> None:
        """RSS feed content is loaded in this method."""

    def get_rss_feed_channel(self) -> RSSFeedChannel:
        """Returns RSS feed channel content as an instance of RSSFeedChannel"""
