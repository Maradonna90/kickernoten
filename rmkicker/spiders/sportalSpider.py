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
        #filename = response.url.split("/")[-2] + '.html'
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        # einwechslungenHeim
        # einwechslungenAusw

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

        #sub players away
        #for sel in response.xpath('//div[contains(@id, "einwechslungenAusw")]'):
            # a = sel.xpath('div/a/text()').extract()
            #spieler_name = sel.xpath('div/a/text()').extract()
            #spieler_note = sel.xpath('div/text()').extract()
            #print(spieler_name, spieler_note)
            #if spieler_note:
                #for i in range(0, len(spieler_note)+1, 2):
                    #print(i)
                    #item = RmkickerItem()
                    #name = spieler_name[i]
                    #name = ''.join(name).replace('\xa0', ' ')
                    #note = spieler_note[int(i/2)]
                    #note = ''.join(note)
                    #note = re.findall('(\d,\d)|(\d)', note)
                    #note = float(''.join(list(filter(None, note))[0]).replace(",", "."))
                    #item['spieler_name'] = name
                    #item['spieler_note'] = note
                    #yield item
        
        #sub player home
        #for sel in response.xpath('//div[contains(@id, "einwechslungenHeim")]'):
            #a = sel.xpath('div/a/text()').extract()
            #spieler_name = sel.xpath('div/a/text()').extract()
            #spieler_note = sel.xpath('div/text()').extract()
            #if spieler_note:
                #for i in range(0, len(spieler_note)+1, 2):
                    #item = RmkickerItem()
                    #name = spieler_name[i]
                    #name = ''.join(name).replace('\xa0', ' ')
                    #note = spieler_note[int(i/2)]
                    #note = ''.join(note)
                    #note = re.findall('(\d,\d)|(\d)', note)
                    #note = float(''.join(list(filter(None, note))[0]).replace(",", "."))
                    #item['spieler_name'] = name
                    #item['spieler_note'] = note
                    #yield item
