import os

from django.core.management.utils import get_random_secret_key


def is_production_environment():
    """ Checks for the ENV enviroment variable and checks whether this is a
    production environment or not
    """
    ENVIRON_VAR_NAME = "ENV"
    # DEV_ENVIRONMENT = "DEV"
    PROD_ENVIRONMENT = "PROD"
    environment = os.environ.get(ENVIRON_VAR_NAME, None)
    if environment and environment == PROD_ENVIRONMENT:
        return True
    return False


def is_pythonanywhere():
    """ @brief Returns True the web app is hosted in pythonanywhere.com
    or returns None if the right environment variable is not set
    """
    pa_domain_var = 'PYTHONANYWHERE_DOMAIN'
    if os.getenv(pa_domain_var):
        return True
    return False


def get_pythonanywhere_hostname():
    """ @brief Extracts the hostname from a pythonanywhere env variable"""
    pa_hostname_var = 'HOST_NAME'

    # NOTE: What happens if HOST_NAME is not set?
    hostname = os.getenv(pa_hostname_var)
    if hostname:
        return hostname


def get_valid_hostnames():
    """ @brief Returns a list of valid hostnames for this Web app"""
    valid_hostnames = set()
    if is_pythonanywhere():
        hostname = get_pythonanywhere_hostname()
        valid_hostnames.add(hostname)

    return list(valid_hostnames)


def get_django_secret_key():
    """ @brief Retrieves Django's secrete key from the environment or
    generates a new key
    """
    secret_key_var = 'DJANGO_SECRET_KEY'

    secret_key = os.getenv(secret_key_var)
    if secret_key:
        return secret_key

    return get_random_secret_key()


def get_db_host():
    """ Retrieves the database's hostname """
    # TODO: Consider storiing the names of these
    # environment variables, inside constants
    # at the top of the script file.
    host = os.environ.get('DB_HOST')
    return host


def get_db_name():
    """ Retrieves the database's name """
    # TODO: Consider storiing the names of these
    # environment variables, inside constants
    # at the top of the script file.
    host = os.environ.get('DB_NAME')
    return host


def get_db_user():
    """ Retrieves the database's user """
    # TODO: Consider storiing the names of these
    # environment variables, inside constants
    # at the top of the script file.
    password = os.environ.get('DB_USER')
    return password 


def get_db_pass():
    """ Retrieves the database's password """
    # TODO: Consider storiing the names of these
    # environment variables, inside constants
    # at the top of the script file.
    password = os.environ.get('DB_PASS')
    return password 