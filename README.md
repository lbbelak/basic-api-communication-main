# Basic api communication

Basic python api designed to communicate with public api

## Getting started

    docker build -t myimage .

    docker run --name mycontainer -p 8000:8000 myimage

or
    
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    
CMC key is limited to 300 credits a day. 
