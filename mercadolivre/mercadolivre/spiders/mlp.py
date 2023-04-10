import scrapy
import json
import re
import mysql.connector

"""
with open("././lista_dutraMaquinas-02-04-2023.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)



with open("././lista_casaDasSerras-04-04-2023.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)


with open("././lista_viking-02-04-2023.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)

"""
#exit(9)

lista = ['././lista_dutraMaquinas-02-04-2023.json', '././lista_casaDasSerras-04-04-2023.json', '././lista_viking-02-04-2023.json']

print(lista[1])

with open(lista[1], encoding='utf-8') as meu_json:
    dados = json.load(meu_json)

print(dados)

exit(90)
# para cada item do arquivo json


    # imprimindo nome e idade formatados
    # print(i['link'])








class MlSpiderone(scrapy.Spider):
    name = "mlp"
    #allowed_domains = ["mercadolivre.com"]
    #start_urls = ["https://www.mercadolivre.com.br/impressora-a-cor-multifuncional-hp-deskjet-ink-advantage-2774-com-wifi-preta-100v240v/p/MLB17509710?pdp_filters=official_store:2972%7Ccategory:MLB1648#searchVariation=MLB17509710&position=15&search_layout=grid&type=product&tracking_id=cb661e23-b999-424d-a091-0751f4223d85"]
    
    start_urls = [dados[1]['link']]

    #print(start_urls)

    #exit(9)



    def parse(self, response, **kwargs):
        #for i in response.xpath('//li[@class="ui-search-layout__item"]'):
        for i in response.xpath('//div[@class="ui-pdp-container ui-pdp-container--pdp"]'):

            var = response.request.url
            #codigo = re.findall(r"(MLB[0-9]{5,})",var)
            codigo = re.findall(r"((MLB)(-)?([0-9]{5,}))",var)
            

            #url = i.xpath('.//div[@class="nav-header-plus-cp-wrapper nav-area nav-bottom-area nav-left-area"]/a/@href').get

            price = i.xpath('.//div[@class="ui-pdp-price__second-line"]/span/span[3]/text()').get()
            title = i.xpath('.//div[@class="ui-pdp-header__title-container"]/h1/text()').get()
            #if i.xpath('.//div[@class="ui-pdp-buybox__quantity mb-12"]//span[4]/text()').get() == null:
            #disponivel = i.xpath('.//div[@class="ui-pdp-buybox__quantity"]//span[4]/text()').get() if i.xpath('.//div[@class="ui-pdp-buybox__quantity"]//span[4]/text()').get() != None else i.xpath('.//div[@class="ui-pdp-buybox__quantity mb-12"]//span[4]/text()').get()


            disponivel = i.xpath('.//*[@id="quantity-selector"]/span/span[4]/text()').get() if i.xpath('.//*[@id="quantity-selector"]/span/span[4]/text()').get() != None else i.xpath('.//div[@class="ui-pdp-buybox__quantity mb-12"]//span[4]/text()').get()

            #else:
            #disponivel2 = i.xpath('.//div[@class="ui-pdp-buybox__quantity mb-12"]//span[4]/text()').get()
            
            yield{
                'codigo' : codigo[0][0],
                'price' : price,
                'title' : title,
                'disponivel' : disponivel
            }

            #next_page = response.xpath('//a[contains(@title,"Seguinte")]/@href').get()
            #if next_page:
            #    yield scrapy.Request(url=next_page, callback=self.parse)

            for i in dados:
                next_page = i['link']
                yield scrapy.Request(url=next_page, callback=self.parse)



class SavingToMysqlPipeline(object):

    def __init__(self):
            self.create_connection()
    
    def create_connection(self):
            self.connection = mysql.connector.connect(
                 host = 'localhost',
                 user = 'root',
                 password = 'vertrigo',
                 database = 'monitoramento',
                 port = '3306'
            )
