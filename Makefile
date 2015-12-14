.PHONY: all clean coverage test data validate analysis report

all: clean coverage test data validate analysis report

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

coverage:
	nosetests code/utils data --with-coverage --cover-package=data  --cover-package=utils

test:
	nosetests code/utils/tests data

verbose:
	nosetests -v code/utils data

data:
	# download raw data from openfmir database
	wget http://openfmri.s3.amazonaws.com/tarballs/ds105_raw.tgz
	# unzip raw data
	tar -zxvf ./ds105_raw.tgz
	# rename folder: ds105 -> ds105_raw
	mv ds105 ds105_old
	# Move to Data
	mv ds105_old /data
	# download preprocessed data
	wget https://nipy.bic.berkeley.edu/rcsds/ds105_mnifunc.tar
	# unzip preprocessed data
	tar -zxvf ./ds105_mnifunc.tar
	# rename folder:
	mv ds105 ds105_new
	# Move to data
	mv ds105_new /data
   
validate:
	python data/data.py

analysis:

report:
