# Project Zeta 

Statistics 159/259: Reproducible and Collaborative Statistical Data Science

UC Berkeley | Fall 2015

[![Build Status](https://travis-ci.org/berkeley-stat159/project-zeta.svg?branch=master)](https://travis-ci.org/berkeley-stat159/project-zeta?branch=master)
[![Coverage Status](https://coveralls.io/repos/berkeley-stat159/project-zeta/badge.svg?branch=master)](https://coveralls.io/r/berkeley-stat159/project-zeta?branch=master)

## About This Repository
This repository contains our analysis and documentations of the visual object recognition data from OpenfMRI. Our main goal is to first test the reproducibility of their study results, then add additional statistical analysis for further insights.

## Our Data
Detailed descriptions of the data can be found at [ds105_old](https://openfmri.org/dataset/ds000105/). This link leads to the first dataset that gets downloaded above. For a cleaner, processed version, which was the second dataset, please check out the following:
[ds105_new](https://nipy.bic.berkeley.edu/rcsds/ds105/). Please read above for download sizes and times. 

## Roadmap

### Main Commands

Please run the following commands in their respective order from the root of the project folder. This will set you up to follow our project. There may be additional Makefiles in subdirectories but they are all wrapped in the one within the root. 

* <code>git clone https://github.com/berkeley-stat159/project-zeta.git</code>: This will clone our repo to you locally. The clone process should be quite short.

* <code>make structure</code>: This creates the directory skeleton necessary for our project.

* <code>make data</code>: This downloads two datasets. Their sizes are 2GB and 12.5GB respectively. Both are needed to complete our analysis, so please ensure there is sufficient space on your computer to download the data. Please ensure that you have a stable
internet connection during the download.

* <code>make validate</code>: This validates that the datasets were downloaded correctly. It will check for appropriate hash values.

* <code>make analysis</code>: This will run all the statistical analysis of our study. All models and figures will be generated from this command. Ensure you have enough memory. The process will take about 60 to 80 minutes to finish. 

* <code>make figures</code>: This will copy all the figures generated above, into their appropriate directories. This is crucial in order to generate the report.

* <code>make report</code>: This will generate the pdf of our final report. This includes detailed write-ups for our analysis and corresponding graphs. You must have LaTeX installed.  

### Additional Commands

Here are some other commands you will find helpful. 

* <code>make all</code>: Runs all commands over our entire project. This will run all the steps above, and then will clean all trash files at the end.

* <code>make clean</code>: Will clean all compiled .pyc and other unnecessary files throughout the project directory. 

* <code>make test</code>: Will run all our tests of the data and our scripts.

* <code>make verbose</code>: Does the same as above, except as 'verbose', giving more information.

* <code>make coverage</code>: Generates a coverage report for the functions in the <code>code</code> and <code>data</code> directories.

## Contributers
Tzu-Chieh Chen [tcchenbtx](https://github.com/tcchenbtx)

Edith Ho [edithhcw](https://github.com/edithhcw)

Zubair Marediya [Zubair-Marediya](https://github.com/Zubair-Marediya)

Michael Tran [miketranx4](https://github.com/miketranx4)

Dongping Zhang [dpzhang](https://github.com/dpzhang)

**A big thank you to Jarrod Millman, Matthew Brett, J-B Poline, and Ross Barnowski for your teaching and advice throughout the semester.**
