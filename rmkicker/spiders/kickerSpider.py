import scrapy
import re
from rmkicker.items import RmkickerItem
class kickerSpider(scrapy.Spider):
    name = "kicker"
    allowed_domains = ["kicker.de"]
    def __init__(self, season=None, day=None):
        base_url = "http://www.kicker.de/news/fussball/bundesliga/spieltag/1-bundesliga/20{0}-{1}/{2}/0/spieltag.html".format(int(season)-1, season, day)
        self.start_urls = [base_url]
        self.season = season
        self.day = day
    def parse(self, response):
        for href in response.xpath('//a[text()="Analyse"]/@href'):
            url = response.urljoin(href.extract())
            #print("url:", url)
            yield scrapy.Request(url, callback=self.getNameAndRating)

    def getNameAndRating(self, response):
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        for sel in response.xpath('//div[@class="spielerdiv"]'):
            item = RmkickerItem()
            spieler_name = sel.xpath('a/text()').extract()
            item['spieler_name'] = ''.join(spieler_name).replace('\xa0', ' ')
            spieler_note = sel.xpath('text()').extract()
            spieler_note = ''.join(spieler_note)
            spieler_note = re.findall('(\d,\d)|(\d)', spieler_note)
            if not spieler_note:
                item['spieler_note'] = 0
            else:
                item['spieler_note'] = float(''.join(list(filter(None, spieler_note))[0]).replace(",", "."))
            yield item
