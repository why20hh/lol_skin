# coding:utf-8
import requests
from pyquery import PyQuery
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from lxml import etree
import os


class Lol:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('https://101.qq.com/#/hero')
        self.hero_name_list = []
        self.hero_list = []

    def get_name_cover(self):
        sleep(3)
        source = self.driver.page_source
        doc = PyQuery(source)
        items = doc('.hero-list>li').items()
        for item in items:
            hero_url = item.find('a').attr('href')
            hero_url = 'https://101.qq.com/' + hero_url
            self.hero_list.append(hero_url)
            name = item.find('p').text()
            self.hero_name_list.append(name)
            url = item.find('img').attr('src')
            url = 'http:' + url
            url_content = requests.get(url).content
            with open('./pic/' + name + '.jpg', 'wb') as file:
                file.write(url_content)
                print(f'正在下载{name}-----{url}')
        print('全部数据下载完毕')
        print('开始下载所有皮肤')
        sleep(3)
        self.get_skin()

    def get_skin(self):
        for i in self.hero_list:
            index = self.hero_list.index(i)  # 用英雄名字来创建文件夹
            print(f'开始下载--{self.hero_name_list[index]}')
            self.driver.get(i)
            sleep(2)
            if len(self.driver.find_elements(By.XPATH, '//*[@id="app"]/div[2]/div/div/div/a[1]')) != 0:
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div/div/a[1]').click()
                sleep(1)
                self.driver.find_element(By.XPATH,'//*[@id="app"]/div/div[3]/div/div[2]/div[2]/div[1]/div[2]/a[7]').click()
            else:
                self.driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div/div[2]/div[2]/div[1]/div[3]/a[7]').click()
            sleep(2)
            skin_source = self.driver.page_source
            parse_html = etree.HTML(skin_source)
            get_hero_skin_name = parse_html.xpath('//*[@class="swiper-wrapper"]/div/img/@alt')
            hero_skin_num = len(get_hero_skin_name) // 3
            get_hero_skin_url = parse_html.xpath('//*[@class="swiper-wrapper"]/div/img/@src')[-hero_skin_num:]
            get_hero_skin_name = get_hero_skin_name[-hero_skin_num:]
            path = f'./skin/{self.hero_name_list[index]}/'
            for down in range(hero_skin_num):
                self.down_hero_skin(get_hero_skin_name[down], get_hero_skin_url[down], path)
            sleep(2)  # 暂停两秒然后继续下一次循环
        print('所有皮肤数据下载完成')

    def down_hero_skin(self, name, url, path):
        if os.path.exists(path) is False:
            os.makedirs(path)
        skin_content = requests.get(url).content
        name = name.replace('/', '／')
        with open(path + name + '.jpg', 'wb') as file:
            file.write(skin_content)
            print(f'正在下载{name}-----{url}')

a = Lol()
a.get_name_cover()
