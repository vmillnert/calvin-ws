# calvin-ws
Calvin workspace for the WASP Project Course


# How-to

For a complete list of Calvin commands, please take a look at their wiki :-)

## Start a runtime:

You can start a runtime with the commands:
```
csruntime --host localhost --port 5000 --controlport 5001 --name edge 
```

You can see the full API of the runtime by pointing web browser to
`localhost:5001`.

## Start metric-pusher:

You initialize metric-pusher together with the control-uri of the
runtime you wish to interact with: ``` python metric-pusher.py
localhost:5001 ```


## Start a web-interface

You can look at a web-interface of the runtime by starting `csweb.py`
and then pointing your web browser to `localhost:8000`.


## Deploy application

You can deploy an application (in this example `hello.calvin`) by running `cscontrol`:
```
cscontrol http://localhost:5001 deploy hello.calvin
```

You can also specify some requirements when deploying the applications, by adding `--reqs <requirements file>`:
```
cscontrol http://localhost:5001 deploy hello.calvin --reqs hello.deployjson
```
