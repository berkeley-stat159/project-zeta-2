test:
	nosetests utils

coverage:
	nosetests utils --with-coverage --cover-package=utils

analysis:
	python linear_model_scripts_sub1.py
	python linear_model_scripts_sub2.py
	python linear_model_scripts_sub3.py
	python linear_model_scripts_sub4.py
	python linear_model_scripts_sub5.py
	python linear_model_scripts_sub6.py
	python correlation_analysis_scripts_sub1.py
	python correlation_analysis_scripts_sub2.py
	python correlation_analysis_scripts_sub3.py
	python correlation_analysis_scripts_sub4.py
	python correlation_analysis_scripts_sub5.py
	python correlation_analysis_scripts_sub6.py
	python cross_subject_analysis.py

regression:
	python linear_model_scripts_sub1.py
	python linear_model_scripts_sub2.py
	python linear_model_scripts_sub3.py
	python linear_model_scripts_sub4.py
	python linear_model_scripts_sub5.py
	python linear_model_scripts_sub6.py

correlation:
	python correlation_analysis_scripts_sub1.py
	python correlation_analysis_scripts_sub2.py
	python correlation_analysis_scripts_sub3.py
	python correlation_analysis_scripts_sub4.py
	python correlation_analysis_scripts_sub5.py
	python correlation_analysis_scripts_sub6.py
	python cross_subject_analysis.py

timeseries:
	python time_series_analysis.py
	python tsa_s2.py
	python tsa_s3.py
	python tsa_s4.py
	python tsa_s5.py
	python tsa_s6.py
	
all:
	test coverage analysis regression correlation timeseries
	
