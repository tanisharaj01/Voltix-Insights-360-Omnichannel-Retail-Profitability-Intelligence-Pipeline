@echo off
echo Starting Data Pipeline...

echo.
echo Running unit tests...
python -m pytest tests/
if %ERRORLEVEL% NEQ 0 (
    echo Tests failed. Stopping pipeline.
    exit /b %ERRORLEVEL%
)

echo.
echo Cleaning data...
python src/clean_data.py
if %ERRORLEVEL% NEQ 0 (
    echo Data cleaning failed. Stopping pipeline.
    exit /b %ERRORLEVEL%
)

echo.
echo Analyzing sales...
python src/analyze_sales.py
if %ERRORLEVEL% NEQ 0 (
    echo Sales analysis failed. Stopping pipeline.
    exit /b %ERRORLEVEL%
)

echo.
echo Pipeline completed successfully!
pause
