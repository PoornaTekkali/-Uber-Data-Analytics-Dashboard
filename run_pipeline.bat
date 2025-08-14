@echo off
REM ------------------------------------------
REM Uber Data Analytics Pipeline Execution
REM ------------------------------------------

REM Set Python path if not in PATH already
REM set PATH=C:\Users\poorn\AppData\Local\Programs\Python\Python310\Scripts;%PATH%

echo Running Data Cleaning...
python data_cleaning.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR in data_cleaning.py
    pause
    exit /b %ERRORLEVEL%
)

echo Running Data Transformation...
python data_transformation.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR in data_transformation.py
    pause
    exit /b %ERRORLEVEL%
)

echo Running Data Analysis...
python data_analysis.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR in data_analysis.py
    pause
    exit /b %ERRORLEVEL%
)

echo Storing Data to SQLite...
python uber_store_db.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR in uber_store_db.py
    pause
    exit /b %ERRORLEVEL%
)

echo Running Visualizations...
python uber_visualization.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR in uber_visualization.py
    pause
    exit /b %ERRORLEVEL%
)

echo Running ML Predictions...
python uber_ml_prediction.py
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR in uber_ml_prediction.py
    pause
    exit /b %ERRORLEVEL%
)

echo ------------------------------------------
echo PIPELINE COMPLETED SUCCESSFULLY
pause
