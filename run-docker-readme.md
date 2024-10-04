### Steps to run the docker image locally

1. Clone the repository
2. Ensure you have docker installed and running on your machine. If you don't have docker installed, you can download it from [here](https://docs.docker.com/get-docker/).
3. Run the following command to build the docker image
```bash
docker build -t <image-name> .
```
Note that the image name can be anything you want to name the image. For example, `docker build -t my-image .`
4. Run the following command to run the docker image
```bash
docker run -p 8081:8080 -it <image-name>
```
5. Open your browser and navigate to `http://localhost:8081` to view the application.