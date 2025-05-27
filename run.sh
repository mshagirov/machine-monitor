#!/bin/bash

Help()
{
  # Display Help
  echo "Run API server at a given port (default port 8000)"
  echo
  echo "Usage: $0 [-p PORT] [-i HOST] [-b]"
  echo
  echo "Options:"
  echo "-h          Print this help" 
  echo "-b          Run in a background, must be used with '&', e.g. 'nohup ./run.sh -b &'"
  echo "-p <PORT>   Port number (int) to use instead of default 8000"
  echo "-i <HOST>   Host IP address, defaults to 0.0.0.0 (all interfaces)"
  echo 
  echo "NOTE: Don not forget to close the program when running in the background."
}

while getopts ":hp:i:b" option; do
  case $option in 
    h) #help
      Help
      exit
      ;;
    p) #port
      PORT=${OPTARG}
      ;;
    i) #host address
      HOST=${OPTARG}
      ;;
    b) #run in a background
      BACKGROUND="True"
      ;;
    *) #invalid options
      Help
      exit
      ;;
  esac
done

if [[ $PORT == "" ]]; then PORT=8000; fi

if [[ $HOST == "" ]]; then HOST="0.0.0.0"; fi

ParentPID=$$

echo "Parent=$ParentPID; HOST:PORT=$HOST:$PORT" > current_run.out

if [[ $BACKGROUND != "" ]] ; then
    nohup $0 -p ${PORT} -i ${HOST} >/dev/null 2>&1 &
else
    fastapi run --port $PORT --host $HOST mm/api.py
fi


