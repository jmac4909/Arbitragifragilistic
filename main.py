import scrapy
import json


data = {}
# data['Basketball'] = []
# data['Hockey'] = []
# data['Football'] = []
# data['Soccer'] = []
# data['Tennis'] = []


class QuotesSpider(scrapy.Spider):
    name = 'events'
    start_urls = [
        'https://www.betonline.ag/sportsbook',

        'https://www.betonline.ag/sportsbook/hockey/nhl',
        ##Basketball
        'https: // www.betonline.ag / sportsbook / basketball / nba'
        'https://www.betonline.ag/sportsbook/basketball/ncaa',
        'https://www.betonline.ag/sportsbook/basketball/australia',
        'https://www.betonline.ag/sportsbook/basketball/brazil',
        'https://www.betonline.ag/sportsbook/basketball/germany',
        'https://www.betonline.ag/sportsbook/basketball/intl',
        'https://www.betonline.ag/sportsbook/basketball/philippines',

        'https://www.betonline.ag/sportsbook/soccer/epl',
        'https://www.betonline.ag/sportsbook/soccer/todaygames#',

        'https://www.betonline.ag/sportsbook/golf/pga',
        'https://www.betonline.ag/sportsbook/golf/euro-pga',

        'https://www.betonline.ag/sportsbook/tennis/atp',
        'https://www.betonline.ag/sportsbook/tennis/wta',
        'https://www.betonline.ag/sportsbook/tennis/challenger'
    ]

    def findsport(self, stringy):
        string = stringy.split(' ')
        if len(string) > 4:
            data[string[5]] = []
            return string[5]
        return 'other'

    def parse(self, response):
        num = 0
        table = response.css('table.league');
        events = table.css('tbody.event');
        dat = table.css('tbody.date')
        tsport = dat.css('td.bdt::text').get()
        sport = self.findsport(str(tsport))
        for event in events:
            ++num
            teamone = event.css('tr.h2hSeq')
            teamonename = teamone.css('td.col_teamname::text').get();
            teamtwo = event.css('tr.otherline')
            teamtwoname = teamtwo.css('td.col_teamname::text').get();
            time = teamone.css('td.col_time::text').get()
            data[sport].append({
                'Event': sport,
                'Time': time,
                'Team 1': teamonename,
                'Team 2': teamtwoname,
            })
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        print("----")
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

