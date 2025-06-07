docker build --no-cache -t patent-summary-api .
docker run -p 8000:80 patent-summary-api
