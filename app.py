"""Application entry point for RSS Feed Reader
"""
from model import RSSFeedChannel
from sys import stdout
from typing import Optional, Sequence, TextIO
from cli import CLIParser
from rssfeedloader import RSSFeedLoader
from rssfeedreader import RSSFeedReader

def get_default_feedloader(rss_feed_url: str) -> RSSFeedLoader:
    from feedloaders import FeedParserRSSFeedLoader
    return FeedParserRSSFeedLoader(rss_feed_url)

def get_default_feedreader(file: TextIO) -> RSSFeedReader:
    from cli import CLIWriter
    return CLIWriter(file=file)

def main(output_stream: TextIO=stdout, args: Optional[Sequence[str]]=None) -> None:
    cli_parser: CLIParser = CLIParser(file=output_stream)
    cli_writer: RSSFeedReader = get_default_feedreader(file=output_stream)
    cli_parser.parse_rss_feed_urls_from_args(args)
    rss_feed_url_list: list[str] = [str(url) for url in cli_parser.get_list_of_rss_feed_urls()]

    # in the backgeound process all feed urls
    feedloader_list: list[RSSFeedLoader] = []
    rss_feed_url: str
    for rss_feed_url in rss_feed_url_list:
        feedloader: RSSFeedLoader = get_default_feedloader(rss_feed_url)
        feedloader.load_rss_feed()
        feedloader_list.append(feedloader)
    
    # display all output together
    feedloader: RSSFeedLoader
    for feedloader in feedloader_list:
        rss_feed_channel: RSSFeedChannel = feedloader.get_rss_feed_channel()
        cli_writer.show_rss_feed_content(rss_feed_channel)

if __name__ == '__main__':
    main()