#!/bin/bash
echo $SSH_PUBLIC_KEY > ~/.ssh/authorized_keys
source venv/bin/activate
/etc/init.d/ssh start
exec gunicorn -b :5000 --access-logfile - --error-logfile - app:app