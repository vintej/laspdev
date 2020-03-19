## Create Containers for NodeA and NodeB
Build image using the Dockerfile and run the containers:
```
$ docker build -t laspvina .
$ docker build -t laspvinb .
$ docker run -ti --name laspvinA laspvina
$ docker run -ti --name laspvinB laspvinb
```
