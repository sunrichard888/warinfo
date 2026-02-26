#!/bin/bash
# Daily warinfo update script for cron

cd /root/.openclaw/workspace/warinfo
python3 update_daily.py >> /var/log/warinfo_update.log 2>&1