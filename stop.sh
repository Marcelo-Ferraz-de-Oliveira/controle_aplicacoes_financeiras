#/bin/bash
lsof -i :5000 | grep "5000" | awk '{print $2}' | xargs -r kill -9
lsof -i :3000 | grep "3000" | awk '{print $2}' | xargs -r kill -9
