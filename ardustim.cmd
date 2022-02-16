:: Check if Miniconda is present
IF EXIST %USERPROFILE%\miniconda3\Scripts\activate.bat (
    set conda_file=%USERPROFILE%\miniconda3
) ELSE (
	IF EXIST %USERPROFILE%\anaconda3\Scripts\activate.bat (
    	set conda_file=%USERPROFILE%\anaconda3
)
)

:: enter conda
call %conda_file%\Scripts\activate.bat

:: Navigate sake-plan directory
cd %USERPROFILE%\Documents\GitHub\ardustim

:: Check if environment exists
IF NOT EXIST %conda_file%\envs\ardustim\python.exe (
    conda env create -f environment.yml
)

:: Activate conda environment
call activate ardustim

:: Launch app
python ardu_stim.py

TIMEOUT 10