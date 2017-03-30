# Minimum microservice structure

A Minimum structure featuring:

* Docker using Slim Debian
* Python 3.6
* Earth Engine Python API, and authorisation set-up
* Flask and Flask_restplus
* Working skeleton of a Flask App with Swagger UI interface

#### Launch

1) Ensure you have execution permissions set for the start.sh and entrypoint.sh files:


```bash
chown +x start.sh
chown +x entrypoint.sh
```

2) Run the `start.sh` script:
```bash
./start.sh develop
```
The microservice should now be accessible at `localhost:8000`

#### Interactive docker session

If you wish to enter the container in interactive mode, identify the `CONTAINER ID` using `docker ps`, e.g.:

```bash
docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                    NAMES
ea58c240878c        dockertest_develop   "./entrypoint.sh d..."   19 minutes ago      Up 19 minutes       0.0.0.0:8000->5000/tcp   dockertest_develop_1
```

Then use the id to run `docker exec`:

```
docker exec -it ea58c240878c bash
```

### Environment variables

* DEBUG= Boolean
* PORT= port that flask app will try and run on e.g. 5000
* EE_USER= Earth Engine user account info
* EE_PRIVATE_KEY=Earth engine private key from which to generate a PEM
* EE_AUTH_TYPE=nonlocal (set to local if you want to authenticte via locally stored Earth Engine credentials)
