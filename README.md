# example_reporting_web_services


Local :

>export PYTHONPATH=.

>python example_reporting_web_services/app_ws.py

http://localhost:50503/api/v1/trend/indicator/investing

http://localhost:50503/api/v1/trend/indicator/tradingview (takes more time due to javascript async in the html page)

http://localhost:50503/api/v1/trend/chart/investtech/graph

http://localhost:50503/api/v1/trend/chart/investtech/rsi


Docker :
Repo Docker Hub
https://hub.docker.com/r/sarramagna/example_reporting_web_services

Fix in progress for the url tradingview due to the usage of chrome with puppeteer on Docker mode

