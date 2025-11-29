#!/bin/bash
if [ "$1" = "work" ]; then
  git config user.name "felixwu"
  git config user.email "felixwu@sheinbpo.com"
  echo "Switched to WORK account"
else
  git config user.name "Lluo"
  git config user.email "lluo2020@163.com"
  echo "Switched to PERSONAL account"
fi