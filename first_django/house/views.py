import json
import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.db.models import Count
from time import time
from locale import LC_NUMERIC, setlocale, atof, atoi

from . import models
from . import data_analyze


# Create your views here.
# 首页
def index(request):
    data = {}
    data['top_info'] = {
        'index': 'active',
        'top100': '',
        'search': '',
        'analyze': ''
    }
    return render(request, 'index.html', data)


# 房价分析
def analyze(request):
    # 使用locale模块来转换字符串和数字
    setlocale(LC_NUMERIC, 'en_US.UTF-8')
    data = {}
    data['top_info'] = {
        'index': '',
        'top100': '',
        'search': '',
        'analyze': 'active'
    }
    if 'province' in request.GET and 'city' not in request.GET:
        """ 选择栏中的数据显示"""
        data['type'] = 1
        data['provinces'] = models.Province.objects.exclude(p_name__in=['北京', '上海', '重庆', '天津'])
        data['province_id'] = request.GET['province']
        data['select_province'] = data['provinces'][int(request.GET['province']) - 5]

        """获取选中的省份的城市的房价信息"""
        cities = data['select_province'].city_set.all()
        name_list = [city.c_name for city in cities]
        num_list = [city.c_price for city in cities]
        yoy_num_list = [atof(city.c_yoy[:-1]) for city in cities]
        mom_num_list = [atof(city.c_mom[:-1]) for city in cities]
        yoy_increase = cities.filter(c_yoy__startswith='+').aggregate(increase=Count('c_yoy'))
        yoy_decrease = cities.filter(c_yoy__startswith='-').aggregate(decrease=Count('c_yoy'))
        mom_increase = cities.filter(c_mom__startswith='+').aggregate(increase=Count('c_mom'))
        mom_decrease = cities.filter(c_mom__startswith='-').aggregate(decrease=Count('c_mom'))

        """将统计好的数据传给数据分析模块并生成数据统计图"""
        data_analyze.histogram('province', data['select_province'].id, 
                data['select_province'].p_name, list(map(atoi, num_list)), name_list)
        data_analyze.histogram_changes('province', data['select_province'].id,
                data['select_province'].p_name, yoy_num_list, mom_num_list, name_list)
        data_analyze.piechart('province', 0, data['select_province'].id, 
                data['select_province'].p_name, yoy_increase, yoy_decrease)
        data_analyze.piechart('province', 1, data['select_province'].id, 
                data['select_province'].p_name, mom_increase, mom_decrease)

    elif 'province' in request.GET and 'city' in request.GET:
        data['type'] = 2
        data['provinces'] = models.Province.objects.exclude(p_name__in=['北京', '上海', '重庆', '天津'])
        data['province_id'] = request.GET['province']
        data['city_id'] = request.GET['city']
        data['cities'] = data['provinces'][int(request.GET['province']) - 5].city_set.all()
        data['select_city'] = data['cities'][int(request.GET['city'])]
        print(request.GET['city'])
    return render(request, 'analyze.html', data)


# 房价查询
def search(request):
    setlocale(LC_NUMERIC, 'en_US.UTF-8')
    data = {}
    data['status'] = False
    data['top_info'] = {
        'index': '',
        'top100': '',
        'search': 'active',
        'analyze': ''
    }
    if request.method == 'POST':
        t = int(request.POST['range'])
        place = request.POST['place']
        data['searched'] = True
        if t == 1:
            province = models.Province.objects.filter(p_name=place).first()
            if province:
                cities = province.city_set.all()
                data['place'] = (place + '省')
                data['type'] = '1'
                for i in range(len(cities)):
                    cities[i].id = i + 1
                    cities[i].name = cities[i].c_name
                    cities[i].price = cities[i].c_price
                    cities[i].mom = cities[i].c_mom
                    cities[i].yoy = cities[i].c_yoy
                data['areas'] = cities
        elif t == 2:
            city = models.City.objects.filter(c_name=place).first()
            if city:
                urbanareas = city.urbanarea_set.all()
                data['place'] = (place + '市')
                data['type'] = '2'
                for i in range(len(urbanareas)):
                    urbanareas[i].id = i + 1
                    urbanareas[i].name = urbanareas[i].u_name
                    urbanareas[i].price = urbanareas[i].u_price
                    urbanareas[i].mom = urbanareas[i].u_mom
                    urbanareas[i].yoy = urbanareas[i].u_yoy
                data['areas'] = urbanareas
    return render(request, 'search.html', data)


# 查找房价前100的城市和区县
def top100(request):
    data = {}
    data['top_info'] = {
        'index': '',
        'top100': 'active',
        'search': '',
        'analyze': ''
    }
    sql = 'select * from house_city ' \
        'order by cast(c_price as unsigned) desc limit 100'     #使用原生语句进行查询
    cities = models.City.objects.raw(sql)
    for i in range(len(cities)):
        cities[i].no = i + 1
    data['cities'] = cities
    sql = 'select * from house_urbanarea ' \
        'order by cast(u_price as unsigned) desc limit 100'
    urbanareas = models.UrbanArea.objects.raw(sql)
    for i in range(len(urbanareas)):
        urbanareas[i].no = i + 1
    data['urbanareas'] = urbanareas
    return render(request, 'top100.html', data)