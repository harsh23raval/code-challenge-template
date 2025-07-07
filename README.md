# Code Challenge Template

Please reference the text files in "answers" directory for :
1. Steps to execute this project locally.
   - Ref: "projectExecution.txt"
2. Aproach to consider for running this project on AWS. 
   - Ref: "deployment.txt"
3. the SQL queries which were used within this project for creating the data model and loading data into those model schemas.
    - Ref: "queries.txt"


Swagger_endpoints documentation:

1. /api/weather
Sample request : 
{
  "station_id": "USC00110072",
  "date": "1985-01-01",
  "page": 1
}
Sample Response : 
{
  "total_results": 1,
  "total_pages": 1,
  "current_page": 1,
  "results_per_page": 25,
  "results": [
    {
      "station_id": "USC00110072",
      "date": "1985-01-01",
      "max_temp": -22,
      "min_temp": -128,
      "precipitation": 94
    }
  ],
  "errorMessage": "None"
}

2. /api/weather/stats
Sample Request:
{
  "station_id": "USC00110072",
  "year": 1995,
  "page": 1
}
Sample Response:
{
  "total_results": 1,
  "total_pages": 1,
  "current_page": 1,
  "results_per_page": 25,
  "results": [
    {
      "station_id": "USC00110072",
      "year": 1995,
      "avg_max_temp_celsius": 15.044,
      "avg_min_temp_celsius": 3.714,
      "total_precipitation": 78.72
    }
  ],
  "errorMessage": "None"
}

Error Handling has been implemented, if an invalid request is passed such as if year is less than 1900 then the errorMessage will be populated accordingly.

unit tests can be found if you navigate to src/test_main.py