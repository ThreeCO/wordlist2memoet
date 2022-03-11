"""
   FORKED FROM https://github.com/mfz/wordlist2anki 
   SCRIPT IS CREATING FLASH CARDS FOR https://github.com/memoetapp/memoet
"""
import bs4
import requests
import json
import sys
import os.path
import time as tme
import random

__doc__ = """
usage: vocab_dl.py wordlist

creates output.csv for import into memoet
"""

"""
obtain word pos, definition, description and word family from vocabulary.com
"""
def worddef(word):
    print("+++++ Current word is '{word}'".format(word = word))
    URL = "https://www.vocabulary.com/dictionary/{word}".format(word = word)
    response = requests.get(URL)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    _ = [x.strip() for x in soup.find('div', class_ = 'definition').text.split('\r\n') if x.strip() != '']
    pos = _[0]
    definition = _[1].replace(',', '&comma;').replace('`',"'").replace('"',"'")
    _ = soup.find('p', class_ = 'short')
    description = ('' if _ is None else _.text).replace(',', '&comma;')
    family = soup.find('vcom:wordfamily')['data']
    fp = json.loads(family)
    _ = sorted([(x['word'], x.get('parent', ''),x['type'], x['ffreq']) for x in fp if x.get('parent', word) == word and x.get('hw', False) == True], key = lambda x: x[3], reverse = True)
    wordfamily = [x[0] for x in _]
    return (word, pos, definition, description, wordfamily)

if __name__ == '__main__':
    wordlist = []
    wordlistfile = sys.argv[1]
    with open(wordlistfile, encoding='utf-8-sig') as fh:
        for line in fh:
            wordlist.append(line.strip())
    items = []
    # OUTPUT NAME HAS TO BE SET MANUALLY
    filename = "english_3000.csv"
    f = open("/app/{filename}".format(filename = filename),"w")
    f.write ("Title,Image,Content,Quiz type,Option 1,Option 2,Option 3,Option 4,Option 5,Correct option (1-5),Explanation\n")
    cnt = 0
    for word in wordlist:
        """ TRYING TO PREVENT GETTING BLOCKED """
        # SLEEP EVERY 15 ENTRIES BETWEEN 3 to 10 SECONDS 
        if (cnt % 15 = 0):
            tme.sleep(random.randrange(3,10,1))
            # SLEEP EVERY 50 ENTRIES BETWEEN 2 to 5 MINUTES
            if (cnt % 50 = 0):
                tme.sleep(random.randrange(120,300,60))
        try:    
            word, pos, definition, description, wordfamily = worddef(word)

            # WRITE FLASH CARDS AS SHOULD BE "NORMAL"
            f.write('"{word}",,,Flash card,,,,,,,"({pos}) **{definition}**"\n'.format(word = word, definition = definition, pos = pos))
            # WRITE FLASH CARDS "REVERSE"
            f.write('"({pos}) {definition}",,,Flash card,,,,,,,"{word}"\n'.format(word = word, definition = definition, pos = pos))
        except:
            print("--- ERROR --- The word '{word}' could not be fetched!".format(word = word))
        cnt = cnt + 1
    f.close()
