import os
import matplotlib.pyplot as plt
import numpy as np
from locale import LC_NUMERIC, setlocale, atof, atoi

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']


def histogram(kind, place_id, place_name, num_list, name_list):
    fig_name = base_dir + \
        f'/static/images/{kind}_images/histogram/sample/{place_id}.png'
    fig = plt.figure(figsize=(len(num_list), 7))
    for rect in plt.bar(name_list, num_list):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0 -
                 0.2, 1.03 * height, '%s' % int(height))
    plt.title(place_name + '房价总览')
    plt.savefig(fig_name)


def histogram_changes(kind, place_id, place_name, num_list1, num_list2, name_list):
    fig_name = base_dir + \
        f'/static/images/{kind}_images/histogram/mom_yoy/{place_id}.png'

    if not os.path.exists(fig_name):
        fig = plt.figure(figsize=(18, 7))
        name = name_list
        y1 = num_list1
        y2 = num_list2
        print(y1)
        print(y2)
        print(name_list)

        x = np.arange(len(name))
        width = 0.25

        plt.bar(x, y1,  width=width, label='同比', color='darkorange')
        plt.bar(x + width, y2, width=width, label='环比',
                color='deepskyblue', tick_label=name)

        # 显示在图形上的值
        for a, b in zip(x, y1):
            plt.text(a, b+0.1, b, ha='center', va='bottom')
        for a, b in zip(x, y2):
            plt.text(a+width, b+0.1, b, ha='center', va='bottom')

        plt.xticks()
        plt.legend(loc="upper left")  # 防止label和图像重合显示不出来
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.ylabel('value')
        plt.xlabel('line')
        plt.title(f'{place_name}地区的房间变化情况')
        plt.savefig(fig_name)


def piechart(kind, kind_t, place_id, place_name, increase, decrease):
    fig_name = base_dir + \
        f'/static/images/{kind}_images/piechart/{kind_t}_{place_id}.png'
    if not os.path.exists(fig_name):
        fig = plt.figure()
        name_list = ['增长', '下降']
        num_list = [increase['increase'], decrease['decrease']]
        colors = ['g', 'r']
        plt.pie(num_list, labels=name_list, autopct='%1.1f%%',
                shadow=False, colors=colors)
        title = f'{place_name}地区房价同比变化情况' if kind_t else f'{place_name}地区房价环比变化情况'
        plt.title(title)
        plt.savefig(fig_name)


if __name__ == "__main__":
    setlocale(LC_NUMERIC, 'en_US.UTF-8')
    num_list = ['13,750', '13,614', '11,331', '10,548', '10,366',
                '10,017', '9,566', '9,244', '8,722', '7,666', '7,608']
    name_list = ['廊坊', '石家庄', '唐山', '沧州', '保定',
                 '承德', '秦皇岛', '邯郸', '张家口', '衡水', '邢台']
    histogram('province', 5, '广东', list(map(atoi, num_list)), name_list)
