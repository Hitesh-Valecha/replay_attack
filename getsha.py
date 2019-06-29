import hashlib

import sys


def get_sha1(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print(get_sha1(sys.argv[1]))
