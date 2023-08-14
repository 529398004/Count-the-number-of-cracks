import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

DataDir = r""
extension = "*.dat"
start_line = "ball data ..."
start_line_contact = "contact data ..."
start_line_bond = "bond data ..."
my_list = []#放小球坐标，内涵多部字典，每部字典代表一个文件中的数据
my_contact = []#放粘接，内涵多个列表，每个列表代表一个文件中裂缝的数据
my_bond = []#放裂缝，内涵多个列表，每个列表代表一个文件中的粘接
#遍历该路径下所有的后缀名为.dat的文件
for file_path in glob.glob(os.path.join(directory, extension)):
    my_list_xy = {}
    my_list_contact = []
    my_list_bond = []
    i = 0
    with open(file_path, 'r') as file:
        content = file.readlines()
        start_index = content.index(start_line + '\n') if start_line + '\n' in content else None
        if start_index is not None:
            for line in content[start_index + 3:]:
                if line.strip() == '':
                    break
                else:
                    columns = line.strip().split()
                    my_list_xy[columns[1]] = columns[2:4]

        start_index = content.index(start_line_contact + '\n') if start_line_contact + '\n' in content else None
        if start_index is not None:
            for line in content[start_index + 2:]:
                if line.strip() == '':
                    break
                else:
                    columns = line.strip().split()
                    my_list_contact.append(columns[0:2])

        start_index = content.index(start_line_bond + '\n') if start_line_bond + '\n' in content else None
        if start_index is not None:
            for line in content[start_index + 2:]:
                if line.strip() == '':
                    break
                else:
                    columns = line.strip().split()
                    my_list_bond.append(columns[0:2])

    my_list.append(my_list_xy)
    my_contact.append(my_list_contact)
    my_bond.append(my_list_bond)

num = [] #新生成的裂缝数量。
#计算每移动一千米新生成的裂缝。
sampleOfContact = []
#创建figure窗口，figsize设置窗口的大小

for i in range(len(my_contact)):
    if i == 0:
        sampleOfContact = my_contact[0]
    else:
        numofcontact = 0
        current_contact = my_contact[i]
        previous_contact = my_contact[:i]
        fig, ax = plt.subplots(figsize=(40, 10))
        ax.plot([1, 61.2], [0.9, 0.9], color='black', linewidth=2.0)
        ax.plot([61.3, 61.3], [1, 15], color='black', linewidth=2.0)
        for item in current_contact:
            if all(item not in prev_contact for prev_contact in previous_contact):
                numofcontact = numofcontact + 1
                id1 = float(item[0])
                id2 = float(item[1])
                x1 = float(my_list[i][str(int(id1))][0]) / 1000
                y1 = float(my_list[i][str(int(id1))][1]) / 1000
                x2 = float(my_list[i][str(int(id2))][0]) / 1000
                y2 = float(my_list[i][str(int(id2))][1]) / 1000
                # print(str(id1) + ' ' + str(x1) + ' ' + str(y1))
                # print(str(id2) + ' ' + str(x2) + ' ' + str(y2))
                ax.plot([i+0.9, i+0.9], [1, 15], color='black', linewidth=2)
                ax.plot([x1, x2], [y1, y2], color='r')
            #设置坐标轴范围
            ax.set_aspect('equal')
            ax.minorticks_on()
            ax.set_xlim(0, 64)
            ax.set_ylim(0, 16)
            # ax.xaxis.set_tick_params(rotation=45, labelsize=18, colors='w')
            # start, end = ax.get_xlim()
            # ax.xaxis.set_ticks(np.arange(start, end, 1))
        # 显示出所有设置
        plt.show()
        num.append(numofcontact)
		
		
# 裂缝波浪图
# x = np.array(list(range(1000, 21000, 1000)))
# y = np.array(num)
# x_new = np.linspace(x.min(), x.max(), 100) # 创建新的x轴数据
# spl = make_interp_spline(x, y, k=3) # 创建一个三次插值的B样条对象
# y_smooth = spl(x_new) # 根据新的x轴数据生成新的y轴数据
# # 绘制原始数据点和平滑后的曲线
# plt.scatter(x, y, label='Original Data') # 绘制散点图
# plt.plot(x_new, y_smooth, label='Smooth Curve') # 绘制make_interp_spline函数生成的曲线
# plt.legend() # 显示图例
# plt.show() # 显示图像