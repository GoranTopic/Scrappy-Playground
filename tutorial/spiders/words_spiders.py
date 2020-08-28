
import scrapy

class WordSpider(scrapy.Spider):
    name = "words"
    allowed_domains = [ 'www.merriam-webster.com']
    start_urls = [ 'https://www.merriam-webster.com/browse/dictionary/a' ]


    def parse(self, response):
        # get all the alpha links
        for alpha_link in response.xpath('//div[@class="alphalinks"]//@href').getall():
            # for every apha link:
            # call ParseAlphaEntriePage which parses and extracs data from every entry
            print(alpha_link)
            yield response.follow(alpha_link, self.parseAlphaEntriesPage)
   
    def parseAlphaEntriesPage(self, response):
        # parse all entries from the page
        self.parseEntires(response)
        # get next page
        next_page = response.xpath('//a[@aria-label="Next"]//@href').get()
        # if there is a next page
        print(next_page)
        if next_page != "javascript: void(0)":
            # if it is not a dead link
            yield response.follow(next_page, self.parseAlphaEntriesPage)

    def parseEntires(self, response):
        # Gets all the entris from an Alpha entry page 
        entrie_links = response.xpath('//div[@class="entries"]//@href').getall()
        for entry_link in entrie_links:
            yield response.follow(entry_link, self.parseWordEntry)

    def clean_string(self, dirty):
        if isinstance(dirty, str):
            return dirty.replace('\n', '').replace('   ', '').rstrip(' ')
        elif isinstance(dirty, list):
            return " ".join(dirty).replace('\n', '').replace('   ', '').rstrip(' ').replace(" (function() { window.mwHeapEvents['Definition - Has Synonym Guide'] = 'true';  })();", "")

    def parseWordEntry(self, response):
        '''Pasre the web page with a word'''
        data = {
            #get word
            "word" : response.xpath('//h1[@class="hword"]/text()').get(),
            #get pronunciation
            "pronunciations" : response.xpath('//span[@class="pr"]/text()').getall(),
            #get syllables
            "syllables" : response.xpath('//span[@class="word-syllables"]/text()').get(),
            #get definition
            "definitions" : {},
            #get synonyms
            "synonyms" : response.xpath('//div[@id="synonyms-anchor"]/p[@class="function-label"][text()="Synonyms "]/following::ul[1]/li/a/text()').getall(),
            #get antonyms
            "antonyms" : response.xpath('//div[@id="synonyms-anchor"]/p[@class="function-label"][text()="Antonyms "]/following::ul[1]/li/a/text()').getall(),
            #get use the right synonym
            "synonym-discussion": self.clean_string(response.xpath('//div[@id="synonym-discussion-anchor"]/descendant::*/text()').getall()),
            #get the exmaples
            "examples" : [ self.clean_string(span.xpath('descendant::text()').getall()) for span in response.xpath('//div[@id="examples-anchor"]/div[@class="in-sentences"]/span')],
            #get etymology
            "etymology": self.clean_string(response.xpath('//div[@id="etymology-anchor"]/descendant::*/text()').getall()),
        }
                
        #get the syntaxes
        syntaxes = response.xpath('//div[@class="wgt-incentive-anchors"]/preceding::span[@class="fl"]/*/text()').getall()
        #get list of definitions
        definitions = [ entry.xpath('descendant::span[@class="dtText"]/text()').getall() for entry in response.xpath('//div[@class="wgt-incentive-anchors"]/preceding::div[starts-with(@id, "dictionary-entry-")]') ]

        for x in range(0, len(syntaxes)):
            data["definitions"][syntaxes[x]] = [ self.clean_string(definition) for definition in definitions[x] ]

        yield data
     
   
