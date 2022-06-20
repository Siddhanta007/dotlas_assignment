# importing the libraries
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

# loading the url inside a list so we can iterate through them.
urls = [
    "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308",
    "https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308",
    "https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308",
    "https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/630107/art-of-dum-discovery-gardens?aid=1308",
    "https://www.talabat.com/uae/restaurant/660056/kings-biryani-jumeirah-lakes-towers--jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/42486/the-500-calorie-projec-jumeirah-lakes-towers--jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/679777/koussa-blaban-jumeirah-beach-residence--jbr?aid=1308",
    "https://www.talabat.com/uae/restaurant/673790/1-billion-meals-business-bay?aid=1308"
]
print("Number of links : ", len(urls))

df = pd.DataFrame(list())
df.to_csv('output.csv', index=False)
i = 1

# iterating through urls
for url in urls:
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')

    # finding the data under script tag
    s = soup.find('script', id='__NEXT_DATA__')

    # converting the data into json format and loading it into a variable
    data = json.loads(s.text)

    # extracting the details about the restaurant and menu from the data
    reaturant_data = data['props']['pageProps']['initialMenuState']['restaurant']
    menu = data['props']['pageProps']['initialMenuState']['menuData']['items']

    # creating resturant table
    menu_items = []
    for i in menu:
        menu_items.append(i['name'])

    resturnt_detail = {}
    resturnt_detail['resturant_name'] = reaturant_data['name']
    resturnt_detail['resturant_logo'] = reaturant_data['logo']
    resturnt_detail['latitude'] = reaturant_data['latitude']
    resturnt_detail['longitude'] = reaturant_data['longitude']
    resturnt_detail['cuisine_tag'] = reaturant_data['cuisineString']
    resturnt_detail['menu_items'] = (','.join(menu_items))

    # creating pandas df from the dictionary
    rest_details_df = pd.DataFrame(resturnt_detail, index=[0])
    print('Table Number : ', i)
    print(rest_details_df)

    # creating menu list
    menu_details = []
    menu_items.append(['item_name', 'item_description', 'item_price', 'item_image'])
    for i in menu:
        menu_details.append([i['name'], i['description'], i['price'], i['image']])

    # creating menu dataframe
    menu_details_df = pd.DataFrame(menu_details, columns=['item_name', 'item_description', 'item_price', 'item_image'])
    print(menu_details_df.head(5))

    # writing dataframes to file

    df_list = [rest_details_df, menu_details_df]
    with open('output.csv', 'a') as file:
        for df in df_list:
            df.to_csv(file, index=False)
            file.write('\n')