import importer
import sys


def main():
    if len(sys.argv) != 2:
        print 'Invalid args'
        return

    if sys.argv[1] == 'rss':
        importer.import_rss_feed()
    elif sys.argv[1] == 'archive':
        importer.import_archives()


if __name__ == '__main__':
    main()
