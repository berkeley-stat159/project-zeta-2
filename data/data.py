from __future__ import print_function, division

import hashlib
import json

def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def check_hashes(d):
    all_good = True
    for k, v in d.items():
        digest = generate_file_md5(k)
        if v == digest:
            print("The file {0} has the correct hash.".format(k))
        else:
            print("ERROR: The file {0} has the WRONG hash!".format(k))
            all_good = False
    if (all_good):
        print("All files have the correct hash.")
    else:
        print("At least one file has the WRONG hash. Please check above.")
    return all_good


if __name__ == "__main__":
    with open('hash_check.json', 'r') as hashfile:
        d = json.load(hashfile)
    check_hashes(d)
