import requests
import json
import re
import os
import sys
import random
import time
import threading


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def allInfo(select,num=10):

    url="https://{}.tumblr.com/api/read/json?start=0&num={}".format(select,num)
    print(url)
    html = requests.get(str(url), headers=headers).text
    #html=requests.get(str(url),headers=headers,verify=False).text
    #print(html[22:-2])
    data=json.loads(str(html[22:-2]))
    '''
    with open('./{}.json'.format(select), 'w')as f:
        f.write(str(data))
    '''
    return data["posts"]

def downLoad(data,select):
    selectDir=os.getcwd()
    videoLine=''
    for i in range(len(data)):
        if data[i]["type"] =='video':

            video=data[i]["video-player-500"]

            videoName = data[i]["slug"]
            p=r'<source src="(.*?)" type="video/mp4">'
            results=re.findall(p,str(video)) #results[0]为正则匹配出的视频链接

            try:
                videoLine +=videoName+':'+results[0]+'\n'
                '''
                video=requests.get(results[0],headers=headers).content
                with open('./info.mp4','wb')as f:
                    f.write(video)
                '''
            except:
                print('错误已忽略！')
        elif data[i]["type"] == 'photo':
            photos = data[i]["photos"]
            fileDir = data[i]["slug"]
            findName = selectDir+'/{}/{}'.format(select,fileDir)


            if len(photos)!=0 :
                if not os.path.exists(findName) and len(fileDir)!=0:
                    print('正在获取'+fileDir)
                    os.makedirs(findName)
                else:
                    fileDir="无题"+str(random.randint(0,233))
                    dirName = os.getcwd() + '/{}/{}'.format(select, fileDir)
                    if not os.path.exists(dirName):
                        os.makedirs(dirName)

                for each in photos:

                    #print(each["photo-url-1280"])
                    imgUrl = each["photo-url-1280"]
                    fileName = imgUrl.split('/')[-1]
                    Dir=os.getcwd()+'/{}/{}/{}'.format(select,fileDir,fileName)
                    if os.path.exists(Dir):
                        print(fileDir+'资源已获取啦！')
                        break
                    else:
                        imgData = requests.get(imgUrl, headers=headers).content
                        with open(Dir, 'wb')as f:
                            f.write(imgData)
            else:
                imgUrl=data[i]["photo-url-1280"]
                #print(imgUrl)
                fileName = imgUrl.split('/')[-1]
                Dir=os.getcwd()+'/{}/{}'.format(select,fileName)
                if os.path.exists(Dir):
                    print('资源已获取啦！')
                else:
                    imgData = requests.get(imgUrl, headers=headers).content
                    with open(Dir, 'wb')as f:
                        f.write(imgData)


    with open('./{}.txt'.format(select), 'w')as f:
        f.write(str(videoLine))
    print('某个账户数据已获取完毕')
    #os.chdir("../")

'''
with open('./info.json','w')as f:
    f.write(str(data))
'''

def conf():
    with open('worm.conf','r')as f:
        num=json.loads(f.readline())['count']

    return num
def brain(select,num):
    if select != "":

        if not os.path.exists(select):
            os.mkdir(select)

        data = allInfo(select, num)
        downLoad(data, select)
    else:
        print('请输入正确参数')


def main():

    sys.argv.pop(0)
    num = conf()
    date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    print('start time:'+date)
    fileName = '采集库'
    #print(len(sys.argv))
    if len(sys.argv)>0:
        if not os.path.exists(fileName):
            os.mkdir(fileName)

        os.chdir(fileName)
        for i in range(len(sys.argv)):
            select = sys.argv[i]
            print(select)
            # select='hxm04,freegirl7788,treenew-bee,jessesonjin ,lovelyporngif'
            t = threading.Thread(target=brain, args=(select, num,))
            t.start()
            print('end')
    else:
        print('参数错误！')



if __name__=="__main__":
    main()

