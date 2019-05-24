@echo off
taskkill /F /IM taobao_list_page_job.py
set basedir=%cd%
echo %basedir%
set base_path=%basedir%
echo %base_path%
set job_path=%base_path%/taobao_list_page_job.bat
call %job_path%