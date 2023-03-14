import boto3
import requests
from bs4 import BeautifulSoup
import datetime

def lambda_handler(event, context):
    # Get the current date and time for the write date
    write_date = datetime.datetime.now().isoformat()

    # Create a DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table_name = 'BlogPosts'
    table = dynamodb.Table(table_name)

    url = 'https://aws.amazon.com/blogs/security'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = soup.find_all('h2', {'class': 'blog-post-title'})
        if len(titles) > 0:
            results = []
            for i, title in enumerate(titles):
                post_url = title.find('a', {'property': 'url'})['href']
                post_title = title.text.strip()
                
                # Check if the blog post with the given title already exists in the table
                existing_post = table.get_item(Key={'Title': post_title})
                if 'Item' in existing_post:
                    continue

                date = title.find_next('footer', {'class': 'blog-post-meta'}).find('time').text.strip()
                categories = title.find_next('footer', {'class': 'blog-post-meta'}).find('span', {'class': 'blog-post-categories'}).text.strip()
                results.append({'Title': post_title, 'Date': date, 'Categories': categories, 'URL': post_url, 'WriteDate': write_date})

            with table.batch_writer() as batch:
                for result in results:
                    batch.put_item(Item=result)
            print(f'Successfully wrote {len(results)} new items to DynamoDB table {table_name}.')
        else:
            print('No blog posts found.')
    else:
        print(f'Error: Unable to retrieve page. HTTP status code: {response.status_code}')
