# WebCrawler

This is a basic web crawler that uses Python and HTMLParser to 'recursively' crawl the URLs on a given page (limited to 100).

## Breadth First Search vs Depth First Search

The word 'recursive' is not accurate, because this script uses the BFS algorithm with a queue rather than a recursive DFS. This is because it makes more sense to fully explore the current page before moving on, rather than going as deep as possible before returning to the current page. Also, considering, the potential 'depth' of the internet, the resulted URLs would probably form a chain rather than a tree (because of our limit - otherwise it would probably overflow the stack).

## Absolute vs Relative URLs

There are two implementations in this script: one that only searches for absolute URLs and one that searches for both absolute URLs and URLs relative to the current path. Although the second implementation might seem more complete, it reaches a lot of useless links, many of them return an HTTP error, and as a consequence it is much slower than the first implementation. Therefore, the default implementation is the one that displays the Absolute URLs. 
