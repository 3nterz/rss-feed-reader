"""Define the protocol for which all RSS Feed Reader implementations will follow
"""
from typing import Protocol
from model import RSSFeedChannel

class RSSFeedReader(Protocol):
    """Protocol for which all RSS Feed Loader implementations will follow
    """
    @staticmethod
    def initialise():
        """Prepare the RSS Feed Reader instance"""

    def show_rss_feed_content(self, content: RSSFeedChannel) -> None:
        """RSS Feed content is rendered using this method"""
