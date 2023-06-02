@echo off
set PGPASSWORD=postgres45
echo.
echo.
echo Pay attention Database cashregister is being removed!!!
echo.
echo.
echo Press a key to remove!
echo.
echo.
echo or press Ctrl+C to abort
pause > nul

"C:\ProgramData\postgresql\bin\dropdb.exe"  -h localhost -p 5432 -U postgres  -w cashregister
echo.
echo.
echo.
echo.
echo Database cashregister is removed.
echo.
echo.
echo.
echo Press a key for ending program .........
pause > nul
