data:
	# download raw data from openfmir database
	wget http://openfmri.s3.amazonaws.com/tarballs/ds105_raw.tgz
	# unzip raw data
	tar -xvzf ./ds105_raw.tgz
	# rename folder: ds105 -> ds105_raw
	mv ds105 ds105_raw
	# download preprocessed data
	wget https://nipy.bic.berkeley.edu/rcsds/ds105_mnifunc.tar
	# unzip preprocessed data
	tar -xvzf ./ds105_mnifunc.tar
   
validate:
	python data.py
