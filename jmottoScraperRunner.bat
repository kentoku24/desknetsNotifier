set HTTP_PROXY=http://localhost:3128
set HTTPS_PROXY=http://localhost:3128

cd /d %~dp0
C:\Python36\python.exe jmottoScraper.py %*
cd
pause