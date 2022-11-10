from parser import url_to_question

from bs4 import BeautifulSoup

import time
import requests
import pickle 

from pathlib import Path

# Obtain the 50 links from the page link
def get_questions(page_link):
    
    soup = BeautifulSoup(requests.get(page_link).content, 'html.parser')
    
    # Get all the links of questions from the page
    question_list = soup.find('div', {'id': 'question-list'})

    # From the question list, get all the questions links
    links = [link.find('a')['href'] for link in  question_list.find_all('h2')]

    # Append the ros answers link to each link
    links = [f'https://answers.ros.org{link}' for link in links]

    return links

def get_page_limit(url):
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    
    # Get the div with the class pager
    pager = soup.find('div', {'class': 'pager'})

    # Get the sixth span from pager
    page_limit = pager.find_all('span')[5].text

    return int(page_limit)


if __name__ == '__main__':

    # Make the data dir    
    p = Path('data')
    p.mkdir(exist_ok=True)

    URL = 'https://answers.ros.org/questions/scope:all/sort:activity-asc'

    questions = list()

    # Get the page limit
    page_limit = get_page_limit(URL)

    for i in range(1, page_limit + 1):

        print(f'Page {i}/{page_limit}')

        # Each question is a link
        all_questions = get_questions(f'{URL}/page:{i}/')
        
        for link in all_questions:
            print(link)
            question = url_to_question(link)
            questions.append(url_to_question(link))

            url_id = link.split('/')[4]
        
            with open(f'data/question_{url_id}.pkl', 'wb') as outp:
                pickle.dump(question, outp, pickle.HIGHEST_PROTOCOL)
            
            time.sleep(1)
