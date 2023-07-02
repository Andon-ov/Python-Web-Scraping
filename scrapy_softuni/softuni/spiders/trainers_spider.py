import scrapy

class TrainersSpider(scrapy.Spider):
    name = 'trainers'
    allowed_domains = ['softuni.bg']
    start_urls = ['https://softuni.bg/trainers']

    def parse(self, response):
        for trainer in response.css('.trainers-page-content-trainer-info'):
            id = trainer.css('.trainers-page-content-trainer-info::attr(data-id)').get()

            name = trainer.css('.trainers-page-content-trainer-name::text').get().strip()
            position = trainer.css('.trainers-page-content-trainer-occupation::text').get().strip()
            info = trainer.css(f'#{id} .trainings-page-content-trainer-info-modal-description::text').get().strip()
            info = info.replace('\n', '').replace('            ', ' ')

            yield {
                'Name': name.strip(),
                'Position': position.strip(),
                'Info': info.strip(),
            }


 # import scrapy

# class TrainersSpider(scrapy.Spider):
#     name = 'trainers'

#     allowed_domains = ['softuni.bg']
#     start_urls = ['https://softuni.bg/trainers']

#     def parse(self, response):
#         for trainer in response.css('.trainers-page-content-trainer-info'):

#             id = trainer.css('.trainers-page-content-trainer-info::attr(data-id)').get()

#             yield {
#                 'name': trainer.css('.trainers-page-content-trainer-name::text').get(),
#                 'position': trainer.css('.trainers-page-content-trainer-occupation::text').get(),
#                 'info': trainer.css(f'#{id} .trainings-page-content-trainer-info-modal-description::text').get(),
#             }
           