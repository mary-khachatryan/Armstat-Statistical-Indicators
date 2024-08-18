from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
id  = '11006'
url = f"https://armstat.am/am/?nid=12&id={id}&submit=%D5%93%D5%B6%D5%BF%D6%80%D5%A5%D5%AC"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
id_dict = {}
data_dict ={}
labels = []



sec_html_tags = soup.find_all('option')
for  section in sec_html_tags:

    id_dict[section.attrs['label']] = (section.attrs['value'])
    labels.append(section.attrs['label'])
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
    df['Value'] = df['Value'].replace('-', 0)
    df['Value'] = df['Value'].astype(float)
    return df

option = st.selectbox("Choose ",labels,index=None,placeholder="Select contact method...",
)

id = id_dict[option]
# id = '08010'
source = page_data_parser(id)

# source = pd.DataFrame({
#     'Year': pd.date_range(start='2020', periods=10, freq='Y'),
#     'Value': [3, 5, 7, 6, 8, 10, 6, 5, 9, 11]
# })
st.area_chart(source, x="Year", y="Value", color='#ff00dd')
st.write("You selected:", option)

print(labels)

# df2= pd.read_html(url)
# print(df2, "ասդ")