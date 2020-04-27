
import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://www.worldometers.info/coronavirus/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
data = []
table = soup.find('table')
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele if ele else '0' for ele in cols]) # Get rid of empty values

import pandas as pd
dftable = pd.DataFrame(data)
print(dftable.to_string())
