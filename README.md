# compliance-bot-assignment
## Problem Statement

The task is to build an API that does the following:

- Take a webpage as the input and it has to check the content in the page against a compliance policy
- Return the findings (non-compliant results) in the response


## Instructions to Start usage

```
# clone the repository:
git clone https://github.com/sounritesh/compliance-bot.git

# change directory to the repository root
cd compliance-bot

# create a .env file
touch .env

# paste your open ai api key as OPENAI_API_KEY
```

### Setup and Installation

#### Setup using virtualenv

```
# create a virtual environment, make sure you have Python>=3.9.2
python3 -m virtualenv botenv

# activate the virtual environment
source botenv/bin/activate

# install and setup requirements
pip install -e .
```

#### Setup using Docker

```
# build docker image
# for mac
docker build --platform=linux/arm64 -t compliance-bot .

# for linux
docker build -t compliance-bot .

# run the docker image as a container
docker run -it --rm -p 80:80 -t compliance-bot
```

### Usage

```
# make a post call to /inference/ endpoint with a body containing the webpage url
# { "url": "page_url" }
curl -H 'Content-Type: application/json' \
      -d '{ "url": "https://www.joinguava.com/"}' \
      -X POST http://0.0.0.0:80/inference/

```
