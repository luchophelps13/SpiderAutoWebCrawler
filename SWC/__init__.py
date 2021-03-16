import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import io
from PIL import Image

class AutoWebScraper:

    def __init__(self, URL):
        self.URL = URL

        HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}
        global r
        r = requests.get(URL, headers=HEADERS)
        global soup
        soup = bs(r.text, "html.parser")



    def find_element_by_class(self, cls, get_text):

        '''Find any element by CSS class. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        elem = soup.find(class_ = cls)

        if get_text == True:
            return elem.text
        else:
            return elem

    def find_elements_by_class(self, cls, get_text):

        '''Find any elements by class. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        elems = soup.find_all(class_ = cls)

        if get_text == True:
            for elem in elems:
                print(elem.text)
        else:
            for elem in elems:
                print(elem)

    def find_element(self, tag, get_text):

        '''Find any element by <tag>. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        if get_text == True:
            return soup.find(tag).text
        else:
            return soup.find(tag)

    def find_elements(self, tag, get_text):

        '''Find any elements by <tag>. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        if get_text == True:
            for elem in soup.find_all(tag):
                print(elem.text)
        else:
            for elem in soup.find_all(tag):
                print(elem)
        
    def find_element_by_id(self, ID, get_text):

        '''Find any element by ID. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        elem = soup.find(id = ID)

        if get_text == True:
            return elem.text
        else:
            return elem

    def find_element_by_full_xpath(self, xpath, get_text):

        '''Find any element by XPATH. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        elems = xpath.split("/")
        if elems[0] == "":
            elems = elems[1:]

        for i in range(len(elems)):
            elem = soup.find(elems[i])

        if get_text == True:
            return elem.text
        else:
            return elem


    def get_footer(self, get_text):

        '''Returns the footer, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        if get_text == True:
            return soup.find("footer").text 
        else:
            return soup.find("footer")

    def get_header(self, get_text):

        '''Returns the header, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        if get_text == True:
            return soup.find("header").text 
        else:
            return soup.find("header")

    def get_headings(self, get_text):

        '''Returns the heading, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        headings = soup.find_all(re.compile('^h[1-6]$'))

        if get_text == True:
            for heading in headings:
                return heading.text
        else:
            return headings

    def get_images(self, KEYWDS=""):

        '''Returns the images, if possible. The key_words paramter is used if the user want to filter images by their src. **CASE SENSITIVE**'''


        imgs = soup.find_all("img")
        for img in imgs:
            img_list = [] 
            img_list.append(img['src'])
            for i in range(len(img_list)):
                if img_list[i][0:7] == "/static":
                    img_list.pop(i)
                else:
                    if img_list[i][0:5] != "http:": ##MAKE SURE URL IS VALID
                        if img_list[i][0:2] == "//":
                            img_list[i] = "https:" + img_list[i]
                        else:
                            img_list[i] = "https://" + img_list[i]
                    
  
                    if KEYWDS != "":
                        if isinstance(KEYWDS, list):  # NOW THAT THE URL IS VALID, CHECK FOR TYPE OF KEYWDS
                            if any(KEYWDS in img_list[i] for KEYWDS in img_list[i]): #IF THE URL DOES CONTAIN THE KEYWRD, ELSE DROP THE IMG FROM THE LIST
                                try:
                                    response = requests.get(img_list[i])
                                    image_bytes = io.BytesIO(response.content)
                                    img = Image.open(image_bytes)
                                    img.show()
                                except:
                                    img_list[i] = "https://" + img_list[i][7:]
                            else:
                                img_list.pop(i)
                        else: #IF IT'S JUST A STRING (e.g. "Bob")
                            if KEYWDS not in img_list[i]:
                                img_list.pop(i)
                            else:

                                response = requests.get(img_list[i])
                                image_bytes = io.BytesIO(response.content)
                                img = Image.open(image_bytes)
                                img.show()
                                
                    else:
                        try:
                            response = requests.get(img_list[i])
                            image_bytes = io.BytesIO(response.content)
                            img = Image.open(image_bytes)
                            img.show()
                        except:
                            print("Image cannot be found.") 


    def get_images_src(self, get_text):
        
        '''Returns the <img>'s src attribute, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        if get_text == True:
            for img in soup.find_all("img"):
                print(img["src"])
        else:
            return soup.find_all("img")

    def get_links(self, get_text):

        '''Returns the <a> tags and their href attribute, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        links = soup.find_all("a")
        hrefs = soup.find_all("a", href=True)

        if get_text == True:
            for link in links:
                for href in hrefs:
                    print(f"Link:, '{link.text.strip()}', HREF:, {href.text.strip()} \n")

        else:
            for link in links:
                for href in hrefs:
                    print(f"Link:, '{link}', HREF:, {href} \n")

    def get_navbar(self, get_text):

        '''Returns the navbar, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        nav = soup.find("nav")

        if get_text == True:
            return re.sub(r'[\r\t]', '', nav.text)
        else:
            return nav

    def get_paragraphs(self, get_text):

        '''Returns the <p> tags, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        pars = soup.find_all("p")

        if get_text == True:
            for par in pars:
                print(par.text)
        else:
            for par in pars:
                print(par)

    def get_spans(self, get_text):

        '''Returns the <span> tags, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        spans = soup.find_all("span")

        if get_text == True:
            for span in spans:
                print(span.text)
        else:
            return spans

    def get_title(self, get_text):

        '''Returns the <title> tag, if possible. The get_text parameter determines whether the user wants the text from the element (if possible) or the tag + text.'''

        if get_text == True:
            return soup.find("title").text
        else:
            return soup.find("title")

    def get_tables(self):

        '''Returns all of the tables, will raise error if none are found.'''

        return pd.read_html(r.text)

    def get_table(self, index):

        '''Returns the table of the index provided.'''

        return pd.read_html(r.text)[index]
