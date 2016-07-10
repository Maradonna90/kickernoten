from os import system
import sys
season = sys.argv[1]
day = season.argv[2]

outFile = 'kicker-'+season+'-'+day+'.json'
system('scrapy crawl kicker -o ' + outFile + ' -a season=' +season+ ' -a day='+ day)
