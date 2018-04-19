# _*_ coding:utf-8 _*_
import sys, httplib, time, sgmllib,urllib, urllib2,os


class SpeedHTML(sgmllib.SGMLParser):

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.status = 0
        self.td = 1
        self.in_tag = 0
        self.ipAddr = []
        self.ipData = []

    def parse(self, s):
        self.feed(s)
        self.close()

#====================== 处理td标签以获得IP地址

    def start_script(self, attributes):
        for name, value in attributes:
            if name == "type" and value == "text/javascript":
                self.status = 1
                self.in_tag = self.in_tag + 1


    def end_tr(self):
        self.status = 0

#========================== tag_p

#========================== 处理td标签以获得流量的字节数

    # def start_td(self, attributes):
    #     for name, value in attributes:
    #         if name == "width" and value == "91":
    #             #因为有两个td标签是width = 85 的,所以这里特殊处理一下
    #             self.td = self.td + 1
    #             self.status = 2
    #             self.in_tag = 1
    #
    # def end_p(self):
    #     self.status = 0

#============================ tag_td
    def handle_data(self, data):
        if self.status == 1 and self.in_tag == 1:
            i=2
            data=data.encode('utf-8')
            self.in_tag = 8
            while 1:
                temp=data.split('\n')[i].split(',')
                i = i+1
                if temp[1] == '0 );':
                    break

                self.ipAddr.append(temp[1])
                self.ipData.append(int(temp[3]))
             # self.in_tag = 1

        # if self.status == 2 and self.in_tag == 1 and self.td % 2 == 0:
        #     self.ipData.append(int(data))
        #     self.in_tag = 0


    def get_ipAddr(self):
        return self.ipAddr

    def get_ipData(self):
        return self.ipData

print "test starting...."

headers = {
    "Accept":"*/*",
    "Referer":"http://192.168.1.1/",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows MT 5.1; SV1; .NET CLR 2.0.50727)",
    "Host": "192.168.1.1",
    "Connection": "Keep-Alive",
    "Authorization": "Basic YWRtaW46YWRtaW4="
    #因为登陆路由器网页需要密码,所以有 Authorization 这一项
    #使用这个项目就不用urllib2里面的那个HTTPBasicAuthHandler 类了
    #这些数据由网络抓包来的数据中来的
}

# router = urllib.urlopen('http://admin:admin@192.168.1.1')
# print 'http header:/n', router.info()
# print 'http status:', router.getcode()
# print 'url:', router.geturl()
# for line in router:
#     print line.decode("cp936"),
# router.close()

# response = urllib2.urlopen('http://192.168.1.1:80')
# html = response.read()
# print html
# req = urllib2.Request("http://baidu.com")
# response = urllib2.urlopen(req)
# html = response.read()
# print html

# url = 'http://192.168.1.1'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# values = {'name' : 'admin','password':'admin'}
# headers = { 'User-Agent' : user_agent}
# data = urllib.urlencode(values)
# req = urllib2.Request(url, data, headers)
# response = urllib2.urlopen(req)
# the_page = response.read()

# url = 'http://www.baidu.com/s'
# values = {'wd':'D_in'}
# data = urllib.urlencode(values)
# print data
# url2 = url+'?'+data
# response = urllib2.urlopen(url2)
# the_page = response.read()
# print the_page


while 1:
    ipAddr = []
    ipData = []
    result = []
    oneKB = float(1024)
    oneMB = oneKB * oneKB
    oneGB = oneKB * oneMB
    #每隔2秒获取一次数据,共获取两次
    for i in range(0, 2):
        con1 = httplib.HTTPConnection("192.168.1.1")
        con1.request("GET", "/userRpm/SystemStatisticRpm.htm?Num_per_page=20", "", headers)
        r1 = con1.getresponse()

        if r1.status == 200:
            # r1.read(3796) #前面有一部分数据完全没有用,所以预读一下忽略掉它
            d = r1.read(1024).encode('gb2312') #开始有用的数据
            d=d.split('\n')
            i = 2
            while 1:

                if d[i] == '0,0 );':
                    break
                statList = d[i].split(',')
                print "IP: ",statList[1].split('"')[1],"MAC: ",statList[2].split('"')[1],
                statList[3] = int(statList[3])
                statList[4] = int(statList[4])
                statList[5] = int(statList[5])
                statList[6] = int(statList[6])
                if (statList[3] < oneMB):
                    tmp = statList[3] / oneKB
                    string = "KB"
                elif (statList[3] < oneGB):
                    tmp = statList[3] / oneMB
                    string = "MB"
                else:
                    tmp = statList[3] / oneGB
                    string = "GB"
                print "下载/上传流量:  ",(str(round(tmp,2)) + string).ljust(10),

                if (statList[4] < oneMB):
                    tmp = statList[4] / oneKB
                    string = "KB"
                elif (statList[4] < oneGB):
                    tmp = statList[4] / oneMB
                    string = "MB"
                else:
                    tmp = statList[4] / oneGB
                    string = "GB"
                print (str(round(tmp,2)) + string).ljust(10),

                if (statList[5] < oneMB):
                    tmp = statList[5] / oneKB
                    string = "KB/s"
                elif (statList[5] < oneGB):
                    tmp = statList[5] / oneMB
                    string = "MB/s"
                else:
                    tmp = statList[5] / oneGB
                    string = "GB/s"

                print "下载/上传速度:  ",(str(round(tmp,2)) + string).ljust(10),

                if (statList[6] < oneMB):
                    tmp = statList[6] / oneKB
                    string = "KB/s"
                elif (statList[6] < oneGB):
                    tmp = statList[6] / oneMB
                    string = "MB/s"
                else:
                    tmp = statList[6] / oneGB
                    string = "GB/s"
                print (str(round(tmp,2)) + string).ljust(10)

                i = i + 1
    #         sg = SpeedHTML()
    #         sg.feed(d)
    #
    #         ipAddr = sg.get_ipAddr()
    #         ipData.append(sg.get_ipData())
    #
    #     con1.close()

        print "==================================================================================================================================="
        con1.close()
        time.sleep(2)
    # for i in range(0, len(ipAddr)):
    #     #计算刚才获取数据那段时间的流量,单位: kb/s
    #     result.append((ipData[1][i] - ipData[0][i]) / 4 / 1000)
    #     print "IP:  ", ipAddr[i], " is ", result[i], " kb/s "
    #     os.system('cls')

