import pandas as pd
import re
import requests
import time
import json
from pathlib import Path


def get_catalog_names():
    catalogs_path = 'data/catalogs.csv'
    # If the file already exists, then we read the categories from it
    catalogs_file = Path(catalogs_path)
    if catalogs_file.exists():
        catalogs = pd.read_csv(catalogs_path, names=['id'])
        return catalogs.id.tolist()

    # If there is no file with categories, then they need to be parsed
    catalogs = set()
    page_number = 1
    while True:
        link = f'https://hi-tech.mail.ru/mobile-catalog/?page={page_number}'
        response = requests.get(link)
        response.encoding = 'utf-8'

        # Example: 14668720-catalog
        current_catalogs = set(re.findall(r'\d{8}-catalog', response.text))
        if not current_catalogs:
            # if there are no catalogs on the page
            break
        catalogs = catalogs | current_catalogs
        page_number += 1

        time.sleep(1)

    # Save catalogs to file
    catalogs_df = pd.DataFrame(catalogs)
    catalogs_df.to_csv(catalogs_path, index=False)

    return list(catalogs)


def get_reviews():
    reviews_path = 'data/raw_reviews.csv'
    # If the file already exists, then we read the reviews from it
    reviews_file = Path(reviews_path)
    if reviews_file.exists():
        raw_reviews = pd.read_csv(reviews_path, index_col=0)
        return process_data(raw_reviews)

    # If there is no file with reviews, then they need to be parsed
    reviews_list = []
    for catalog in get_catalog_names():
        page_number = 1
        while True:
            link = f'https://hi-tech.mail.ru/ajax/{catalog}/feedback/list/?page={page_number}'
            response = requests.get(link)
            response.encoding = 'utf-8'

            page = json.loads(response.text)
            if not page:
                break

            for review in page['data']:
                for field in review['text']:
                    review[field['title']] = field['text']
                del review['text']
                reviews_list.append(review)
            if page['pager']['next'] is None:
                break
            else:
                page_number += 1

            time.sleep(1)

    raw_reviews = pd.DataFrame(reviews_list)
    raw_reviews.to_csv(reviews_path)

    return process_data(raw_reviews)


def process_data(data):
    pros = data[['Плюсы']]
    pros = pros.rename(columns={'Плюсы': 'text'})
    pros.loc[:, 'label'] = 1

    cons = data[['Минусы']]
    cons = cons.rename(columns={'Минусы': 'text'})
    cons.loc[:, 'label'] = 0

    pr_data = pros.append(cons, ignore_index=True, sort=False)
    # This transformation is required for TfidfVectorizer to work
    pr_data['text'] = pr_data['text'].values.astype('U')

    return pr_data


if __name__ == "__main__":
    get_reviews()
