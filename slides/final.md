% Project Zeta Final Report
% Tzu-Chieh Chen, Edith Ho, Zubair Marediya, Mike Tran, Dongping Zhang
% December 3, 2015

# Background

## The Paper

- 'Distributed and Overlapping Representations of Faces and Objects in Ventral Temporal Cortex'
- from OpenFMRI.org
- ds105

## The Data

- 6 subjects
- 12 runs per subject
- 8 conditions per run: faces, houses, cats, scissors, bottles, chairs, scrambledpix, shoes

## The Method

- Linear regression (Lasso/Ridge/Elastic Net)
- T-tests
- Convolution
- Smoothing

# Initial work

## Our Hypothesis
- The differences of BOLD signals between different conditions are significant

## Exploratory Data Analysis

- Downloaded data
- Initial analysis: Sub001 Run001
- Identified and removed outliers (with functions from HW2)
- Attempted to test our hypothesis
- Convolution and prediction of BOLD signals
- Created design matrix for linear regression

## Identify outliers
![Outliers in sub001 run001](outlier.png "Outliers in sub001 run001")

## Task time course - Event related design
![Task time course](Task_time_course.png "Task time course")

## Convolution Graphs
![Predicted BOLD](stimulation_bold.png "BOLD prediction") 

## Design Matrix
- bottle, cat, chair, face, house, scissors, scrambledpix, shoe, drift1, drift2, ones
![Design Matrix](design_matrix.png "Design Matrix")

## Problems Faced

- Noise within original dataset, causing low-resolution brain images
- Drifting of BOLD signals
- Standardization of BOLD signals across different subjects for comparison
- Difficulty understanding the study and the dataset itself
- Hence only did analysis on one subject and one run so far

## Before And After Smoothing
- Background noise is high:
![House-Before smoothing](sub1_run1_house_before_smooth.png "house before smoothing")

## Before And After Smoothing
- Before Smoothing:
![Before Smoothing](before_smooth.png "Before Smooth")

## Before And After Smoothing
- Used smoothing techniques to create clearer and more meaningful images
![After Smoothing](after_smooth.png "After Smooth")

## Before And After Smoothing
- We can identify brain region specific for stimulation
![House-After smoothing](sub1_run1_house_after_smooth.png "house after smoothing")

## Before And After Smoothing
- Detail:
![House-After smoothing-detail](sub1_run1_house_detail.png "house detail")

## Masking
- wrote helper function to create masks for useful brain areas
- 80th percentile cutoff for intensities

## Affining
- took masked to voxel coordinates and tracked them through different runs
- helped us properly correlate intensities

## Correlation
- correlation between:
- run1 house vs run2 house = 
- run1 house vs run2 face = 
- run1 house vs run3 house = 0.82295125
- run1 house vs run3 face = 0.64401008
- run2 house vs run4 house = 0.52813216
- run2 house vs run4 face = 0.23481469

- all odds house vs all even face = -0.05986216
- all odd house vs all even house = 

## Time Series

