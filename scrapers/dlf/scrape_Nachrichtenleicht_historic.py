#!/usr/bin/env python3

from DLFScrapers import NachrichtenleichtScraper


for offset_start in range(0, 20000, 100):
    offset_end = offset_start + 100
    nl_feed_url = 'https://www.nachrichtenleicht.de/api/partials/PaginatedArticles_NL?drsearch:currentItems='+ str(offset_start) + '&drsearch:itemsPerLoad=' + str(offset_end) + '&drsearch:partialProps={%22sophoraId%22:%22nachrichtenleicht-nachrichten-100%22}&drsearch:_ajax=1'
    NachrichtenleichtScraper(nl_feed_url).scrape()
