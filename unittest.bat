:: ------------- Unittest + coverage --------------------------------------
nosetests --with-coverage --cover-package=src --cover-erase --cover-inclusive
pause

:: ------------- Pylint ---------------------------------------------------
pylint test
cd src
pylint src
cd..
pause
