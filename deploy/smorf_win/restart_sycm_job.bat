@echo off
taskkill /F /IM sycm_job.py
set basedir=%cd%
echo %basedir%
set base_path=%basedir%
echo %base_path%
set job_path=%base_path%/sycm_job.bat
call %job_path%