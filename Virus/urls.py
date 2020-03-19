"""Virus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from apscheduler.scheduler import Scheduler
from django.urls import path
from Virus_s import models
import json
import pymysql
import urllib.request as r
import ssl
import time
ssl._create_default_https_context = ssl._create_unverified_context
from Virus_s import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'',views.index),
    path(r'rumors/',views.rumors),
    path(r'mapchoose/',views.mapchoose),
    path(r'returnindex/',views.index),
    path(r'hubeichoose/',views.hubeichoose),
    path(r'news/',views.news),
    path(r'newschoose/',views.newschoose),
    path(r'rumorschoose/',views.rumorschoose)
]
sched = Scheduler()  # 实例化，固定格式
@sched.interval_schedule(seconds=200,max_instances=10)
def mytask():
    getoverall()
    time.sleep(1)
    getprovince()
    time.sleep(1)
    getcity()
    time.sleep(1)
    getwuhan()
    time.sleep(1)
    getrumors()
    time.sleep(1)
    getnews()
    time.sleep(1)
    gethubei()
    time.sleep(1)
sched.start()  # 启动该脚本


def getoverall():
    print("getoverall()ing")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/overall?latest=0', headers=headers)
    response = r.urlopen(req)
    data_json_overall = json.load(response)
    for item in data_json_overall['results']:
        if models.overall.objects.filter(updatetime=item['updateTime']).exists():
            pass
        else:
            try:
                models.overall.objects.create(currentConfirmedCount = item['currentConfirmedCount'],confirmedCount = item['confirmedCount'],
                                              suspectedCount = item['suspectedCount'],curedCount = item['curedCount'],
                                              deadCount = item['deadCount'],seriousCount =item['seriousCount'],
                                              currentConfirmedIncr = item['currentConfirmedIncr'],confirmedIncr = item['confirmedIncr'],
                                              suspectedIncr = item['suspectedIncr'], curedIncr = item['curedIncr'],
                                              deadIncr = item['deadIncr'],seriousIncr = item['seriousIncr'],
                                              generalRemark = item['generalRemark'],abroadRemark = item['abroadRemark'],
                                              remark1 = item['remark1'],remark2 = item['remark2'],remark3 = item['remark3'],remark4=item['remark4'],
                                              remark5= item['remark5'],note1=item['note1'],note2=item['note2'],note3=item['note3'],updatetime=item['updateTime'])
                print("overallchenggong!")
            except KeyError:
                pass
def getprovince():
    print("getprovince()ing")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/area', headers=headers)
    response_area = r.urlopen(req)
    data_json_city_name = json.load(response_area)
    for item in data_json_city_name['results']:
        if models.City.objects.filter(locationId =item['locationId']).exists():
            try:
                models.City.objects.filter(locationId =item['locationId']).update(currentConfirmedCount = item['currentConfirmedCount'],
                                                                                  confirmedCount=item['confirmedCount'],
                                                                                  suspectedCount = item['suspectedCount'],
                                                                                  curedCount=item['curedCount'],
                                                                                  deadCount = item['deadCount'])
            except KeyError:
                pass

        else:
            try:
                models.City.objects.create(locationId = item['locationId'],continentName = item['continentName'],
                                           continentEnglishName = item['continentEnglishName'],countryName = item['countryName'],
                                           countryEnglishName = item['countryEnglishName'],provinceName = item['provinceName'],
                                           provinceShortName = item['provinceShortName'],provinceEnglishName = item['provinceEnglishName'],
                                           currentConfirmedCount = item['currentConfirmedCount'],confirmedCount=item['confirmedCount'],
                                           suspectedCount = item['suspectedCount'],curedCount=item['curedCount'],
                                           deadCount = item['deadCount'])
                print("Citychenggong")
            except KeyError:
                pass
def getcity():
    print("getcity()ing")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/area', headers=headers)
    response_area = r.urlopen(req)
    data_json_city_name = json.load(response_area)
    for item1 in data_json_city_name['results']:
        if item1['cities'] is None:
            pass
        else:
            for item2 in item1['cities']:
                if item2['cityName'] == "未明确地区" or item2['cityName'] == "待明确地区":
                    pass
                else:
                    if models.AreaCity.objects.filter(locationId=item2['locationId']).exists():
                        models.AreaCity.objects.filter(locationId=item2['locationId']).update(currentConfirmedCount = item2['currentConfirmedCount'],
                                                                                              confirmedCount = item2['confirmedCount'],suspectedCount = item2['suspectedCount'],
                                                                                              curedCount = item2['curedCount'],deadCount = item2['deadCount'])
                    else:
                        try:
                            models.AreaCity.objects.create(cityName = item2['cityName'],currentConfirmedCount = item2['currentConfirmedCount'],
                                                       confirmedCount = item2['confirmedCount'],suspectedCount = item2['suspectedCount'],
                                                       curedCount = item2['curedCount'],deadCount = item2['deadCount'],
                                                       locationId = item2['locationId'],cityEnglishName = item2['cityEnglishName'],
                                                       provinceName = item1['provinceName'])
                            print("areacitychenggong")
                        except KeyError:
                            pass

def getwuhan():
    print("getwuhan()ing")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/area?latest=0&province=%E6%B9%96%E5%8C%97%E7%9C%81', headers=headers)
    response_wuhan = r.urlopen(req)
    data_json_city_name = json.load(response_wuhan)
    for item1 in data_json_city_name['results']:
        if models.wuhan.objects.filter(updateTime=item1['updateTime']).exists():
            pass
        else:
            try:
                for item2 in item1['cities']:
                    if item2['cityName'] == "武汉":
                        try:
                            # if models.wuhan.objects.filter(updateTime=item1['updateTime']).exists():
                            #     pass
                            # else:
                            models.wuhan.objects.create(cityName = item2['cityName'],currentConfirmedCount = item2['currentConfirmedCount'],
                                                            confirmedCount = item2['confirmedCount'],suspectedCount = item2['suspectedCount'],
                                                            curedCount = item2['curedCount'] , deadCount = item2['deadCount'],locationId = item2['locationId'],
                                                            cityEnglishName = item2['cityEnglishName'],updateTime=item1['updateTime'])
                            print("wuhanchenggong")
                        except KeyError:
                            pass
            except:
                pass


def getrumors():
    print("getrumor()ing")
    # for rumortype in [0,1,2]:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/rumors', headers=headers)
    response_rumors = r.urlopen(req)
    data_json_rumors = json.load(response_rumors)
    for item in data_json_rumors['results']:
        if models.rumors.objects.filter(rumorsid=item['_id']).exists():
            pass
        else:
            try:
                models.rumors.objects.create(title=item['title'],
                                             mainSummary=item['mainSummary'],
                                             body=item['body'],
                                             rumorType=item['rumorType'],
                                             rumorsid=item['_id'])
                print("rumorschenggong!")
            except KeyError:
                pass
    time.sleep(1)


def getnews():
    print("getnews()ing")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/news', headers=headers)
    response_news = r.urlopen(req)
    data_json_news = json.load(response_news)
    for item in data_json_news['results']:
        if models.news.objects.filter(title=item['title']).exists():
            pass
        else:
            try:
                models.news.objects.create( title= item['title'],
                                              summary= item['summary'],
                                              infoSource= item['infoSource'],
                                              sourceUrl = item['sourceUrl'],
                                              pubDate=item['pubDate'],
                                              provinceName=item['provinceName'],
                                              provinceId=item['provinceId'])
                print("newschenggong!")

            except KeyError:
                pass

def gethubei():
    print("gethubei()ing")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = r.Request(url='https://lab.isaaclin.cn/nCoV/api/area?latest=0&province=%E6%B9%96%E5%8C%97%E7%9C%81', headers=headers)
    response_hubei = r.urlopen(req)
    data_json_hubei= json.load(response_hubei)
    for item in data_json_hubei['results']:
        if models.hubei.objects.filter(updatetime=item['updateTime']).exists():
            pass
        else:
            try:
                models.hubei.objects.create(provinceName=item['provinceName'],
                                            provinceShortName=item['provinceShortName'],
                                            provinceEnglishName=item['provinceEnglishName'],
                                            currentConfirmedCount=item['currentConfirmedCount'],
                                            confirmedCount=item['confirmedCount'],
                                            suspectedCount=item['suspectedCount'],
                                            curedCount=item['curedCount'],
                                            deadCount=item['deadCount'],
                                            updatetime=item['updateTime'])
                print("hubeichenggong!")
            except KeyError:
                pass
