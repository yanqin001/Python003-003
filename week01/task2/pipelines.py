# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Task2Pipeline:
    def process_item(self, item, spider):
        title = item['title']
        mytype = item['mytype']
        onlinedate = item['onlinedate']
        output = f'|{title}|\t|{mytype}|\t{content}|\n\n'
        with open('./mydy.txt','a+',encoding='utf-8') as article:
            article.write(output)
        return item