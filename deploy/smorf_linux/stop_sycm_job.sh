#!/usr/bin/env bash
ps aux | grep 'sycm_job.py' | awk -F" " '{print $2}' | xargs kill -9