import scrapy


class MoviesSpider(scrapy.Spider):
    name = "movies"

    # start_urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    
    def start_requests(self):
        urls = [
            "https://www.imdb.com//chart/top"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_and_extract_urls)
    
    def parse_and_extract_urls(self, response):
        # titles = response.css('td.titleColumn a::text').extract() 
        links = response.css('td.titleColumn a::attr(href)').extract()
        urls=[]

        for i in links:
            urls.append("https://www.imdb.com/"+i)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        title = response.css('div.title_wrapper h1::text').extract_first()
        runtime = response.css('div.txt-block time::text').extract_first()
        rating, release_date = response.css('div.title_wrapper meta::attr(content)').extract()
        print rating
        genre = ','.join(response.css('div.title_wrapper span.itemprop::text').extract())
        voters = response.css('span.small::text').extract_first()
        plot_short = response.css('div.summary_text::text').extract_first()
        directors = ','.join(response.css('div.credit_summary_item')[0].css('span.itemprop::text').extract())
        # print directors
        writers = ','.join(response.css('div.credit_summary_item')[1].css('span.itemprop::text').extract())
        # print writers
        stars = ','.join(response.css('div.credit_summary_item')[2].css('span.itemprop::text').extract())
        # print stars
        # plot_summary = response.css('p.blurb span::text').extract_first()
        actors = ','.join(response.css('td.itemprop span::text').extract())
        # print actors
        characters = ','.join(response.css('td.character a::text').extract())
        # print characters
        # plot_keywords = 
        # country =
        # language = 
        # filming_location = 
        # budget = 
        # gross_usa = 
        # gross_worldwide = 
        production_company = response.css('span.itemprop::text').extract()[-1]
        
        fields = [title, runtime, rating, release_date, genre, voters, plot_short, directors, writers, stars, actors, characters, production_company] 
        # plot_summary]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

        data = ':'.join(fields) + "\n"
        
        with open("movies.csv", "a") as file:
            file.write(data.encode('utf-8'))
        self.log('%s data scraped' % title)
        