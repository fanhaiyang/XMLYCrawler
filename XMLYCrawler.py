import requests
import json

# 抓取喜马拉雅音频文件
class XiMa(object):
    def __init__(self,bookName):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
            }
        self.startUrl = "https://www.ximalaya.com/revision/play/album?albumId=269179&pageNum=1&sort=-1&pageSize=30"
        self.bookName = bookName

    # 获取资源列表
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
        for item in sources:
            print('开始抓取文件[' +item['name']+ ']...')
            # 以二进制格式打开
            file=open('F:\\Python练习\\喜马拉雅音频\{}.m4a'.format('['+self.bookName+']'+item['name']),'ab')
            r=requests.get(item['src'],headers=self.headers)
            file.write(r.content)
            file.close()
            print('文件[' +item['name']+ ']抓取结束')

    # 执行方法
    def runFun(self):
        sourceList=self.getSource()
        self.saveSource(sourceList)


# 调用入口
if __name__=='__main__':
    xima=XiMa('吴晓波频道')
    xima.runFun()

