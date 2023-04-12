from json import JSONDecodeError
import cv2, os, requests, shutil, time, io, csv, numpy, json
from ids import table

temptable = []
for b in range(0, len(table)):
    temptable.insert(b, table[b])
    if b % 100 == 0 or len(table) < 100:
        def getdata(temptabl):
            output = io.StringIO()
            csv.writer(output, quoting=csv.QUOTE_NONNUMERIC).writerow(temptabl)
            output.getvalue()
            url = f"https://thumbnails.roblox.com/v1/badges/icons?badgeIds={str(output.getvalue()).rstrip()}&size=150x150&format=Png&isCircular=false"
            return url
        data = requests.get(getdata(temptable)).json()['data']
        for s in range(0, len(data)):
            try:
                data[s]
            except:
                print("Error.... retrying")
                time.sleep(5)
                data = requests.get(getdata(temptable)).json()['data']
            lol = requests.get(data[s]['imageUrl'])
            try:
                json.loads(lol.text)
            except JSONDecodeError:
                data[s]
            else:
                print("Error.... retrying")
                time.sleep(5)
                data = requests.get(getdata(temptable)).json()['data']
        for i in range(0,len(data)):
            if data[i]['state'] == 'Completed':
                def downloadimg(i, date):
                    image_url = date[i]['imageUrl']
                    id = date[i]['targetId']
                    filename = f"{id}.png"
                    time.sleep(.5)
                    r = requests.get(image_url, stream = True)
                    if r.status_code == 200:
                        r.raw.decode_content = True
                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
                    try:
                        img.shape[:2]
                    except:
                        downloadimg(i, data)
                    else:
                        if img.shape[:2] != (150,150):
                            print(f"{id} is a square badge!")
                        elif img.shape[:2] == (150,150):
                            quards = []
                            for i in range(0, 149+1):
                                quards.append(numpy.array(img[i][i]).tolist())
                            try:
                                img[i][i][3]
                            except IndexError:
                                print(f"{id} may be a square badge")
                            if [0,0,0,0] in quards:
                                print(f"{id} is not a square badge")
                                os.remove(filename)
                            else:
                                print(f"{id} is a square badge!")
                downloadimg(i, data)
        while temptable:
            temptable.pop()