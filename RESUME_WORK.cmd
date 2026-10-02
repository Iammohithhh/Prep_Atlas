@echo off
if exist "%~dp0build\PAUSE" del "%~dp0build\PAUSE"
echo Pause flag removed. Claude resumes the workers at its next check, or tell it 'resume'.
pause
