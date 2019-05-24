#!/usr/bin/env bash
ps aux | grep 'taobao_list_page_job.py' | awk -F" " '{print $2}' | xargs kill -9