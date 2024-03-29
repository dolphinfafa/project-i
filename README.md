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

## Build static files for development

make new directory 'tmp' under root and 'cache' under /tmp

```
make build
```

## Build static files for deployment
```
make build-prod
```

## Environment variables for deployment
```
$DJANGO_SECRET_KEY     Random String
$PYFFX_KEY             Random String
$GOOGLE_MAPS_API_KEY   Google Maps Javascript API Key
$JING_STATIC_DIR       Static Diretory Path
$JING_MEDIA_DIR        Media Diretory Path
```
