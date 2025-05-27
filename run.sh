#!/bin/bash

Help()
{
  # Display Help
  echo "Run API server at a given port (default port 8000)"
  echo ""
  echo "Usage: $0 [-p PORT]"
  echo "options:"
  echo "-h           Print this help." 
  echo "-p <PORT>   Port number (int) to use instead of default 8000"
}

# if [[ "$#" -lt 1 ]]; then PORT=8000; fi

while getopts ":hp:i:" option; do
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
    *) #invalid options
      Help
      exit
      ;;
  esac
done

if [[ $PORT == "" ]]; then PORT=8000; fi

if [[ $HOST == "" ]]; then HOST="0.0.0.0"; fi

echo HOST:PORT = $HOST:$PORT

fastapi run --port $PORT --host $HOST mm/api.py
