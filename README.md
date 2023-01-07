# Podcast scraper
Downloads podcast files from a given RSS feed

Very much work-in-progress at the moment. Generally it gets modified as and when I try to download a new set of podcasts.

Using it is as simple as:

$ ./scraper-py --dest "/local_folder/" http://www.address_to_rss.com/url.xml

You may want to use `--dryrun` first to check what files it intends to download. The script will try to avoid downloading files that have already been downloaded before.

If the filenames of the RSS feed are not unique then try `--fileuniq` to prefix the filename with the URL.
