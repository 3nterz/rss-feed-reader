"""model: Defined data structures for rss-feed-reader"""
from dataclasses import dataclass

@dataclass
class RSSFeedItem:
    """ Representation of an RSS Feed Item """
    title: str
    description: str
    link: str

@dataclass
class RSSFeedChannel:
    """ Representation of an RSS Feed Channel """
    title: str
    description: str
    link: str
    items: list[RSSFeedItem]
