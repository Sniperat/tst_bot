# tst_bot

git clone 'link'

### create venv
> python -m venv 'venv name'

### use venv
windows:
>.  'venv name'.Script.activate

linux:
>.  'venv name'.bin.activate

### install packages
>pip install -r requirements.txt

### create database
>python manage.py makemigrations 

>python manage.py migrate

### create super user
>python manage.py createsuperuser

### to run project you need to create '.env' file inside 'config' folder and write this:
>SECRET_KEY=

>DEBUG=

>BOT_TOKEN=

### and fill values

### after this we need to set telegram webhook to our domen, and must have ssl
### like this 

>https://api.telegram.org/bot{"YOUR TOKEN}/setWebhook?url=https://{"YOUR DOMAIN"}/

### I recomended you to use ngrock to temporary ssl domain

### finally 
>python manage.py runserver

# good luck