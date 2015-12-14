structure:
    python structure

data:
	# download raw data from openfmir database
	wget http://openfmri.s3.amazonaws.com/tarballs/ds105_raw.tgz
	# unzip raw data
	tar -xvzf ./ds105_raw.tgz
	# rename folder: ds105 -> ds105_raw
	mv ds105 ds105_old
	# download preprocessed data
	wget https://nipy.bic.berkeley.edu/rcsds/ds105_mnifunc.tar
	# unzip preprocessed data
	tar -xvzf ./ds105_mnifunc.tar
	# rename folder:
	mv ds105 ds105_new
	# download actc.txt
	wget http://www.jarrodmillman.com/rcsds/_downloads/actc.txt
	mv actc.txt ../code/txt/
   
validate:
	python data.py
