from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import jellyfish
import time
import random

id  = '11006'
url = f"https://armstat.am/am/?nid=12&id={id}&submit=%D5%93%D5%B6%D5%BF%D6%80%D5%A5%D5%AC"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
id_dict = {}
threshold = 0.9
labels = []
gender = ['տղամարդ','կանայք','տղամարդու', 'կնոջ', 'աղջիկներ', 'տղաներ','Կանայք', "Տղամարդ"] 


sec_html_tags = soup.find_all('option')
for  section in sec_html_tags:

    id_dict[section.attrs['label']] = (section.attrs['value'])
    labels.append(section.attrs['label'])
# print(labels)



def page_data_parser(id):
    url = f"https://armstat.am/am/?nid=12&id={id}&submit=%D5%93%D5%B6%D5%BF%D6%80%D5%A5%D5%AC"

    # Retry logic
    retries = 5
    for attempt in range(retries):
        try:
            # Adding a timeout and fetching the page
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Introduce a random sleep interval to avoid hammering the server
            time.sleep(random.uniform(1, 3))

            # Parsing the HTML content
            soup = BeautifulSoup(response.content, "html.parser")
            break  # If the request is successful, break out of the loop
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error on attempt {attempt + 1}: {e}")
            time.sleep(2)  # Wait before retrying
        except requests.exceptions.Timeout as e:
            print(f"Timeout on attempt {attempt + 1}: {e}")
            time.sleep(2)
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            return None  # Stop further attempts on an HTTP error
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    # Return None if all retries fail
    if response is None:
        return None

    # Extracting data from the tables on the page
    one_page_data = []
    tables = soup.find_all('table', class_='data')

    

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
    
    df['Value'] = df['Value'].replace('-', 0)
    df['Value'] = df['Value'].astype(float)
    

    return df

option = st.selectbox("Choose ",labels,index=None,placeholder="Select contact method...",
)
similars = []
if option:
    similars = []
    similars.append(option)
    for gend in gender:
        if gend in option:
             st.write("gender:", gend, option)
             for sim in labels:
                similarity_score = jellyfish.jaro_winkler_similarity(option, sim) 
                if 1 > similarity_score > threshold:
                    # print(f"The texts are similar (score: {similarity_score:.2f})", sim)
                    # st.write(f"The texts are similar (score: {similarity_score:.2f})", sim)
                    similars.append(sim)
    
if len(similars) > 1:
    add = st.radio("See also ",similars)
    if add:
        id = id_dict[add]
        print(add)
        source = page_data_parser(id)
        st.area_chart(source, x="Year", y="Value", color='#dfedeb')
        st.write("You selected:", option)

else:
    id = id_dict[option]
    source = page_data_parser(id)
    st.area_chart(source, x="Year", y="Value", color='#ff00dd')
    st.write("You selected:", option)
    


