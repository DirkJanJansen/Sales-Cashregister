@echo off
set PGPASSWORD=postgres45
echo.
echo.
echo LET OP Database bisystem wordt verwijderd!!!
echo.
echo.
echo Druk een toets om database cashregister te verwijderen
echo.
echo.
echo of druk Ctrl+C om te annuleren
pause > nul

"C:\ProgramData\postgres\bin\dropdb.exe"  -h localhost -p 5432 -U postgres  -w cashregister
echo.
echo.
echo.
echo.
echo Database cashregister is verwijderd.
echo.
echo.
echo.
echo Druk een toets voor einde programma .........
pause > nul
