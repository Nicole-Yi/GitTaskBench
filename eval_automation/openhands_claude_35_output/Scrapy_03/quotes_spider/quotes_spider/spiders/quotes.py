import scrapy
import xml.etree.ElementTree as ET
from xml.dom import minidom


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/tag/humor/"]

    def parse(self, response):
        root = ET.Element("quotes")
        
        for quote in response.css("div.quote"):
            quote_elem = ET.SubElement(root, "quote")
            
            text = quote.css("span.text::text").get()
            author = quote.css("small.author::text").get()
            tags = quote.css("div.tags a.tag::text").getall()
            
            text_elem = ET.SubElement(quote_elem, "text")
            text_elem.text = text
            
            author_elem = ET.SubElement(quote_elem, "author")
            author_elem.text = author
            
            tags_elem = ET.SubElement(quote_elem, "tags")
            for tag in tags:
                tag_elem = ET.SubElement(tags_elem, "tag")
                tag_elem.text = tag
        
        # 格式化XML输出
        xml_str = minidom.parseString(ET.tostring(root, encoding='utf-8')).toprettyxml(indent="    ", encoding='utf-8')
        
        # 保存到文件
        with open("/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_03/output.xml", "wb") as f:
            f.write(xml_str)