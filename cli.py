"""cli: module to handle the validation and parsing of the RSS feed URLs on the
command line interface.
"""
from sys import stdout
from typing import TextIO, Sequence, Any, Optional
from argparse import ArgumentParser, Namespace
import validators
from model import RSSFeedChannel, RSSFeedItem

class CLIWriter:
    """Class to write RSS feed content to the commane line interface
    """
    def __init__(self, file: TextIO) -> None:
        """Build a CLIWriter
        """
        self.output_stream: TextIO = file
        CLIWriter.initialise()

    @staticmethod
    def initialise() -> None:
        """Prepare the RSS Feed Reader instance"""
        return None

    def print_func(self, msg: str) -> None:
        """Template method to reduce line length.
        Set print function output stream in one place.
        """
        print(msg, file=self.output_stream)

    def show_rss_feed_content(self, content: RSSFeedChannel) -> None:
        """Render representation of RSSFeedChannel on the CLI
        """
        self.print_func(f"{'='*20}")
        self.print_func(f"Feed Title: {content.title}")
        self.print_func(f"Link: {content.link}")
        self.print_func(f"{content.description}")
        item: RSSFeedItem
        for item in content.items:
            self.print_func(f"{'-'*20}")
            self.print_func(f"Item Title: {item.title}")
            self.print_func(f"Link: {item.link}")
            self.print_func(f"{item.description}")

class CLIParser:
    """Class to encapsulate the parsing of the RSS feed URLs on the command line interface.
    """
    def __init__(self, file: TextIO=stdout):
        """Builds a CLIParser instance, with optional parameter file to specify target of CLI output
        """
        self.cli_parser: ArgumentParser = CLIParser._build_argument_parser()
        self.rss_feed_url_list: list[Any] = list[Any]()
        self.output_stream: TextIO = file

    @staticmethod
    def _uri(url: Any) -> Any:
        """Returns url if url is a valid URL
        ValueError: If url is not a valid URL
        """
        if validators.url(url) is True:
            return url
        raise ValueError

    @staticmethod
    def _build_argument_parser() -> ArgumentParser:
        """Returns object responsible for transforming command line strings into RSS feed URLs.
        """
        cli_parser: ArgumentParser = ArgumentParser(
            description='Fetches and displays content from the provided RSS feed URLs'
        )
        cli_parser.add_argument(
            '--url',
            metavar=('http://... http://...'),
            type=CLIParser._uri,
            action='append'
        )
        return cli_parser

    @staticmethod
    def _get_list_of_rss_feed_urls_from_parsed_args(parsed_args: Namespace) -> list[Any]:
        """Returns list of RSS Feed URLs from given Namespace object
        """
        rss_feed_url_list = vars(parsed_args).get('url', list[Any]())
        if rss_feed_url_list is None:
            rss_feed_url_list = list[Any]()
        if not isinstance(rss_feed_url_list, list):
            rss_feed_url_list = list[Any]()
        return rss_feed_url_list

    def _get_parsed_namespace_from_args(self, args: Optional[Sequence[str]]=None) -> Namespace:
        """Returns Namespace object resulting from parsing command line strings
        """
        return self.cli_parser.parse_args(args=args)

    def parse_rss_feed_urls_from_args(self, args: Optional[Sequence[str]]=None) -> None:
        """Parses RSS Feed URLs from command line strings.
        Prints out help message for CLI usage if no URLs are provided.
        Performs validation of RSS Feed URLs and prints out error if it finds a string
        that is not a valid URL.
        """
        parsed_args: Namespace = self._get_parsed_namespace_from_args(args=args)
        self.rss_feed_url_list = CLIParser._get_list_of_rss_feed_urls_from_parsed_args(parsed_args)
        if len(self.rss_feed_url_list) == 0:
            self.cli_parser.print_usage(self.output_stream)

    def get_list_of_rss_feed_urls(self) -> list[Any]:
        """Returns list of validated RSS feed URLs from command line strings.
        """
        return self.rss_feed_url_list
