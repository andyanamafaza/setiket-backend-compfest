import requests
import random
endpoint = 'http://localhost:5001/api/ticket/create/'
category = [{
    'relawan':random.randint(1000,10_000_000),
    'paid':random.randint(1000,10_000_000),
    'free':random.randint(1000,10_000_000)
}]