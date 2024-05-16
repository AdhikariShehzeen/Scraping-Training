# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import urllib.request
from scrapy.exceptions import DropItem


class BooksToScrapePipeline:
    def process_item(self, item, spider):
        if 'image' in item:
            image_url = item['image']
            folder_path = 'images'
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            
            # Extracting the image name from the URL
            image_name = os.path.basename(image_url)
            
            # Constructing the path where the image will be saved
            image_path = os.path.join(folder_path, image_name)
            
            try:
                # Downloading the image
                urllib.request.urlretrieve(image_url, image_path)
                # Adding the downloaded image path to the item
                item['image_path'] = image_path
            except Exception as e:
                
                raise DropItem("Failed to download image at %s : %s" % (image_url, str(e)))
        
        return item
       
