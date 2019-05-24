@echo off
title taobao_list_page_job
set basedir=%cd%
echo %basedir%
set base_path=%basedir%/../../../
echo %base_path%
set env_path=%base_path%/local_python3_virtualenv
echo %env_path%
call %env_path%/Scripts/activate
set project_path=%base_path%./mall_spider/
echo %project_path%
cd %project_path%
set PYTHONPATH=%PYTHONPATH%;%project_path%
set job_path=%project_path%./mall_spider/job/taobao_list_page_job.py
echo %job_path%
python %job_path% --env dev
