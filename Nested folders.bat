@echo off&setlocal enabledelayedexpansion

::文件分类管理：按每1个文件装进一个文件夹整理。

echo;&echo;    开始整理……&echo;

set newf=0

set numf=0

set conf=0

if not exist New!newf! md New!newf!

for /f "tokens=*" %%a in ('dir /b /a-d') do (

    if !numf! geq 1 set numf=0&set /a newf+=1&md New!newf!

    if not "%%~na"=="%~n0" copy "%%~a" New!newf!&set /a numf+=1

    set /a conf=!newf!*1+!numf!

)

echo;&echo;    整理完成，共 !conf! 个文件，请注意检查！&pause>nul