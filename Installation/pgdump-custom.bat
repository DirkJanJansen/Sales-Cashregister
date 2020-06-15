@echo off

set PGPASSWORD=postgres45

echo.
echo.
echo.
echo Druk op een toets om een backup te maken van de database cashregister.
pause > nul
echo.
"C:\ProgramData\Postgres\bin\pg_dump.exe" -U postgres -v --verbose -d  cashregister -Fc -f  "C:\ProgramData\Sales\Backup\cashregister.backup"
echo.
echo.
echo Backup van de database cashregister is gemaakt.
echo.
echo Druk een toets om af te sluiten.
pause > nul
#-Fp Plain
#-Fc Custom
#-Fd directory
#-Ft tar