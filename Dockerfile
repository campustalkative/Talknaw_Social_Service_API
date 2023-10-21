FROM python:3.10-slim

# Update the package list and install libmagic for python-magic and cloudinary
RUN apt-get update && apt-get install -y libmagic1

WORKDIR /app


ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.dev.txt requirements.txt


RUN pip install -r requirements.txt  


COPY . .

# ARG SECRET_KEY
# ARG TREBLLE_API_KEY
# ARG TREBLLE_PROJECT_ID
# ARG OPENAI_API_KEY
# ARG DEBUG
# ARG DATABASE_URL
# ARG STRIPE_SECRET_KEY
# ARG DJANGO_SETTINGS_MODULE
# ARG PGDATABASE
# ARG PGUSER
# ARG PGPASSWORD
# ARG PGPORT
# ARG PGHOST

# # Set the ENV variables using the ARG values
# ENV SECRET_KEY=$SECRET_KEY
# ENV TREBLLE_API_KEY=$TREBLLE_API_KEY
# ENV TREBLLE_PROJECT_ID=$TREBLLE_PROJECT_ID
# ENV OPENAI_API_KEY=$OPENAI_API_KEY
# ENV DEBUG=$DEBUG
# ENV DATABASE_URL=$DATABASE_URL
# ENV STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
# ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-SymplyFinance.settings}
# ENV PGDATABASE=$PGDATABASE
# ENV PGUSER=$PGUSER
# ENV PGPASSWORD=$PGPASSWORD
# ENV PGPORT=$PGPORT
# ENV PGHOST=$PGHOST

RUN python3  manage.py collectstatic --no-input

RUN python3 manage.py migrate

EXPOSE 8000


CMD ["gunicorn", "--bind", ":8000","Talknaw.wsgi:application"]
# CMD [ "python3", "manage.py", "runserver" ] 


