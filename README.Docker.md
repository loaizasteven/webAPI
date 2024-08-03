### Building and running your application

To compose and build up your application you can following the provided structure in the file `docker-compose.yml`. In this file we send an env variable securely in transit, via encryption, to the docker container. The command below will build the image and run the container, add `-d` to have it detached and run in the background.

`docker compose up --build`.

Your application will be available at http://localhost:80/docs.

### Otherwise (This repo uses this method)

First, build your image, e.g.: `docker build -t fastapiimage .`, then run your container `docker run -d --name fastapicontainer -p 80:80 fastapiimage`. 

If you container exists, you will need to stop and remove it. \
- `docker stop fastapicontainer`
- `docker rm fastapicontianer`

### Bash Shortcuts
Run the following to build you docker image/container in one line:
```bash 
source api_script && docker_build
```

### References
* [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi)
* [Docker's Python guide](https://docs.docker.com/language/python/)