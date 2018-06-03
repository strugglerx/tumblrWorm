import os
import requests
import threading





def download(url,name):
    global headers
    filename=os.getcwd() + '/video/'+name
    print(filename)

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    if  not os.path.exists(filename):
        try:
            video=requests.get(url,headers=headers).content
            #print(video.url)
            with open(filename,'wb')as f:
                f.write(video)
        except:
            pass
    else:
        print('视频已下载了！')


def getfile():
    files = os.listdir(os.getcwd())
    data = []
    for each in files:
        if not os.path.isdir(each) and 'txt' in each:
            data.append(each)
    return data

def geturl(filename):
    with open(filename, 'r')as f:
        data = f.readlines()

    for each in data:
        line = each.replace('\n', '').split(':', 1)[1]
        name = line.split('/')[-1] + '.mp4'
        print(line)
        download(line, name)



def main():
    videos=getfile()
    filename = 'video'
    if not os.path.exists(filename):
        os.mkdir(filename)
    for each in videos:
        t=threading.Thread(target=geturl,args=[each,])
        t.start()
        #t.join()
    #geturl(videos)

if __name__=='__main__':
    main()






