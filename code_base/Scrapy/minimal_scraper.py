import requests
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
import os

url = "https://quotes.toscrape.com/tag/humor/"
output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_03"
os.makedirs(output_dir, exist_ok=True)

response = requests.get(url)
root = Element('quotes')

for quote in response.html.find('div.quote'):
    quote_elem = SubElement(root, 'quote')
    SubElement(quote_elem, 'author').text = quote.find('span small', first=True).text
    SubElement(quote_elem, 'text').text = quote.find('span.text', first=True).text
    tags_elem = SubElement(quote_elem, 'tags')
    for tag in quote.find('div.tags a.tag'):
        SubElement(tags_elem, 'tag').text = tag.text

xml_str = parseString(tostring(root)).toprettyxml()
with open(os.path.join(output_dir, 'output.xml'), 'w') as f:
    f.write(xml_str)