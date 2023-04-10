import scrapy

viking = ["https://lista.mercadolivre.com.br/informatica/_Loja_viking"]
dutraMaquinas = ['https://loja.mercadolivre.com.br/dutra-maquinas']
casaDasSerras = ['https://loja.mercadolivre.com.br/casa-das-serras']

megamamute = ['https://loja.mercadolivre.com.br/mega-mamute']
siberiano = ['https://loja.mercadolivre.com.br/siberiano']
eletro2 = ['https://loja.mercadolivre.com.br/2eletro']
inpower = ['https://loja.mercadolivre.com.br/inpower']
comprou123 = ['https://lista.mercadolivre.com.br/_Loja_123-comprou']



class MlSpider(scrapy.Spider):
    name = "ml"
    #allowed_domains = ["mercadolivre.com"]
    start_urls = megamamute
    #! start_urls = viking

    def parse(self, response, **kwargs):
        for i in response.xpath('//li[@class="ui-search-layout__item"]'):
            price = i.xpath('.//div[@class="ui-search-price__second-line shops__price-second-line"]/span[last()-1]/span[@class="price-tag-text-sr-only"]//text()').getall()
            #title = i.xpath('.//li[@class="ui-search-layout__item"]//h2[@class="ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title"]/text()')
            #title = i.xpath('.//*[@class="ui-search-item__group ui-search-item__group--title shops__items-group"]/h2/text()').get()
            title = i.xpath('.//div[@class="ui-search-item__group ui-search-item__group--title shops__items-group"]/a/h2/text()').get()
            #link = i.xpath('.//*[@class="andes-card andes-card--flat andes-card--default ui-search-result shops__cardStyles ui-search-result--core andes-card--padding-default andes-card--animated"]/a/@href').get()
            link = i.xpath('.//div[@class="ui-search-result__image shops__picturesStyles"]/a/@href').get()
            condPagto = i.xpath('.//span[@class="ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--LIGHT_GREEN"]/text()').getall() 
            # if i.xpath('.//span[@class="ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--LIGHT_GREEN"]/div[2]/text()').get() != None else i.xpath('.//span[@class="ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--BLACK"]/div[2]/text()').get()
            
            yield{
                'price' : price,
                'title' : title,
                'condicao' : condPagto,
                'link' : link
            }

            next_page = response.xpath('//a[contains(@title,"Seguinte")]/@href').get()
            if next_page:
                yield scrapy.Request(url=next_page, callback=self.parse)
