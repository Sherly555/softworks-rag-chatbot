import requests
from bs4 import BeautifulSoup
from pathlib import Path
URL = "https://www.softworkstech.com/"
def collect_website_text():
    print("Collecting Data")
    response=requests.get(
        URL,
        timeout=30,
        headers={"User-Agent":"Mozilla/5.0"}
    )
    response.raise_for_status()
    
    soup=BeautifulSoup(response.text,"html.parser")
    
    text=soup.get_text(separator="\n",strip=True)
    Path("data/softworks.txt").write_text(
        text,
        encoding="utf-8"
    )
    print("Website text saved to data/softworks.txt")
    print("Characters collected:", len(text))
if __name__=="__main__":
    collect_website_text()
