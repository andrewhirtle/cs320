# project: p3
# submitter: ahirtle
# partner: none
# hours: 6
import os, zipfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import time

class GraphScraper:
    def __init__(self):
        self.visited = set()
        self.BFSorder = []
        self.DFSorder = []

    def go(self, node):
        raise Exception("must be overridden in sub classes -- don't change me here!")

    def dfs_search(self, node):
        children = self.go(node)
        self.visited.add(node)
        for child in children:
            if child not in self.visited:
                self.dfs_search(child)

    def bfs_search(self, node):
        todo = [node]
        while len(todo) > 0:
            curr = todo.pop(0)
            if curr not in self.visited:
                children = self.go(curr)
                self.visited.add(curr)
                for x in children:
                    if x not in self.visited:
                        todo.append(x)

class FileScraper(GraphScraper):
    def __init__(self):
        super().__init__()
        if not os.path.exists("Files"):
            with zipfile.ZipFile("files.zip") as zf:
                zf.extractall()

    def go(self, node):
        with open(os.path.join('Files','{}.txt'.format(node))) as f:
            data = f.read()
            rows = data.split('\n')
            children = rows[1].split(' ')
            bfs = rows[2].split(' ')[1]
            dfs = rows[3].split(' ')[1]
            self.BFSorder.append(bfs)
            self.DFSorder.append(dfs)
        return children
    
    
class WebScraper(GraphScraper):
    # required
    def	__init__(self, driver=None):
        super().__init__()
        self.driver = driver

    # these three can be done as groupwork
    def go(self, url):
        self.driver.get(url)
        if url not in self.visited:
            dfs_btn = self.driver.find_element_by_id('DFS')
            clicked = dfs_btn.click()
            dfs_val = self.driver.find_element_by_id('DFS')
            self.DFSorder.append(dfs_val.text)
            bfs_btn = self.driver.find_element_by_id('BFS')
            clicked = bfs_btn.click()
            bfs_val = self.driver.find_element_by_id('BFS')
            self.BFSorder.append(bfs_val.text)
            self.visited.add(url)
        children = self.driver.find_elements_by_tag_name('a')
        links = []
        for child in children:
            if child.get_attribute('href') not in self.visited:
                links.append(child.get_attribute('href'))
        return links

    def dfs_pass(self, start_url):
        self.visited = set()
        self.DFSorder = []
        self.dfs_search(start_url)
        final = ''
        return final.join(self.DFSorder)

    def bfs_pass(self, start_url):
        self.visited = set()
        self.BFSorder = []
        self.bfs_search(start_url)
        final = ''
        return final.join(self.BFSorder)

    # write the code for this one individually
    def protected_df(self, url, password):
        self.driver.get(url)
        pwd = self.driver.find_element_by_id('password-input')
        pwd.clear()
        pwd.send_keys(password)
        btn = self.driver.find_element_by_id('attempt-button')
        btn.click()
        time.sleep(1)
        add_btn = self.driver.find_element_by_id('more-locations-button')
        for x in range(20):
            add_btn.click()
            time.sleep(.005)
        table = pd.read_html(self.driver.page_source)
        return table[0]