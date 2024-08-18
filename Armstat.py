from bs4 import BeautifulSoup
import requests
import pandas as pd

id  = '11006'
url = f"https://armstat.am/am/?nid=12&id={id}&submit=%D5%93%D5%B6%D5%BF%D6%80%D5%A5%D5%AC"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
id_dict = {}
data_dict ={}



sec_html_tags = soup.find_all('option')
for  section in sec_html_tags:
    id_dict[section.attrs['label']] = section.attrs['value']
    
print(id_dict)



def page_data_parser(id):

    url = f"https://armstat.am/am/?nid=12&id={id}&submit=%D5%93%D5%B6%D5%BF%D6%80%D5%A5%D5%AC"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")


    one_page_data = []
    tables = soup.find_all('table', class_='data')
    for table in tables:
        for row in table.find_all('tr'):    
            columns = row.find_all('td')
            row_data = [column.get_text(strip=True) for column in columns]
            row_data = row_data[:3] 
            
            if len(row_data) > 0:
                one_page_data.append(row_data)
        
    df = pd.DataFrame(one_page_data, columns=['Year', 'Value', 'decrease']) 
    name = soup.find('h2').text
    data_dict[name] = df



# df2= pd.read_html(url)
# print(df2, "ասդ")