# TEST SETTINGS
INSTALLED_APPS = (
    'djflocash',
    'django.contrib.contenttypes',
    'django.contrib.auth',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
SECRET_KEY = "NSRT89aieu/*-v+ST"


FLOCASH_MERCHANT = "test@merchant.com"
FLOCASH_MERCHANT_NAME = "test name"

ROOT_URLCONF = "djflocash.urls"
