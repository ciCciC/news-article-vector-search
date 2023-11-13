import requests
import asyncio
import os
import argparse
import pandas as pd


def get_args():
    parser = argparse.ArgumentParser(__name__,
                                     description=f'{__name__} as data downloader',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--SCRAPER_API_URL', type=str, default='http://localhost:5011', help='URL of the scraper api')
    return parser.parse_args()


def get_categories():
    response = requests.get(f'{os.environ["SCRAPER_API_URL"]}/categories/nl')
    return [category['topic'] for category in response.json()]


def get_category_articles(category: str):
    bases_url = f'{os.environ["SCRAPER_API_URL"]}/category/all/{category}'
    return [category, requests.get(bases_url)]


async def get_category_articles_async(category: str):
    return await asyncio.to_thread(get_category_articles, category)


async def main():
    all_categories = get_categories()

    print(f'Download started for {all_categories} ...')
    results = await asyncio.gather(*[get_category_articles_async(category) for category in all_categories])

    all_articles = []
    cats = []
    for response in results:
        r = response[1].json()
        cat = [response[0]] * len(r)
        print(f'{cat[0]} -> {len(r)}, {len(cat)}')
        cats += cat
        all_articles += r

    print(f'Articles: {len(all_articles)} \t Cats: {len(cats)}')

    print('Storing all articles...')
    raw_data = pd.DataFrame(all_articles)
    raw_data['category'] = cats
    raw_data.to_csv('data/articles.csv', index=False)
    print('Storing done')


if __name__ == "__main__":
    args = get_args()
    os.environ["SCRAPER_API_URL"] = args.SCRAPER_API_URL
    asyncio.run(main())
