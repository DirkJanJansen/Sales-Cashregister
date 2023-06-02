@echo off

set PGPASSWORD=postgres45

echo.
echo.
echo.
echo Press a key to backup database cashregister.
pause > nul
echo.
"C:\ProgramData\Postgres\bin\pg_dump.exe" -U postgres -v --verbose -d  cashregister -Fc -f  "D:\Sales\Installation\cashregister.backup"
echo.
echo.
echo Backup of database cashregister is done.
echo.
echo Press a key to exit.
pause > nul
#-Fp Plain
#-Fc Custom
#-Fd directory
#-Ft tar
