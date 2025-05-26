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

if [[ "$#" -ne 1 ]]; then PORT=8000; fi

while getopts ":hp:" option; do
  case $option in 
    h) #help
      Help
      exit
      ;;
    p) #port
      PORT=${OPTARG}
      ;;
    *) #invalid options
      Help
      exit
      ;;
  esac
done

fastapi run --port $PORT mm/api.py
