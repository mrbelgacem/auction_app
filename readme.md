
## Required :
Install Docker Engine
Install Docker Compose

## Start verify Docker
$ systemctl start docker
$ systemctl status docker
$ docker run hello-world
$ docker container ls

## Start the Algorand sandbox with the default configuration

$ ./sandbox up -v testnet
$ ./sandbox logs
$ ./sandbox status  ( same as : $ ./sandbox goal node status )

## examples of how to interact with the environment:
$ ./sandbox test 

## Sandbox creates the following API endpoints:
algod:
    address: http://localhost:4001
    token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
kmd:
    address: http://localhost:4002
    token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
indexer:
    address: http://localhost:8980

## Available accounts
$ ./sandbox goal account list

## How to enter a Docker container to explore the files inside the container
$ ./sandbox enter algod   ( /opt/testnetwork/Node )
$ ls -la

## Configured address to which the Algod API is exposed
$ cat algod.net
[::]:4001
## Print the contents of the genesis file
$ cat genesis.json

## Setup Python environment (one time), activate Python virtual environment.
$ python3 -m venv venv
$ . venv/bin/activate

## Run application
$ python3 manage.py runserver

## Stop the Algorand sandbox 
$ ./sandbox down