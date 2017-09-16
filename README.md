# Jingpai.co.uk

## Overview

## Prerequisites

- Python 3.6
- [Yarn](https://yarnpkg.com/en/docs/install)

## Install Node packages
```
yarn install
```
## Install requirements

### Development
```
pip install -r requirements/local
```

### Deployment
```
pip install -r requirements/production
```

### Test
```
pip install -r requirements/test
```

## Sync database
```
python manage.py migrate
```

## Show code quality report
```
make report
```

## Build static files for deployment
```
make build
```
