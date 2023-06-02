@echo off

set PGPASSWORD=postgres45


echo.
echo.
echo.
echo. 
echo Remove first with pgdrop-cashregister.bat database if already exist
echo 
echo.
echo.
echo You are going to replace database cashregister.
echo Press a key to restore ........
echo.
echo or press CTRL+C to cancel
echo.
pause > nul
echo.
echo.
echo Restore database cashregister by cashregister.backup
echo.
echo.
echo.
"C:\ProgramData\postgresql\bin\createdb.exe" -h  localhost -p 5432 -U postgres -w cashregister 
"C:\ProgramData\postgresql\bin\pg_restore.exe" --dbname=cashregister  --verbose "C:\ProgramData\Sales\Installation\cashregister.backup"
echo.
echo Database cashregister is restored!
echo.
echo Press any key for ending this program .........
pause > nul
