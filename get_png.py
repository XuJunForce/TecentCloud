import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号

# 数据
data = {
    'Server': ['S8', 'S8', 'SA4', 'SA4'],
    'Client_Count': [50, 75, 50, 75],
    'Input_Mb_Average': [0.085, 0.10, 0.085, 0.105],
    'Input_Mb_EMA': [0.005, 0.01, 0.005, 0.0],
    'Input_Mb_Maximum': [0.17, 0.185, 0.19, 0.87],
    'Output_Mb_Average': [4.225, 6.385, 4.33, 6.48],
    'Output_Mb_EMA': [0.59, 0.65, 0.09, 0.02],
    'Output_Mb_Maximum': [18.545, 24.15, 20.585, 28.99],
    'RTT_95th_Percentile(ms)': [96.5, 104.125, 96.575, 113.625],
    'RTT_Average(ms)': [92.595, 90.48, 84.465, 92.62],
    'RTT_EMA(ms)': [94.965, 93.865, 88.4, 81.1],
    'RTT_Maximum(ms)': [125.5, 127.0, 114.0, 128.0],
    'RTT_Minimum(ms)': [62.5, 61.0, 53.0, 48.0]
}

# 将数据转换为DataFrame
df = pd.DataFrame(data)

# 定义性能指标分类，删除EMA相关指标
rtt_metrics = [
    'RTT_Average(ms)',
    'RTT_95th_Percentile(ms)',
    'RTT_Maximum(ms)',
    'RTT_Minimum(ms)'
]

input_metrics = [
    'Input_Mb_Average',
    'Input_Mb_Maximum'
]

output_metrics = [
    'Output_Mb_Average',
    'Output_Mb_Maximum'
]

# 创建输出目录（当前目录）
output_dir = os.getcwd()

# 定义颜色和标签
color_map = {
    'SA4-50': 'skyblue',
    'SA4-75': 'navy',
    'S8-50': 'salmon',
    'S8-75': 'darkred'
}

labels = ['SA4-50', 'SA4-75', 'S8-50', 'S8-75']

# 准备数据
metrics_categories = {
    'RTT': rtt_metrics,
    'Input': input_metrics,
    'Output': output_metrics
}

# 设置图表样式
plt.style.use('ggplot')

def plot_category(category_name, metrics, filename):
    """
    生成指定类别的柱状图并保存为PNG文件。

    参数：
    - category_name: 类别名称（如 'RTT', 'Input', 'Output'）
    - metrics: 该类别下的性能指标列表
    - filename: 保存的文件名
    """
    plt.figure(figsize=(12, 8))
    
    x = np.arange(len(metrics))  # 每个类别的指标数量
    total_width = 0.8
    num_bars = len(labels)
    bar_width = total_width / num_bars
    offsets = np.linspace(-total_width/2 + bar_width/2, total_width/2 - bar_width/2, num_bars)
    
    for i, label in enumerate(labels):
        server, client = label.split('-')
        client = int(client)
        # 选择对应的数据
        value = df[(df['Server'] == server) & (df['Client_Count'] == client)][metrics].values.flatten()
        # 绘制柱状图
        plt.bar(x + offsets[i], value, width=bar_width, label=label, color=color_map[label])
        # 添加数值标签
        for j in range(len(metrics)):
            plt.text(x[j] + offsets[i], value[j] + max(value)*0.01, f'{value[j]}', ha='center', va='bottom', fontsize=9)
    
    # 设置x轴标签
    plt.xticks(x, [metric.replace('RTT_', '').replace('Mb_', '').replace('_ms)', ')').replace('_', ' ') for metric in metrics], rotation=45, ha='right', fontsize=12)
    plt.title(f'{category_name} Performance Analysis', fontsize=16)
    plt.ylabel('Value', fontsize=14)
    plt.xlabel('性能指标', fontsize=14)
    plt.legend(title='服务器-客户端', fontsize=12, title_fontsize=12)
    
    # 优化布局
    plt.tight_layout()
    
    # 保存图表为PNG文件
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300)
    plt.close()
    
    print(f"图表已保存为: {filename}")

# 生成RTT相关的柱状图
plot_category('RTT', rtt_metrics, 'RTT_Performance_Analysis.png')

# 生成Input相关的柱状图
plot_category('Input', input_metrics, 'Input_Performance_Analysis.png')

# 生成Output相关的柱状图
plot_category('Output', output_metrics, 'Output_Performance_Analysis.png')

print("所有图表已生成并保存。")
