from __future__ import print_function, division

import hashlib
import os


d = {
# data hash check for subject 1
'./ds105_old/sub001/BOLD/task001_run001/bold.nii.gz': "65f443622f3f600fb965943966518e6b",
'./ds105_old/sub001/BOLD/task001_run002/bold.nii.gz': "3680137dd2af37e2bf6faf60f0cb7841",
'./ds105_old/sub001/BOLD/task001_run003/bold.nii.gz': "eea714b14947a73d83bb51a0c370ce8c",
'./ds105_old/sub001/BOLD/task001_run004/bold.nii.gz': "de41e8060104696f3e2d5a908cd0770f",
'./ds105_old/sub001/BOLD/task001_run005/bold.nii.gz': "5801152f0b4d7031f7bfba50ecd13343",
'./ds105_old/sub001/BOLD/task001_run006/bold.nii.gz': "a64974f0030c939ba37b1b170194e53b",
'./ds105_old/sub001/BOLD/task001_run007/bold.nii.gz': "45da9ab760f43b268b01cff5024fd8a4",
'./ds105_old/sub001/BOLD/task001_run008/bold.nii.gz': "37472e2fc3e9ec9ad6d8d9ca7d19be05",
'./ds105_old/sub001/BOLD/task001_run009/bold.nii.gz': "bdfa0c72f0bf6f7f425cfd0a0e61e564",
'./ds105_old/sub001/BOLD/task001_run010/bold.nii.gz': "71cc8adb1274e5fb57f4a253f28669a1",
'./ds105_old/sub001/BOLD/task001_run011/bold.nii.gz': "b945b00ef11664fd4005e70558a7a211",
'./ds105_old/sub001/BOLD/task001_run012/bold.nii.gz': "a7124aa88bc29d76121cb07fb8e4ae0a",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond001.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond005.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond004.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond002.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond008.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond002.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond004.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond001.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond006.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond001.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond008.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond004.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond003.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond006.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond007.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond003.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond005.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond006.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond002.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond005.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond007.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond001.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond001.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond008.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond007.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond006.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond001.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond002.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond007.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond003.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond006.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond003.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond002.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond008.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond001.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond007.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond005.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond005.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond006.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond002.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond008.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond005.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond006.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond004.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond005.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond001.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond001.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond007.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond002.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond004.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond003.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond003.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond005.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond006.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run011/cond005.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond001.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond004.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond008.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond007.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond003.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond002.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond003.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond007.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond003.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond002.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond008.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond003.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond008.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond004.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run012/cond007.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond002.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond003.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond005.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond006.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond007.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond008.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond002.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond003.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond005.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond002.txt': "8cd8574d0f6110495b6291a99cd10f2d",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond004.txt': "5945c7ae1fb56a08ed211830cbdc2a45",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond006.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond004.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond008.txt': "a5e7be61a49df6b66cacb57bf0eedb77",
'./ds105_old/sub001/model/model001/onsets/task001_run010/cond007.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run009/cond006.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run001/cond004.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run005/cond008.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond001.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond005.txt': "41b83e3025e12e2fd0c96267e806034e",
'./ds105_old/sub001/model/model001/onsets/task001_run008/cond001.txt': "cac7baa6040f83eb166846087334d484",
'./ds105_old/sub001/model/model001/onsets/task001_run004/cond008.txt': "47d498aef4efa87c3bbe1b29f2156af0",
'./ds105_old/sub001/model/model001/onsets/task001_run003/cond004.txt': "13595e833e4fe17644abcd8bf76b9838",
'./ds105_old/sub001/model/model001/onsets/task001_run002/cond007.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run006/cond004.txt': "2c32bab7dbfe09767759ab65b079a0fa",
'./ds105_old/sub001/model/model001/onsets/task001_run007/cond006.txt': "a5e7be61a49df6b66cacb57bf0eedb77"
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
    if (all_good):
        print("All files have the correct hash.")
    else:
        print("At least one file has the WRONG hash. Please check above.")
    return all_good


if __name__ == "__main__":
    check_hashes(d)
