from django.shortcuts import render
from Virus_s import models
import json
import ssl
import time
import heapq
import re
from django.db.models import Max
ssl._create_default_https_context = ssl._create_unverified_context
# Create your views here.
def index(request):
    # 确诊人数
    table_province = models.City.objects.filter(countryName = "中国")
    list= []
    for item in table_province:
        result = {'name': item.provinceShortName,'value':item.currentConfirmedCount}
        list.append(result)
    table_city = models.AreaCity.objects.all()
    for item in table_city:
        if  item.cityName.find("区")<0 and item.cityName != "恩施州" and item.cityName.find("市")<0:
            item.cityName=item.cityName+"市"
            result_1 = {'name':item.cityName,'value':item.currentConfirmedCount}
            list.append(result_1)
        elif item.cityName == "恩施州":
            item.cityName ="恩施土家族苗族自治州"
            result_1 = {'name': item.cityName, 'value': item.currentConfirmedCount}
            list.append(result_1)
        else:
            result_1 = {'name': item.cityName, 'value': item.currentConfirmedCount}
            list.append(result_1)
    list = json.dumps(list)
    #新闻
    table_news_time = models.news.objects.values_list("pubDate")
    table_news_top10 = heapq.nlargest(10, table_news_time)
    list_temp = []
    for temp in table_news_top10:
        number=re.findall(r'\d',str(temp))
        mid = ""
        for a in number:
            mid = mid+a
        list_temp.append(mid)
    table_news_all = models.news.objects.values("title","pubDate","sourceUrl")
    list_news=[]
    for item in table_news_all:
        if item['pubDate'] in list_temp:
            a=float(item['pubDate'])/1000
            time_return=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))
            result_news={'title':item['title'],'sourceUrl':item['sourceUrl'],'time':time_return}
            list_news.append(result_news)
    # 谣言
    table_rumors_id = models.rumors.objects.values_list("rumorsid")
    list_temp = []
    for temp in table_rumors_id:
        number = re.findall(r'\d', str(temp))
        mid = ""
        for a in number:
            mid = mid + a
        list_temp.append(int(mid))
    table_rumors_top10 = heapq.nlargest(10, list_temp)
    table_rumors_all = models.rumors.objects.values("title","mainSummary","rumorType","rumorsid")
    list_rumors=[]
    result_rumors={}
    for item in table_rumors_all:
        if int(item['rumorsid']) in table_rumors_top10:
            if item['rumorType'] == "0":
                result_rumors = {'title':item['title'],'maninSummary':item['mainSummary'],'rumorType':"谣言"}
            elif item['rumorType'] == "1":
                result_rumors = {'title':item['title'],'maninSummary':item['mainSummary'],'rumorType':"可信信息"}
            if item['rumorType'] == "2":
                result_rumors = {'title':item['title'],'maninSummary':item['mainSummary'],'rumorType':"尚未证实"}
            list_rumors.append(result_rumors)
    #6大数据
    pubdate=models.overall.objects.all().aggregate(Max('updatetime'))
    table_shuju = models.overall.objects.values("currentConfirmedCount","suspectedCount","seriousCount","confirmedCount","curedCount","deadCount","updatetime")
    result_shuju={}
    for item in table_shuju:
        if pubdate['updatetime__max'] == item['updatetime']:
            result_shuju = {'currentCofirmedCount':item['currentConfirmedCount'],'seriousCount':item['seriousCount'],
                            'suspectedCount':item['suspectedCount'],'confirmedCount':item['confirmedCount'],'curedCount':item['curedCount'],
                            'deadCount':item['deadCount']}
    #表格
    table_hubei = models.hubei.objects.all().order_by('updatetime')
    list_time=[]
    list_shuzhi=[]
    for item in table_hubei:
        a = float(item.updatetime) / 1000
        time_return = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))[5:]
        list_time.append(time_return)
        list_shuzhi.append(int(item.currentConfirmedCount))
    list_shuzhi = json.dumps(list_shuzhi)
    list_time = json.dumps(list_time)
    return render(request,'index.html',{'list':list,'list_news':list_news,'list_rumors':list_rumors,'result':result_shuju,'list_time':list_time,'list_shuzhi':list_shuzhi})



def mapchoose(request):
    if request.method=='POST':
        choose = request.POST.get('choose',None)
        if choose == "治愈率":
            table_province = models.City.objects.filter(countryName="中国")
            list = []
            for item in table_province:
                temp =float(item.curedCount)/float(item.confirmedCount)
                result = {'name': item.provinceShortName, 'value': temp}
                list.append(result)
            table_city = models.AreaCity.objects.all()
            for item in table_city:
                if item.cityName.find("区") < 0 and item.cityName != "恩施州" and item.cityName.find("市") < 0:
                    item.cityName = item.cityName + "市"
                    temp = float(item.curedCount) / float(item.confirmedCount)
                    result_1 = {'name': item.cityName, 'value': temp}
                    list.append(result_1)
                elif item.cityName == "恩施州":
                    item.cityName = "恩施土家族苗族自治州"
                    temp = float(item.curedCount) / float(item.confirmedCount)
                    result_1 = {'name': item.cityName, 'value': temp}
                    list.append(result_1)
                else:
                    temp = float(item.curedCount) / float(item.confirmedCount)
                    result_1 = {'name': item.cityName, 'value': temp}
                    list.append(result_1)
            list = json.dumps(list)
            tishi = json.dumps("治愈率")
            color_tishi = json.dumps('#00ff00')
            return render(request,'moremap.html',{'list':list,'tishi':tishi,'color':color_tishi})
        elif choose == "死亡率":
            table_province = models.City.objects.filter(countryName="中国")
            list = []
            for item in table_province:
                temp = float(item.deadCount) / float(item.confirmedCount)
                result = {'name': item.provinceShortName, 'value': temp}
                list.append(result)
            table_city = models.AreaCity.objects.all()
            for item in table_city:
                if item.cityName.find("区") < 0 and item.cityName != "恩施州" and item.cityName.find("市") < 0:
                    item.cityName = item.cityName + "市"
                    temp = float(item.deadCount) / float(item.confirmedCount)
                    result_1 = {'name': item.cityName, 'value': temp}
                    list.append(result_1)
                elif item.cityName == "恩施州":
                    item.cityName = "恩施土家族苗族自治州"
                    temp = float(item.deadCount) / float(item.confirmedCount)
                    result_1 = {'name': item.cityName, 'value': temp}
                    list.append(result_1)
                else:
                    temp = float(item.deadCount) / float(item.confirmedCount)
                    result_1 = {'name': item.cityName, 'value': temp}
                    list.append(result_1)
            list = json.dumps(list)
            tishi = json.dumps("死亡率")
            color_tishi = json.dumps('#ff0000')
            return render(request, 'moremap.html', {'list': list,'tishi':tishi,'color':color_tishi})
def hubeichoose(request):
    if request.method=='POST':
        choose = request.POST.get('choose',None)
        if choose == "全国感染人数":
            table_overall = models.overall.objects.all().order_by('updatetime')
            list_time = []
            list_shuzhi = []
            for item in table_overall:
                a = float(item.updatetime) / 1000
                time_return = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))[5:]
                list_time.append(time_return)
                list_shuzhi.append(int(item.currentConfirmedCount))
            list_shuzhi = json.dumps(list_shuzhi)
            list_time = json.dumps(list_time)
            tishi1 = json.dumps("全国近期感染情况")
            tishi2 = json.dumps("感染人数")
            return render(request,'morehubei.html',{'list_time':list_time,'list_shuzhi':list_shuzhi,'tishi1':tishi1,'tishi2':tishi2})
        elif choose == "武汉感染人数":
            table_wuhan = models.wuhan.objects.all().order_by('updateTime')
            list_time = []
            list_shuzhi = []
            for item in table_wuhan:
                a = float(item.updateTime) / 1000
                time_return = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))[5:]
                list_time.append(time_return)
                list_shuzhi.append(int(item.currentConfirmedCount))
            list_shuzhi = json.dumps(list_shuzhi)
            list_time = json.dumps(list_time)
            tishi1 = json.dumps("武汉近期感染情况")
            tishi2 = json.dumps("感染人数")
            return render(request, 'morehubei.html',
                          {'list_time': list_time, 'list_shuzhi': list_shuzhi, 'tishi1': tishi1, 'tishi2': tishi2})
        elif choose == "全国治愈人数":
            table_overall = models.overall.objects.all().order_by('updatetime')
            list_time = []
            list_shuzhi = []
            for item in table_overall:
                a = float(item.updatetime) / 1000
                time_return = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))[5:]
                list_time.append(time_return)
                list_shuzhi.append(int(item.curedCount))
            list_shuzhi = json.dumps(list_shuzhi)
            list_time = json.dumps(list_time)
            tishi1 = json.dumps("全国近期治愈情况")
            tishi2 = json.dumps("治愈人数")
            return render(request, 'morehubei.html',
                          {'list_time': list_time, 'list_shuzhi': list_shuzhi, 'tishi1': tishi1, 'tishi2': tishi2})
        elif choose == "湖北治愈人数":
            table_hubei = models.hubei.objects.all().order_by('updatetime')
            list_time = []
            list_shuzhi = []
            for item in table_hubei:
                a = float(item.updatetime) / 1000
                time_return = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))[5:]
                list_time.append(time_return)
                list_shuzhi.append(int(item.curedCount))
            list_shuzhi = json.dumps(list_shuzhi)
            list_time = json.dumps(list_time)
            tishi1 = json.dumps("湖北近期湖北情况")
            tishi2 = json.dumps("治愈人数")
            return render(request, 'morehubei.html',
                          {'list_time': list_time, 'list_shuzhi': list_shuzhi, 'tishi1': tishi1, 'tishi2': tishi2})
        elif choose =="武汉治愈人数":
            table_wuhan = models.wuhan.objects.all().order_by('updateTime')
            list_time = []
            list_shuzhi = []
            for item in table_wuhan:
                a = float(item.updateTime) / 1000
                time_return = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a))[5:]
                list_time.append(time_return)
                list_shuzhi.append(int(item.curedCount))
            list_shuzhi = json.dumps(list_shuzhi)
            list_time = json.dumps(list_time)
            tishi1 = json.dumps("武汉近期治愈情况")
            tishi2 = json.dumps("治愈人数")
            return render(request, 'morehubei.html',
                          {'list_time': list_time, 'list_shuzhi': list_shuzhi, 'tishi1': tishi1, 'tishi2': tishi2})
def rumors(request):
    rutab0 = models.rumors.objects.filter(rumorType=0)
    rutab1 = models.rumors.objects.filter(rumorType=1)
    rutab2 = models.rumors.objects.filter(rumorType=2)
    temp0 = "【谣言：已辟谣】"
    temp2 = "【信息：已证实】"
    temp1 = "【信息：未证实】"
    return render(request, 'rumors.html', {'table0': rutab0,'table1':rutab1,'table2':rutab2,'temp0':temp0,'temp1':temp1,'temp2':temp2})


def news(request):
    list_province = models.news.objects.values_list('provinceName', flat=True)
    temp=[]
    for item in list_province:
        if item not in temp:
            temp.append(item)
    news_all = models.news.objects.all()
    return render(request,'news.html',{'temp':temp,'news_all':news_all})


def newschoose(request):
    if request.method=='POST':
        list_province = models.news.objects.values_list('provinceName', flat=True)
        temp = []
        for item in list_province:
            if item not in temp:
                temp.append(item)
        choose = request.POST.get('choose', None)
        news_all = models.news.objects.filter(provinceName = choose)
        return render(request,'news.html',{'temp':temp,'news_all':news_all})

def rumorschoose(request):
    if request.method=='POST':
        choose =request.POST.get('choose',None)
        if choose == "谣言":
            rutab0 = models.rumors.objects.filter(rumorType=0)
            temp = "【谣言：已辟谣】"
            return render(request, 'rumors.html', {'table0': rutab0,'table1':None,'table2':None,'temp0':temp})
        elif choose =="可信信息":
            rutab2 = models.rumors.objects.filter(rumorType=2)
            temp = "【信息：已证实】"
            return render(request, 'rumors.html', {'table2': rutab2,'table0':None,'table1':None,'temp2':temp})
        elif choose =="未证实信息":
            rutab1 = models.rumors.objects.filter(rumorType=1)
            temp = "【信息：未证实】"
            return render(request, 'rumors.html', { 'table1': rutab1,'table2':None,'tabale0':None,'temp1':temp})