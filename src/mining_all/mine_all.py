# -*- coding: utf-8 -*-
from ros_answers_miner.parser import url_to_question
# Import the necessary libraries

from bs4 import BeautifulSoup

import pickle
import time
import requests

from pathlib import Path

# Obtain the 50 links from the page link
def get_questions(page_link):
    
    try_get_questions = True
    
    while try_get_questions:
        try:
            soup = BeautifulSoup(requests.get(page_link).content, 'html.parser')
            
            # Get all the links of questions from the page
            question_list = soup.find('div', {'id': 'question-list'})

            # From the question list, get all the questions links
            links = [link.find('a')['href'] for link in  question_list.find_all('h2')]

            # Append the ros answers link to each link
            links = [f'https://answers.ros.org{link}' for link in links]

            try_get_questions = False

        # Catch the NewConnectionError exception
        except requests.exceptions.NewConnectionError:
            # Sleep for 3 minutes to prevent the connection error
            time.sleep(180)
            continue
    
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

    # Get the page limit
    page_limit = get_page_limit(URL)

    for i in range(1, page_limit + 1):

        print(f'Page {i}/{page_limit}')

        # Each question is a link
        all_questions = get_questions(f'{URL}/page:{i}/')
        
        questions_page = list()

        for link in all_questions:
            print(f'Parsing {link}')

            try_get_question = True

            while try_get_question:
                try:
                    question = url_to_question(link)
                    questions_page.append(question)

                    try_get_question = False
                
                except requests.exceptions.NewConnectionError:
                    time.sleep(180)
                
                except Exception:
                    # Write to a text file the link of the question that failed
                    with open('data/failed_questions.txt', 'a') as f:
                        f.write(f'{link}')
                        try_get_question = False
                    
        # Save the questions_page list to a pickle file in data dir
        with open(f'data/questions_page_{i}.pkl', 'wb') as f:
            pickle.dump(questions_page, f)

        # Sleep for 0.5 second
        time.sleep(0.5)