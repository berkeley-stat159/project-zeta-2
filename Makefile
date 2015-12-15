.PHONY: all structure data validate analysis figures 
		report clean test verbose coverage

all: clean coverage test data validate analysis report
	 cd code && make all
	 cd data && make all
	 cd paper && make all
	 cd proposal && make all
	 cd slides && make all

structure:
	cd data && make structure

data:
	cd data && make data
   
validate:
	cd data && make validate

analysis:
	cd code && make analysis
	cd code && make timeseries

figures: 
	cd paper && make figures

report:
	pdflatex -interaction=nonstopmode report.tex

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f
	cd paper && make clean
	cd proposal && make clean
	cd slides && make clean

test:
	nosetests code/utils/tests data
	cd code && make test

verbose:
	nosetests -v code/utils data
	cd code && nosetests -v utils

coverage:
	nosetests code/utils data --with-coverage --cover-package=data  --cover-package=utils
	cd code && make coverage
