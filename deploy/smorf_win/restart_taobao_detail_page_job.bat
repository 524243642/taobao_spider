@echo off
taskkill /F /IM taobao_detail_page_job.py
set basedir=%cd%
echo %basedir%
set base_path=%basedir%
echo %base_path%
set job_path=%base_path%/taobao_detail_page_job.bat
call %job_path%
