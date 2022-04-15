# JSON parsing with BSPump library

## Description:
Python script for parsing and extracting data from a JSON file, and writing final output to the specified DB, in this case, MongoDB is used as a final data sink.

## Libraries used
The script takes an advantage of the [BitSwan Pump: A real-time stream processor for Python 3.5+](https://github.com/LibertyAces/BitSwanPump), for parsing, processing, and outputting the file, each of the processes is modular and could be replaced with a different source/processor/sink module.

## Docker containers
Python script and MongoDB database instance are packaged as two docker containers. Dockerfile for the script is provided and uses conda env to manage dependencies. MongoDB image uses MongoDB version 5.0 as specified in the docker-compose.yml file.


## How to run a script
To run a script you need to have a `docker` and `docker-compose` installed on your target system. 
1. On a Linux system: `make run` or `docker-compose up -d`
2. On a Windows system: `docker-compose up -d` or `make run` if you have `make` installed (e.g. with chocolatey package manager).
