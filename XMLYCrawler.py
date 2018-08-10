import requests
import json
import os
#from lxml import etree  #可实现xpath

# 抓取喜马拉雅音频文件 网址：https://www.ximalaya.com/top/
class XiMa(object):
    def __init__(self,bookName,bookId):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
            }
        self.startUrl = "https://www.ximalaya.com/revision/play/album?albumId={}&pageNum=1&sort=-1&pageSize=30".format(int(bookId)) #当前是指定频道的第一页数据
        self.bookName = bookName

    # 获取当前频道资源列表
    def getSource(self):
        r = requests.get(self.startUrl,headers=self.headers)
        result = r.content.decode()
        jsonResult = json.loads(result)
        dataList = jsonResult['data']['tracksAudioPlay']
        sourceList=[]
        for item in dataList:
            source={}
            source['name']=item['trackName']
            source['src']=item['src']
            sourceList.append(source)
        #print(sourceList)
        return sourceList

    # 保存音频文件
    def saveSource(self,sources):
        #bookName =str(self.bookName).replace('"',' ')  # ??未起作用
        path='F:\\Python练习\\喜马拉雅音频\\'+bookName
        isExistd=os.path.exists(path)
        # 判断文件夹是否存在
        if not isExistd:
            os.makedirs(path)

        for item in sources:
            print('开始抓取文件[' +item['name']+ ']...')
            filePath = path+'\{}.m4a'.format('['+bookName+']'+item['name']) 
            # 判断文件是否存在
            if os.path.exists(filePath):
                print("已存在！无需下载")
                continue

            # 以二进制格式打开
            f=open(filePath,'ab')
            r=requests.get(item['src'],headers=self.headers)
            f.write(r.content)
            f.close()
            print('文件[' +item['name']+ ']抓取结束')

    # 执行方法
    def runFun(self):
        sourceList=self.getSource()
        self.saveSource(sourceList)

# 获取所有频道信息
def getAllPDList():
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    mainUrl="https://www.ximalaya.com/revision/rank/getRankList?rankType=freeAlbum&pageSize=100" # 顶级入口目录
    r=requests.get(mainUrl,headers=headers)
    result=r.json()
    dataList=result['data']['freeAlbumRank']['rankListInfo']
    dataSources=[]
    for data in dataList:
        dataSource={}
        dataSource['id']=data['id']
        dataSource['title']=data['albumTitle']
        dataSources.append(dataSource)
    return dataSources


# 调用入口
if __name__=='__main__':
    #xima=XiMa('吴晓波频道',15273276)
    #xima.runFun()

    allSources = getAllPDList()
    #print(allSources)
    for source in allSources:
        xima=XiMa(source['title'],source['id'])
        xima.runFun()


