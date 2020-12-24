import feedparser

class NewsAPI(object):

    rss_link = 'https://www.channelnewsasia.com/rssfeeds/8396082'
    keyword_highlight_color = 'red'
    
    def __init__(self, master, callback_=None):
        self.master = master
        if callback_ != None:
            self.callback_ = callback_
    
      


    def get_news(self, number, keyword=None):
        news = ""
        NewsFeed = feedparser.parse(self.rss_link)

        c = 0
        found = False
        for i in NewsFeed.entries:
            if keyword != None:
                for k,v in keyword.items():
                    if k.lower() in i['title'].lower():
                        found=True
                        i['title'] = "<font color=\""+v+"\">"+i['title']+"</font>"
                        break
            if found == True:
                news = news + i['title'] + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
            else:
                news = news + i['title'] + '      '

            c = c + 1
            if c == number:
                break

        return news
    
    def process_news_data(self, data):
        results = []
        d = data.splitlines()
        for line in d:
            line = line.strip()
            if '<title>' in line:
                results.append(line.replace('<title>','').replace('</title>','').replace('&#039;','"'))
        return results