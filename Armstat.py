# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# import time



# service = Service(executable_path = 'chromedriver.exe')
# driver = webdriver.Chrome(service = service)

# driver.get("https://armstat.am/am/?nid=12&id=08001")

# time.sleep(10)

# driver.quit()

from bs4 import BeautifulSoup
import requests
import pandas as pd


url = r"https://armstat.am/am/?nid=12&id=11001&submit=%D5%93%D5%B6%D5%BF%D6%80%D5%A5%D5%AC"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
sec_html_tags = soup.find_all('option')
# for sections in sec_html_tags:
#     print(sections.text)
    
#     break

# data = soup.find_all('table')
# for d in data:
#     print(data.text)
# tables = soup.find_all('table')


# table = soup.find_all('table', class_='data')
# for row in table.find_all('tr'):    
#     # Find all data for each column
#     columns = row.find_all('td')
#     print(type(columns))

tables = soup.find_all('table', class_='data')
all_data = []
data_dict ={}

for table in tables:
    for row in table.find_all('tr'):    
        columns = row.find_all('td')
        row_data = [column.get_text(strip=True) for column in columns]
        row_data = row_data[:3] 
        
        if len(row_data) > 0:
            all_data.append(row_data)
        
df = pd.DataFrame(all_data, columns=['Year', 'Value', 'decrease']) 

# Display the DataFrame
# print(df)
name = soup.find('h2').text
data_dict[name] = df
print(data_dict[name].columns)