# Example of usages of python FastAPI, scraping (sync & async mode) and unittest
## Subject : trends and charts about the market Bitcoin - USD

## Global usage :
See the main repo here : https://github.com/nicolas-sarramagna/example_reporting_main

## Local :

### with source code
1. get the source code of the project

2.
*without docker* : in a terminal, type **uvicorn example_reporting_web_services.app_ws:app**

or

*with docker* : in a terminal, type **docker-compose up**

3.
Endpoints wuthout docker
 - GET http://localhost:8000/api/v1/trend/indicator/investing -> json
 - GET http://localhost:8000/api/v1/trend/indicator/tradingview -> json (takes more time due to javascript async in the html page)
 - GET http://localhost:8000/api/v1/trend/chart/investtech/graph -> image png
 - GET http://localhost:8000/api/v1/trend/chart/investtech/rsi -> image png

With docker, the port is 10503 (defined in the file docker-compose.yml)

### without source code i.e with image Docker :
Image repo Docker Hub : https://hub.docker.com/r/sarramagna/example_reporting_web_services

1. get the file [prod.yml](https://github.com/nicolas-sarramagna/example_reporting_web_services/blob/main/prod.yml)
2. in a terminal, type  **docker-compose up -f prod.yml up**
3. Endpoints on port 20503 (defined in prod.yml)


