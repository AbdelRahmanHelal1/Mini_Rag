Mini-rag

this app for learn implementation for rag model for question answer


## requiremets 

- python 3.12 or later

## install python using MiniConda

- Activate environment

## install the requirements packages
--> pip install -r requirements.text

# setup the env variable 

## change the file of  .env.example to .env and put your secrt keys

'''
$ cp .env.example .env
'''

## Run the fastapi server 

'''
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
'''

## postman Collection

install it and put into in assets floder
