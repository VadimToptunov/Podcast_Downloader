from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
import time
import os


class PodcastDownloader:
    def grab_podcast_urls(self, podname, episodes_link, minrange, maxrange, step, attributes):
        """
        Parses podcast's download urls.
        """
        for item in range(minrange, maxrange, step):
            url = f"{episodes_link}{item}"
            self.grab_links(podname, url, attributes)

    def grab_dataskeptic_urls(self, minrange, maxrange, step, attributes):
        browser = webdriver.Chrome(r".\chromedriver.exe")
        for item in range(minrange, maxrange, step):
            url = f"http://dataskeptic.com/podcast?year={item}&limit=10&offset=30"
            browser.get(url)
            browser.set_window_position(-2000, 0)
            time.sleep(30)
            self.grab_links("dataskeptic", url, attributes)
            browser.quit()

    def grab_podcast_urls_pfm(self, podname):
        browser = webdriver.Chrome(r".\chromedriver.exe")
        url = f"https://player.fm/series/{podname}"
        browser.get(url)
        browser.set_window_position(-2000, 0)
        time.sleep(30)
        self.grab_links(podname, url, {'href': re.compile("http.*\.mp3")})
        browser.quit()

    def grab_links(self, podname, url, attributes):
        pod_links = []
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, "html.parser")
        podcast_links = soup.find_all("a", attrs=attributes)
        unique = set(podcast_links)
        for _ in unique:
            link = _.get('href')
            print(link)
            pod_links.append(link)

        for url_pod in pod_links:
            dirname = f".\\{podname}_podcasts"
            self.download_podcast(dirname, url_pod)

    def download_podcast(self, dirname, url_pod):
        """
        Downloads podcast's episodes to a specific folder.
        :return:
        """
        r = requests.get(url_pod, allow_redirects=True)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        else:
            pass
        filename, file_extension = os.path.splitext(os.path.basename(url_pod))
        print(f"File {filename}.mp3 is going to be downloaded.")
        open(f"{dirname}\\{filename}.mp3", 'wb').write(r.content)