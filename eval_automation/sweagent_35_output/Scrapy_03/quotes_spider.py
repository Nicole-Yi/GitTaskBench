
import urllib.request
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom

def scrape_quotes():
    url = 'https://quotes.toscrape.com/tag/humor/'
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode('utf-8')
        
        # Create XML structure
        root = ET.Element('quotes')
        
        # Find all quotes using regex
        quote_pattern = r'<div class="quote".*?<span class="text".*?>(.*?)</span>.*?<small class="author".*?>(.*?)</small>.*?<div class="tags">(.*?)</div>'
        quotes = re.finditer(quote_pattern, html, re.DOTALL)
        
        for quote_match in quotes:
            quote = ET.SubElement(root, 'quote')
            
            # Get text
            text = quote_match.group(1).strip()
            text_elem = ET.SubElement(quote, 'text')
            text_elem.text = text
            
            # Get author
            author = quote_match.group(2).strip()
            author_elem = ET.SubElement(quote, 'author')
            author_elem.text = author
            
            # Get tags
            tags_html = quote_match.group(3)
            tags_elem = ET.SubElement(quote, 'tags')
            tag_pattern = r'<a class="tag".*?>(.*?)</a>'
            for tag_match in re.finditer(tag_pattern, tags_html):
                tag_elem = ET.SubElement(tags_elem, 'tag')
                tag_elem.text = tag_match.group(1).strip()
        
        # Create pretty XML string
        xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
        
        # Write to file
        with open('/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/Scrapy_03/output.xml', 'w', encoding='utf-8') as f:
            f.write(xml_str)
            
        print("Successfully scraped quotes and saved to XML file.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    scrape_quotes()