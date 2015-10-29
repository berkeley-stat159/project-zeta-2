from __future__ import print_function, division

import hashlib
import os


d = {
'./ds105/sub001/BOLD/task001_run001/bold.nii.gz': "65f443622f3f600fb965943966518e6b"
'./ds105/sub001/BOLD/task001_run002/bold.nii.gz': "3680137dd2af37e2bf6faf60f0cb7841"
'./ds105/sub001/BOLD/task001_run003/bold.nii.gz': "eea714b14947a73d83bb51a0c370ce8c"
'./ds105/sub001/BOLD/task001_run004/bold.nii.gz': "de41e8060104696f3e2d5a908cd0770f"
'./ds105/sub001/BOLD/task001_run005/bold.nii.gz': "5801152f0b4d7031f7bfba50ecd13343"
'./ds105/sub001/BOLD/task001_run006/bold.nii.gz': "a64974f0030c939ba37b1b170194e53b"
'./ds105/sub001/BOLD/task001_run007/bold.nii.gz': "45da9ab760f43b268b01cff5024fd8a4"
'./ds105/sub001/BOLD/task001_run008/bold.nii.gz': "37472e2fc3e9ec9ad6d8d9ca7d19be05"
'./ds105/sub001/BOLD/task001_run009/bold.nii.gz': "bdfa0c72f0bf6f7f425cfd0a0e61e564"
'./ds105/sub001/BOLD/task001_run010/bold.nii.gz': "71cc8adb1274e5fb57f4a253f28669a1"
'./ds105/sub001/BOLD/task001_run011/bold.nii.gz': "b945b00ef11664fd4005e70558a7a211"
'./ds105/sub001/BOLD/task001_run012/bold.nii.gz': "a7124aa88bc29d76121cb07fb8e4ae0a"

}


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
    return all_good


if __name__ == "__main__":
    check_hashes(d)
