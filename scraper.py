#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse
import urllib.request
import shutil
import tempfile
import os
import string

# Idea of parameters
# URL to donwload
# filetype to search for
# destination path
# verbose option
#
# Download should check whether file exists or not
# Program should give a log of files found. Those downloaded and those already existing
# Program can also just produce a list of files found perhaps?

def covert_to_filename(s):
    s = s.replace('&', 'and')
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def main():
    parser = argparse.ArgumentParser(description="Fetch files from a given XML file")
    parser.add_argument('url', metavar='URL', type=str, help='URL to XML file to scan for the files of a given type')
    parser.add_argument('--dest', default=None, type=str,  help='Destination folder')
    parser.add_argument('--dryrun', action='store_true', help='Do dry run test')
    parser.add_argument('--writexml', default=None, type=str, help='Write RSS XML to a specified file (useful for debugging)')
    parser.add_argument('--fileuniq', action='store_true', help='Tries to make filename unique using full URL path')
    parser.add_argument('--filetitle', action='store_true', help='Prefix filename with the title')

    args = parser.parse_args()

    with urllib.request.urlopen(args.url) as f:
        
        # Fetch URL to a temporary file
        fp = tempfile.NamedTemporaryFile(mode='w', delete=False)
        fp.write(f.read().decode('utf-8'))
        fp.close()

        if args.writexml:
            shutil.copyfile(fp.name, args.writexml)

        if args.dest:
            output_dir = os.path.expanduser(args.dest)
            output_dir = os.path.abspath(output_dir)

            if not os.path.isdir(output_dir):
                print("The directory: {} cannot be found".format(output_dir))
                quit()

            # Load XML and look for URLs
            tree = ET.parse(fp.name)
            root = tree.getroot()
            parent_map = {c:p for p in root.iter() for c in p}
            for data in root.iter('enclosure'):
                # print(data.get('url'))
                url = data.get('url')
                url_parsed = urllib.parse.urlparse(url)

                if args.fileuniq:
                    filename = '_'.join(url_parsed.path.split('/')).lstrip('_')
                else:
                    filename = os.path.basename(url_parsed.path)

                if args.filetitle:
                    title = '_'.join(parent_map[data].find('title').text.split(' ')).lstrip('_')
                    filename = title + '_' + filename

                filename = covert_to_filename(filename)

                output = os.path.join(output_dir, filename)
                if os.path.exists(output):
                    print("NOT downloading {} as it already exists".format(filename))
                else:
                    print("Downloading {} (saving as {})".format(url_parsed.geturl(), filename))
                    if not args.dryrun:
                        # Download and write out file
                        with urllib.request.urlopen(url_parsed.geturl()) as response, open(output, 'wb') as out_file:
                            shutil.copyfileobj(response, out_file)

        # Clean up
        os.unlink(fp.name)

if __name__ == "__main__":
    main()
    
