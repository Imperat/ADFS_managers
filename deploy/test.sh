#!/bin/bash
#run and del container after
if [ -z "$1" ]
   then
     echo "params <username> is empty"
   else
     docker run -it --rm --link postgres:postgres postgres psql -h postgres -U "$1"
fi
