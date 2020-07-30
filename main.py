import sys
import re
import urllib.request
from html.parser import HTMLParser
from collections import deque


class UrlHTMLParser(HTMLParser):

    def __init__(self, rootUrl):
        HTMLParser.__init__(self)
        self.urlQueue = deque()
        self.urlQueue.append(rootUrl)
        self.crawledUrls = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    # the parser does not work if the href
                    # uses single quotations, so I forced it:
                    if value[:2] == "\\'" and value[-2:] == "\\'":
                        self.urlQueue.append(value[2: -2])
                    else:
                        self.urlQueue.append(str(value))


class UrlHTMLParser2(HTMLParser):

    """This implementation looks for relative URLs, too"""

    def __init__(self, rootUrl):
        HTMLParser.__init__(self)
        self.baseUrl = rootUrl              # base for relative urls
        self.urlQueue = deque()
        self.urlQueue.append(rootUrl)
        self.crawledUrls = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name, value) in attrs:
                if name == 'href':
                    # relative url
                    if not re.match('https?:\/\/.*', value):
                        if self.baseUrl[-1] == '/':
                            aux = self.baseUrl[:-1]
                            self.baseUrl = aux
                        # the parser does not work if the href
                        # uses single quotations, so I forced it:
                        if value[:2] == "\\'" and value[-2:] == "\\'":
                            self.urlQueue.append(self.baseUrl + '/' + value[2:-2])
                        else:
                            self.urlQueue.append(self.baseUrl + '/' + str(value))
                    # absolute url
                    else:
                        if value[:2] == "\\'" and value[-2:] == "\\'":
                            self.urlQueue.append(value[2:-2])
                        else:
                            self.urlQueue.append(str(value))


def printUrls(urlNo, parserVersion):
    parser = None
    if (parserVersion == 1):
        parser = UrlHTMLParser(sys.argv[1])
    else:
        parser = UrlHTMLParser2(sys.argv[1])

    while len(parser.urlQueue) > 0 and len(parser.crawledUrls) < urlNo:
        currentUrl = parser.urlQueue.popleft()
        try:
            content = str(urllib.request.urlopen(currentUrl).read())
            if currentUrl not in parser.crawledUrls and currentUrl + '/' not in parser.crawledUrls:
                parser.baseUrl = currentUrl
                parser.feed(content)
                parser.crawledUrls.add(currentUrl)
                print(currentUrl)
        except:
            pass

printUrls(100, 1)
