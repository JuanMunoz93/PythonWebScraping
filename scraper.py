from re import L, T
import requests
import lxml.html as html
import os
import datetime
import constans

def getCount():
    return constans.COUNT_TEST

def updateCount():
    constans.COUNT_TEST=constans.COUNT_TEST +1

def get_html_from_response(response, decode_format):
    notice=response.content.decode(decode_format)                           #decode the site content to utf-8
    return html.fromstring(notice)                                          #parse de content to html

def parse_news(link, today):
    try:
        response=requests.get(link)
        if response.status_code==200:
            
            parsed = get_html_from_response(response,'utf-8')
            try:

                title=parsed.xpath(constans.XPATH_TITLE)[0]
                title="%s %s"%(str(getCount()), title.replace("#","").replace("|",""))
                updateCount()
                print(title)
                summary=parsed.xpath(constans.XPATH_SUMMARY)[0]
                body=parsed.xpath(constans.XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
             raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def scrap_news():
    try:
        response=requests.get(constans.HOME_URL)                            #get the home page
        if response.status_code==200:                                       #verify that the site is available
            parsed = get_html_from_response(response,'utf-8')
            links_to_news= parsed.xpath(constans.XPATH_LINK_TO_ARTICLE)     #get the links of the news
            today = datetime.date.today().strftime('%d-%m-%Y')              #create the file name using the current date
            today=f'scraps//{today}'

            if not os.path.isdir(today):                                    #creates the file if it doesnt exist
                os.mkdir(today)

            for link in links_to_news:                                      #scrap each one of the news
                parse_news(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        



def run():
    scrap_news()

if __name__ == '__main__':
    run()
