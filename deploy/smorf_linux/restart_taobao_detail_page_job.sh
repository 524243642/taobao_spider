#!/usr/bin/env bash
ps aux | grep 'taobao_detail_page_job.py' | awk -F" " '{print $2}' | xargs kill -9
basedir=`pwd -P`
echo $basedir
base_path=$basedir
job_path=$base_path/taobao_detail_page_job.sh
nohup $job_path &> /dev/null &