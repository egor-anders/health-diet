import requests
from bs4 import BeautifulSoup
import csv
import json


main_url = 'https://health-diet.ru'

def get_html(url):
    r = requests.get(url)
    return r.text

def make_headers(headers, count, category_name):
    with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow((headers[0].text, headers[1].text + ' кКал', headers[2].text + ' г', headers[3].text + ' г', headers[4].text + ' г'))
        
def write_csv(data, count, category_name):
    with open(f'data/{count}_{category_name}.csv', 'a', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow((data['name'], data['calories'], data['proteins'], data['fats'], data['carbohydrates']))

def make_json(data, count, category_name):
    with open(f'data/{count}_{category_name}.json', 'a', encoding='utf-8-sig') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def make_html(content, count, category_name):
    with open(f'data/{count}_{category_name}.html', 'w', encoding='utf-8-sig') as f:
        f.write(content)





# with open('index.html', 'w', encoding="utf-8-sig") as f:
#     url = "https://health-diet.ru/table_calorie/"
#     f.write(get_html(url))


def get_links(file_name):
    with open(f'{file_name}', encoding="utf-8-sig") as f:
        content = f.read()

    soup = BeautifulSoup(content, 'lxml')

    categories = soup.find_all('a', class_="mzr-tc-group-item-href")

    categories_data = {}
    symbols = [', ', ' ', '-']
    for category in categories:
        category_name = category.text.strip()

        if "'" in category_name:
            category_name = category_name.replace("'", '')

        for symbol in symbols:
            category_name = category_name.replace(symbol, '_')
        category_url = main_url + category.get('href').strip()
        categories_data[category_name] = category_url

    with open('main.json', 'w', encoding='utf-8-sig') as j:
        json.dump(categories_data, j, indent=4, ensure_ascii=False)


with open('main.json', encoding='utf-8-sig') as f:
        categories = json.loads(f.read())



def main():
    # get_links('index.html')
    count = 1
    for category_name, category_url in categories.items():
        content = get_html(category_url)
        soup = BeautifulSoup(content, 'lxml')
        if soup.find('div', class_='uk-alert-danger'):
            continue
        else:
            headers = soup.find('thead').find('tr').find_all('th')
            make_headers(headers, count, category_name)
            trs = soup.find('tbody').find_all('tr')
            data_json = []
            for tr in trs:
                tds = tr.find_all('td')
                name = tds[0].text.strip()
                calories = tds[1].text.replace('кКал', '').strip()
                proteins = tds[2].text.replace('г', '').strip()
                fats = tds[3].text.replace('г', '').strip()
                carbohydrates = tds[4].text.replace('г', '').strip()
                data = {
                    'name': name,
                    'calories': calories,
                    'proteins': proteins,
                    'fats':fats,
                    'carbohydrates': carbohydrates
                }
                data_json.append(data)
                write_csv(data, count, category_name)
            make_json(data_json, count, category_name)
            make_html(content, count, category_name)
            count +=1 
                


if __name__ == '__main__':
    main()