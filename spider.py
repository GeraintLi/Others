import requests
import re
import os
import numpy as np

dir = './pic2/'
base_url = 'https://www.xiaozhu2.com/shijiazhuang/buycar/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
i = 1
for j in np.arange(15)+2:
    url = base_url + 'p' + str(j) + '.html'
    response = requests.get(url,headers=headers)
    response.encoding = 'utf-8'
    t = '<img class="b-lazy" alt="(.*?)" data-src="(.*?)" src="(.*?)"'
    imgs = re.findall(t,response.text)
    for img in imgs:
        print(img[1])
        data_src = img[1]
        img_obj = requests.get(data_src,headers=headers)
        with open(dir+'pic'+str(i)+'.jpg','wb') as f:
            f.write(img_obj.content)
        i = i+1

    
