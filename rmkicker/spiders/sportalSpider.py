import scrapy
import re
from rmkicker.items import RmkickerItem
class kickerSpider(scrapy.Spider):
    name = "sportal"
    allowed_domains = ["sportal.de"]
    def __init__(self, season=None, day=None):
        base_url = "http://www.sportal.de/fussball/bundesliga/ergebnisse/spieltag-{2}-saison-20{0}-20{1}".format(int(season)-1, season, day)
        self.start_urls = [base_url]
        self.season = season
        self.day = day
    def parse(self, response):
        for href in response.xpath('//li[@class="score"]/a[contains(text(), ":")]/@href'):
            url = response.urljoin(href.extract())
            #print("url:", url)
            yield scrapy.Request(url, callback=self.getToRatings)
    
    def getToRatings(self, response):
        for href in response.xpath('//a[text()="Spielernoten"]/@href'):
            url = response.urljoin(href.extract())
            #print("url:", url)
            yield scrapy.Request(url, callback=self.getNameAndRating)

    def getNameAndRating(self, response):

        #starting lineup
        for sel in response.xpath('//div[@class="spielinfoSpielfeldPlayer"]'):
            item = RmkickerItem()
            spieler_name = sel.xpath('div/a/@title')[0].extract()
            item['spieler_name'] = ''.join(spieler_name).replace('\xa0', ' ')
            spieler_note = sel.xpath('div/div[@class="note_zahl"]/text()').extract()
            spieler_note = ''.join(spieler_note)
            spieler_note = re.findall('(\d,\d)|(\d)', spieler_note)
            if not spieler_note:
                item['spieler_note'] = 0
            else:

                item['spieler_note'] = float(''.join(spieler_note[0]).replace(",", "."))
            yield item
        
        #sub players
        for sel in response.xpath('//div[@class="headDataRowLiDiv2" and contains(text(), "für")]/text()'):
            string = sel.extract().split('(')
            if len(string) > 1:
                spieler_name = ''.join(re.findall('[a-zA-Zäüö]' , string[0]))
                spieler_note = ''.join(re.findall('(\d,\d)|(\d)', string[1])[0])
                spieler_note = float(spieler_note.replace(",", "."))
                #print(spieler_name, spieler_note)
                item['spieler_name'] = spieler_name
                item['spieler_note'] = spieler_note
                yield item

