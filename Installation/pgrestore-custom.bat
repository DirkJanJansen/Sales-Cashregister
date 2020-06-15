@echo off

set PGPASSWORD=postgres45


echo.
echo.
echo.
echo. 
echo Verwijder eerst met pgdrop-cashregister.bat de database
echo als dit nog niet is gedaan
echo.
echo.
echo U gaat nu de database cashregister.backup terugplaatsen
echo Druk een toets voor terugplaatsen database cashregister ........
echo.
echo of druk CTRL+C om te annuleren
echo.
pause > nul
echo.
echo.
echo Restore database bisystem via cashregister.backup
echo.
echo.
echo.
"C:\ProgramData\postgres\bin\createdb.exe" -h  localhost -p 5432 -U postgres -w cashregister 
"C:\ProgramData\postgres\bin\pg_restore.exe" --dbname=cashregister  --verbose "C:\ProgramData\Sales\Installation\cashregister.backup"
echo.
echo Database cashregister is teruggeplaatst!
echo.
echo Druk een toets voor einde programma .........
pause > nul
