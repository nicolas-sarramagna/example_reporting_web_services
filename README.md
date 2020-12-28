# Example of usages of python FastAPI, scraping (sync & async mode) and unittest
## Subject : trends and charts about the market Bitcoin - USD

## Global usage :
See the main repo here : https://github.com/nicolas-sarramagna/example_reporting_main

## Local :

>export PYTHONPATH=.

>gunicorn example_reporting_web_services.app_ws:app --bind 0.0.0.0:50503 -w 1 -k uvicorn.workers.UvicornWorker


Endpoints : 
 - http://localhost:50503/api/v1/trend/indicator/investing
 - http://localhost:50503/api/v1/trend/indicator/tradingview (takes more time due to javascript async in the html page)
 - http://localhost:50503/api/v1/trend/chart/investtech/graph
 - http://localhost:50503/api/v1/trend/chart/investtech/rsi


## Docker :
Repo Docker Hub
https://hub.docker.com/r/sarramagna/example_reporting_web_services

Local : docker-compose up

Fix in progress for the url tradingview due to the usage of chrome with puppeteer on Docker mode

