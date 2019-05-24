#!/usr/bin/env bash
basedir=`pwd -P`
echo $basedir
base_path=$basedir/../../../
env_path=$base_path/local_python3_virtualenv
source $env_path/bin/activate
project_path=$base_path./mall_spider/
echo $project_path
cd $project_path
export PYTHONPATH=$PYTHONPATH:$project_path
job_path=$project_path./mall_spider/job/sycm_job.py
echo $job_path
python $job_path --env dev
