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

## Linear regression again
- betas for Sub001-Run001-bottle
![Sub001-Run00-bottle](betas_for_sub001_run001-bottle.png "Sub1-Run1-Bottle")

## Linear regression again                                                      
- betas for Sub001-Run001-cat                                                
![Sub001-Run00-cat](betas_for_sub001_run001-cat.png "Sub1-Run1-Cat") 

## Linear regression again                                                      
- betas for Sub001-Run001-chair                                                
![Sub001-Run00-chair](betas_for_sub001_run001-chair.png "Sub1-Run1-Chair") 

## Linear regression again                                                      
- betas for Sub001-Run001-face                                                
![Sub001-Run00-face](betas_for_sub001_run001-face.png "Sub1-Run1-Face") 

## Linear regression again                                                      
- betas for Sub001-Run001-house                                                
![Sub001-Run00-house](betas_for_sub001_run001-house.png "Sub1-Run1-House") 

## Linear regression again                                                      
- betas for Sub001-Run001-scissors                                                
![Sub001-Run00-scissors](betas_for_sub001_run001-scissors.png "Sub1-Run1-Scissors") 

## Linear regression again                                                      
- betas for Sub001-Run001-scrambledpix                                                
![Sub001-Run00-scrambledpix](betas_for_sub001_run001-scrambledpix.png "Sub1-Run1-Scrambledpix") 

## Linear regression again                                                      
- betas for Sub001-Run001-shoe                                                
![Sub001-Run00-shoe](betas_for_sub001_run001-shoe.png "Sub1-Run1-Shoe") 

## Focusing on most response area
- Example: Run1-House
![Run1 House](run1_house.png "Run1 House")

## Focusing on most response area (cont.)                                              
- Example: Run2-House    
![Run2 House](run2_house.png "Run2 House") 

## Focusing on most response area (cont.)                                           
- Example: Run2-Face    
![Run2 Face](run2_face.png "Run2 Face") 

## Correlation                                                                  
- correlation between:                                                          
- run1 house vs run2 house = 0.50060026                                         
- run1 house vs run2 face  = 0.76080714     

## Correlation
- correlation between:
- run1 house vs run2 house = 0.50060026
- run1 house vs run2 face  = 0.76080714
- run1 house vs run3 house = 0.82295125
- run1 house vs run3 face  = 0.64401008
- run2 house vs run4 house = 0.52813216
- run2 house vs run4 face  = 0.23481469

## Make average for odd runs and even runs
- Odd-House:
![Odd House](odd_house.png "Odd House")

## Make average for odd runs and even runs (cont.)                                     
- Even-House:                                
![Even House](even_house.png "Even House")

## Make average for odd runs and even runs (cont.)                              
- Face:                                                                        
![Odd Face](odd_face.png "Odd Face") 

## Make average for odd runs and even runs (cont.)                              
- Even-House:                                        
![Even Face](even_face.png "Even Face")                                      
                                            
## Correlation
- correlation between:
- all odds house vs all even face = -0.05986216
- all odd house vs all even house = 1.00000

- correlation highest when comparing same object

## Affining                                                                     
- took masked to voxel coordinates and tracked them through different runs      
- helped us properly correlate intensities      

## Time Series
- ARIMA model, parameters = 1.70360618, -0.05272599, -0.53091966, 1.06627208, 0.63106367
![ACF and PACF](sub001_run001_corrFunc.png "ACF and PACF")

## Time Series (cont.)
- ACF and PACF:
![Residual ACF and PACF](sub001_run001_residcorrFunc.png "Residuals ACF and PACF")

## Time Series (cont.)
- Residual Plot
![Residual Plot](sub001_run001_residFit.png "Residuals Plot")

## Time Series (cont.)
- Actual vs. Fitted
![Actual vs. Fitted](sub001_run001_TimeSeries.png "Actual vs. Fitted")

