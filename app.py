from dataclasses import dataclass
import argparse
from sys import stdout
import feedparser
import html2text

@dataclass
class RSSFeedItem:
    title: str
    description: str
    link: str

@dataclass
class RSSFeedChannel:
    title: str
    description: str
    link: str
    items: list[RSSFeedItem]

def build_cli_parser():
    cli_parser = argparse.ArgumentParser(
        description='Fetches and displays content from the provided RSS feed URLs'
    )
    cli_parser.add_argument(
        '--url', 
        metavar=('http://.../atom10.xml'),
        action='append'
    )
    return cli_parser

def parse_rss_feed_urls_from_args(args=None, cli_parser=None):
    if cli_parser is None:
        cli_parser = build_cli_parser()
    return cli_parser.parse_args(args)

def get_list_of_rss_feed_urls(parsed_args):
    rss_feed_url_list = vars(parsed_args).get('url', [])
    if rss_feed_url_list is None:
        rss_feed_url_list = []
    return rss_feed_url_list

def parse_rss_feed_by_url(url):
    return feedparser.parse(url)

def get_parsed_rss_feed_channel(parsed_rss_feed):
    return parsed_rss_feed.get('feed', {})

def get_parsed_rss_feed_item_list(parsed_rss_feed):
    return parsed_rss_feed.get('entries', {})

def strip_whitespace(text_content):
    if text_content is not None and len(text_content) > 0:
        text_content = text_content.strip()
    return text_content

def convert_html_content_to_text(html_content):
    text_content = html2text.html2text(html_content)
    return strip_whitespace(text_content)

def convert_parsed_rss_feed_to_rss_feed_channel(parsed_rss_feed):
    parsed_rss_feed_channel = get_parsed_rss_feed_channel(parsed_rss_feed)
    parsed_rss_feed_item_list = get_parsed_rss_feed_item_list(parsed_rss_feed)
    rss_feed_item_list = list[RSSFeedItem]()
    for parsed_rss_feed_item in parsed_rss_feed_item_list:
        rss_feed_item = convert_parsed_rss_feed_item_to_rss_feed_item(parsed_rss_feed_item)
        rss_feed_item_list.append(rss_feed_item)

    whitespace_stripped_title = strip_whitespace(parsed_rss_feed_channel.get('title', 'No title'))
    whitespace_stripped_description = convert_html_content_to_text(parsed_rss_feed_channel.get('description', 'No description'))
    whitespace_stripped_link = strip_whitespace(parsed_rss_feed_channel.get('link', 'No link'))

    return RSSFeedChannel(
        title=whitespace_stripped_title,
        description=whitespace_stripped_description,
        link=whitespace_stripped_link,
        items=rss_feed_item_list
    )

def convert_parsed_rss_feed_item_to_rss_feed_item(parsed_rss_feed_item):

    whitespace_stripped_title = strip_whitespace(parsed_rss_feed_item.get('title', 'No title'))
    whitespace_stripped_description = convert_html_content_to_text(parsed_rss_feed_item.get('description', 'No description'))
    whitespace_stripped_link = strip_whitespace(parsed_rss_feed_item.get('link', 'No link'))

    return RSSFeedItem(
        title=whitespace_stripped_title,
        description=whitespace_stripped_description,
        link=whitespace_stripped_link
    )

def show_rss_feed_content(content, output_stream):
    print(f"""{'='*20}
Feed Title: {content.title}
Link: {content.link}
{content.description}
""", file=output_stream)
    for item in content.items:
        print(f"""{'-'*20}
Item Title: {item.title}
Link: {item.link}
{item.description}
""", file=output_stream)

def main(output_stream=stdout, args=None):
    cli_parser = build_cli_parser()
    parsed_args = parse_rss_feed_urls_from_args(args=args, cli_parser=cli_parser)
    rss_feed_url_list = get_list_of_rss_feed_urls(parsed_args)
    if len(rss_feed_url_list) == 0:
        cli_parser.print_usage(file=output_stream)
    else:
        for rss_feed_url in rss_feed_url_list:
            parsed_rss_feed = parse_rss_feed_by_url(rss_feed_url)
            rss_feed_channel = convert_parsed_rss_feed_to_rss_feed_channel(parsed_rss_feed)
            show_rss_feed_content(rss_feed_channel, output_stream=output_stream)

if __name__ == '__main__':
    main()