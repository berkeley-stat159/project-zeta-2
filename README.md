# Project Zeta 

Statistics 159/259: Reproducible and Collaborative Statistical Data Science

UC Berkeley | Fall 2015

[![Build Status](https://travis-ci.org/berkeley-stat159/project-zeta.svg?branch=master)](https://travis-ci.org/berkeley-stat159/project-zeta?branch=master)
[![Coverage Status](https://coveralls.io/repos/berkeley-stat159/project-zeta/badge.svg?branch=master)](https://coveralls.io/r/berkeley-stat159/project-zeta?branch=master)

## About This Repository
This repository contains our analysis and documentations of the visual object recognition data from OpenfMRI. Our main goal is to first test the reproducibility of their study results, then add additional statistical analysis for further insights.

## Our Data
Detailed descriptions of the data can be found at [ds00105](https://openfmri.org/dataset/ds000105/).

Use 'make data' to download the raw and preprocessed data, which are 2GB and 12.5GB in size respectively. Both are needed to complete our analysis, so please ensure there is sufficient space on your computer to download the data. 

After downloading the data, you can use 'make validate' to validate it. 

## Our Code
First, run 'make clean' to clean up the data as preparation for analysis.

To runs our scripts for data analysis and generates figures, use the 'make analysis' command. This might take up quite some time and disk space, since the data is large in size. 

'make test' runs all tests and 'make coverage' generates a the coverage report for this repository.

## Our Report
Use 'make report' to produce our the pdf file for our final report, which includes detailed write-ups for our analysis and corresponding graphs.

## Contributers
Tzu-Chieh Chen [tcchenbtx](https://github.com/tcchenbtx)

Edith Ho [edithhcw](https://github.com/edithhcw)

Zubair Marediya [Zubair-Marediya](https://github.com/Zubair-Marediya)

Michael Tran [miketranx4](https://github.com/miketranx4)

Dongping Zhang [dpzhang](https://github.com/dpzhang)

**A big thank you to Jarrod Millman, Matthew Brett, J-B Poline, and Ross Barnowski for your teaching and advice throughout the semester.**
