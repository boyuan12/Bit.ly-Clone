# Bit.ly Clone API

**BASE_URL = http://0.0.0.0:1234**

This is a REST API and all response will return in JSON. If an error occured, there will be a code and error key to describe what happened

200 - OK
400 - Error
500 - Internal Server Error
502 - Under Mainteance

## GET /api?custom=

**Check whether a given custom code already exist in our database or not**

Return **200**, otherwise will return 400.

## GET /api?url=

**Create a new shortened URL by generating random 7 digits alphanumeric characters**

Return **200** with url key, otherwise will return 400 if the URL is not valid

## GET /api?url=&custom=

**Create a new shortened URL by user's given code**

Return **200** with url key, otherwise will return 400 if the URL is not valid, or the custom code is not valid