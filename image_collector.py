import requests
import shutil
import pickle
from bs4 import BeautifulSoup

def main():
    hwc_downloader()

def height_weight_chart():
    source = requests.get('https://height-weight-chart.com/').text
    soup = BeautifulSoup(source, "html.parser")
    chart = soup.find('chart')
    links = []
    for span in chart.children:
        if (not hasattr(span,'children')):
            continue
        for link in span.children:
            if (not hasattr(link,'attrs') or not 'href' in link.attrs):
                continue
            links.append(link.attrs['href'])

    download_links = []
    for link in links:
        print('checking: https://height-weight-chart.com/' +  link)
        source = requests.get('https://height-weight-chart.com/' + link).text
        soup = BeautifulSoup(source,'html.parser')
        imgs = soup.findAll('img',{'class':'largepic'})
        if imgs is None:
            continue
        for img in imgs:
            download_links.append('https://height-weight-chart.com/' + img.attrs['src'])

    with open('data','wb') as f:
        pickle.dump(download_links, f)

def hwc_downloader():
    with open('data','rb') as f:
        download_links = pickle.load(f)

    counter = 969
    for link in download_links:
        r = requests.get(link)
        ndata = link[34:41]
        print(counter)
        name = '{:04d}'.format(counter) + 'h' + str(int(int(ndata[0]) * 30.48 + int(ndata[1:3]) * 2.54)) + 'w' + \
            str(int(int(ndata[4:7]) * 0.453592))  + '.jpg'
        with open('./height-weight-charts/'+name, 'wb') as out_file:
            # shutil.copyfileobj(r.raw, out_file)
            out_file.write(r.content)
        counter += 1







main()