docker build -t cortevaimage .
docker run -d --name cortevacontainer -p 80:80 cortevaimage