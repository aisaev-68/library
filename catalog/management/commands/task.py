from mimesis import Text, Person, Numeric, Internet, Code, Gender, Datetime
from mimesis.locales import Locale
import requests

internet = Internet()


url = internet.stock_image_url(width=800, height=600)
request = requests.get(url)

print(request.status_code)