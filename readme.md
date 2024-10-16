
# Travis
[![Build Status](https://app.travis-ci.com/deepjyotk/ebdjango.svg?token=DshHywy8DJZVn4vVJ5Hg&branch=main)](https://app.travis-ci.com/deepjyotk/ebdjango)

[![Coverage Status](https://coveralls.io/repos/github/deepjyotk/ebdjango/badge.svg)](https://coveralls.io/github/deepjyotk/ebdjango)

# Django App Deployment on AWS Elastic Beanstalk

Deployed Django Application: [http://django-env2.eba-j27d8ku3.us-west-2.elasticbeanstalk.com/polls/](http://django-env2.eba-j27d8ku3.us-west-2.elasticbeanstalk.com/polls/)

## Table of Contents

- [Travis](#travis)
- [Django App Deployment on AWS Elastic Beanstalk](#django-app-deployment-on-aws-elastic-beanstalk)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Prerequisites](#prerequisites)
  - [Setup Django Project](#setup-django-project)
  - [Prepare for AWS Elastic Beanstalk Deployment](#prepare-for-aws-elastic-beanstalk-deployment)
  - [Deploying to AWS Elastic Beanstalk](#deploying-to-aws-elastic-beanstalk)
  - [Post-Deployment Configuration](#post-deployment-configuration)
  - [Troubleshooting](#troubleshooting)
   
## Introduction

This guide will walk you through the steps to deploy a Django application to AWS Elastic Beanstalk. The live application can be accessed here: [Django Application](http://django-env.eba-uypr5ve5.us-west-2.elasticbeanstalk.com/).

## Prerequisites

Before deploying your Django app to Elastic Beanstalk, ensure the following are set up:

1. **AWS Account**: You must have an AWS account. If you don't have one, you can create it [here](https://aws.amazon.com/).
2. **AWS CLI**: Install and configure the AWS CLI by following the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
3. **EB CLI (Elastic Beanstalk CLI)**: Install the EB CLI by following the instructions [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html).
4. **Python & Django**: Install Python and set up your Django project locally. For guidance on installing Python, refer to [Python's installation page](https://www.python.org/downloads/).

## Setup Django Project

1. Create a new Django project (if you haven't already):

   ```bash
   django-admin startproject myproject
   cd myproject
   ```

2. Install all necessary Python packages and dependencies:

   ```bash
   pip install django gunicorn
   ```

3. Create a `requirements.txt` file:

   ```bash
   pip freeze > requirements.txt
   ```

## Prepare for AWS Elastic Beanstalk Deployment

1. **Modify `settings.py`**:
   - Replace the `SECRET_KEY` with environment variable handling:

     ```python
     import os
     SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-fallback-secret-key')
     ```

   - Set `ALLOWED_HOSTS` to include the Elastic Beanstalk domain:

     ```python
     ALLOWED_HOSTS = ['.elasticbeanstalk.com']
     ```

2. **Create a `.ebextensions` directory**:
   - Create a directory named `.ebextensions` in the root of your project.
   - Inside `.ebextensions`, create a file called `django.config` and add the following content to configure the Python environment and WSGI server:

     ```yaml
     option_settings:
       aws:elasticbeanstalk:container:python:
         WSGIPath: myproject.wsgi:application
     ```

3. **Ensure that a Procfile is created**:
   - In your project’s root directory, create a `Procfile` to tell Elastic Beanstalk to use `gunicorn` to run your Django app:

     ```bash
     web: gunicorn myproject.wsgi
     ```

4. **Initialize EB CLI**:
   - Run the following command to initialize Elastic Beanstalk within your project:

     ```bash
     eb init
     ```

   - Follow the prompts to configure the Elastic Beanstalk environment for your project.

## Deploying to AWS Elastic Beanstalk

1. **Create a New Elastic Beanstalk Environment**:
   - If you haven't already created an environment, run:

     ```bash
     eb create my-env-name
     ```

2. **Deploy the Django Application**:
   - Once the environment is created, deploy your app:

     ```bash
     eb deploy
     ```

   - After the deployment is complete, you can access the live application by running:

     ```bash
     eb open
     ```

   This will open the deployed application in your default browser.

## Post-Deployment Configuration

1. **Set Environment Variables**:
   - Set the `DJANGO_SECRET_KEY` and other required environment variables in the Elastic Beanstalk console:
     - Go to the **Elastic Beanstalk Console**.
     - Select your environment, then navigate to **Configuration** > **Software**.
     - Add the environment variables like `DJANGO_SECRET_KEY`.

2. **Static Files Configuration**:
   - Set up static file hosting by configuring your S3 bucket or storing static files on the Elastic Beanstalk instance.

   In `settings.py`, ensure:

   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')
   ```

   Afterward, run:

   ```bash
   python manage.py collectstatic
   ```

## Troubleshooting

- **Issue**: _"This branch does not have a default environment"._
  - **Solution**: Run `eb use my-env-name` to set the default environment.
  
- **Issue**: Application not loading or showing server errors.
  - **Solution**: Check the logs using `eb logs` or in the AWS Management Console.
  
- **Issue**: Static files not loading properly.
  - **Solution**: Ensure `collectstatic` has been run, and static files are served from the correct location (e.g., S3, Elastic Beanstalk).
