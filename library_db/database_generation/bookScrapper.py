import requests
import json
import pandas as pd
import xlsxwriter

def getBookInfoWithTitle(title):
    url = 'https://openlibrary.org/search.json?title=' + title
    try:
        response = requests.get(url, allow_redirects=True, timeout=20)
        data = json.loads(response.text)
    except:
        print(title)
        return
    try:
        work = data['docs'][0]['key']
        seed = data['docs'][0]['seed'][0]
    except:
        bookInfo={'title': title, 'authors': [None], 'subjects': [None], 'publishers': [None],
                  'publish_date': None, 'revision': None, 'number_of_pages': None}
        return bookInfo
    
    return getBookInfo(work, seed)

def getBookInfo(work, seed):
    url = 'https://openlibrary.org' + work + '.json'
    try:
        response = requests.get(url, allow_redirects=True, timeout=20)
        data = json.loads(response.text)
    except:
        return
    bookInfo = {}
    # Get info for a specific work
    wantedKeys = ['title', 'authors', 'subjects', 'description']
    for key in wantedKeys:
        if key in data:
            if key == 'authors':
                bookInfo[key] = []
                for author in data[key]:
                    author = author['author']
                    try:
                        url = 'https://openlibrary.org' + \
                            author['key'] + '.json'
                        response = requests.get(
                            url, allow_redirects=True, timeout=20)
                        authorData = json.loads(response.text)
                        bookInfo[key].append(authorData['name'])
                    except:
                        pass
            else:
                bookInfo[key] = data[key]
    # Get info for a specific book of the previous work
    wantedSeed = ['identifiers', 'languages', 'publishers',
                  'publish_date', 'publish_places', 'revision', 'number_of_pages']
    url = 'https://openlibrary.org' + seed + '.json'
    try:
        response = requests.get(url, allow_redirects=True, timeout=20)
        data = json.loads(response.text)
    except:
        data = {}
    for key in wantedSeed:
        if key in data:
            bookInfo[key] = data[key]
    return bookInfo


def findBookTitles():
    import re
    url = 'https://libraryof1000books.wordpress.com/the-list-of-1000-books/'
    response = requests.get(url, allow_redirects=True)
    data = response.text
    titles = re.findall(r'<li>(.+?) &#8211', data)
    
    for i in range(len(titles)):
        title = titles[i]
        if title[0]=="<":
            while title[0]!=">":
                title=title.replace(title[0],"",1)
            title=title.replace(title[0],"",1)
        if title[-6:]=="&#8217":
            title=title.replace(title[-6:],"")
        titles[i]=title
        
    return titles

def generate():
    titles = findBookTitles()
    bookInfos = []
    for title in titles:
        print(f"Getting info for {title}...")
        print(f"Remaining: {len(titles) - titles.index(title)}")
        bookInfo = getBookInfoWithTitle(title)
        if bookInfo:
            bookInfos.append(bookInfo)
    with open('bookInfos.json', 'w') as f:
        json.dump(bookInfos, f)
    df=pd.read_json("bookInfos.json")
    df.to_excel("excel_files/bookInfo.xlsx", engine="xlsxwriter")
    
