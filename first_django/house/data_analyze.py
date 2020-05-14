import os
import matplotlib.pyplot as plt
import numpy as np
from locale import LC_NUMERIC, setlocale, atof, atoi

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plt.rcParams['font.sans-serif']=['WenQuanYi Zen Hei'] 


def histogram(kind, place_id, place_name, num_list, name_list):
    fig_name = base_dir + f'/static/images/{kind}_images/histogram/{place_id}.png'
    print(fig_name)
    print(num_list)
    print(name_list)
    if not os.path.exists(fig_name):
        for rect in plt.bar(name_list, num_list):
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2.0 - 0.2, 1.03 * height, '%s' % int(height))
        plt.title(place_name + '房价柱状图')
        plt.savefig(fig_name)


def peichart():
    pass
    

if __name__ == "__main__":
    setlocale(LC_NUMERIC, 'en_US.UTF-8')
    num_list = ['13,750', '13,614', '11,331', '10,548', '10,366', '10,017', '9,566', '9,244', '8,722', '7,666', '7,608']
    name_list = ['廊坊', '石家庄', '唐山', '沧州', '保定', '承德', '秦皇岛', '邯郸', '张家口', '衡水', '邢台']
    histogram('province', 5, '广东', list(map(atoi, num_list)), name_list)