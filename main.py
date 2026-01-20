import matplotlib.pyplot as plt
import matplotlib.patches as patches
import colorsys
import hashlib

# ==========================================
# 1. 课程数据 (经过二次人工核对)
# ==========================================
# 格式: [课程名称, 教师, 星期(1-7), "开始-结束", 教室]
raw_data = [
    # Page 1
    ["微分几何", "王险峰", 3, "7-8", "A411"],
    ["微分几何", "王险峰", 3, "11-12", "A411"],
    ["应用数学前沿选讲", "史永堂", 3, "9-10", "B101"],
    ["风险理论基础", "李波", 2, "7-9", "A602"],
    ["有限群表示论", "常亮", 5, "2-4", "A101"],
    ["代数与编码", "陈鲁生", 2, "3-4", "数学第三教室"],
    ["代数与编码", "陈鲁生", 4, "3-4", "数学第三教室"],
    ["数据结构", "吴忠华", 2, "7-9", "数学机房"],
    ["精算数学", "李津竹", 2, "3-4", "B101"],
    ["精算数学", "李津竹(1-15单)", 5, "3-4", "B101"],
    ["数论", "栗慧曦", 2, "7-8", "A108"],
    ["数论", "栗慧曦", 4, "3-4", "A602"],
    ["金融工程学", "李静", 3, "2-4", "A512"],
    ["抽象函数与巴拿赫代数", "刘锐", 2, "2-4", "B104"],
    ["计算机集合论与逻辑", "李军", 3, "11-12", "A101"],
    ["计算机集合论与逻辑", "李军", 5, "11-12", "A101"],
    ["点集拓扑学", "丁龙云", 2, "11-13", "B205"],
    ["点集拓扑学", "GAO SU", 2, "11-13", "B302"],
    ["数学前沿问题选讲", "马世光(2-16双)", 5, "7-8", "数学第一报告厅"],

    # Page 2
    ["并行数值方法", "张胜", 1, "11-13", "A101"],
    ["现代分析基础", "张震球", 2, "3-4", "A101"],
    ["现代分析基础", "张震球", 5, "9-10", "A101"],
    ["运筹学", "胡威", 1, "7-9", "B104"],
    ["交换代数", "于世卓", 4, "11-12", "数学第二报告厅"],
    ["交换代数", "于世卓", 5, "11-12", "数学第二报告厅"],
    ["数值逼近", "叶培新", 5, "2-4", "A401"],
    ["结合代数", "王立云", 5, "2-4", "A203"],
    ["离散优化", "史永堂", 1, "3-4", "A304"],
    ["离散优化", "史永堂", 3, "7-8", "A304"],
    ["GPU程序设计", "袁拓", 2, "1-2", "A101"],
    ["抽象代数II", "邓少强", 2, "9-10", "A101"],
    ["抽象代数II", "邓少强", 3, "9-10", "A101"],
    ["抽象代数II", "邓少强", 4, "3-4", "A101"],
    ["抽象代数II", "文豪", 2, "9-10", "A411"],
    ["抽象代数II", "文豪", 3, "9-10", "A411"],
    ["抽象代数II", "文豪", 4, "3-4", "A601"],
    ["微分方程数值解", "胡广辉(1-5)/乐航睿(6-16)", 4, "11-13", "A202"],
    ["人工智能算法导论", "张胜", 2, "11-13", "A202"],
    ["科学计算实验", "张胜", 5, "7-9", "A103"],
    ["离散结构及其算法", "郭龙,孙慧,谷珊珊", 1, "7-9", "A202"],
    ["数值代数", "高冰", 1, "1-3", "A411"],
    ["李群与代数群", "李宁", 5, "7-9", "数学第三教室"],
    ["黎曼几何与几何分析选讲", "王文龙", 2, "11-12", "A411"],
    ["黎曼几何与几何分析选讲", "王文龙", 3, "3-4", "A411"],
    ["现代图论(全英文)", "王周宁馨", 2, "7-9", "A202"],
    ["拓扑线性空间", "李磊", 2, "2-4", "数学第五教室"],
    ["Galois 理论", "徐言", 2, "9-10", "A101"],
    ["Galois 理论", "徐言", 3, "9-10", "A101"],
    ["高级语言程序设计2-2", "郭宪", 3, "1-2", "A510"],
    ["变分学", "朱朝锋", 4, "11-13", "省身楼214"],
]

# ==========================================
# 2. 核心逻辑：动态宽度计算
# ==========================================

def get_text_color(course_name, teacher):
    """
    生成高对比度颜色，用于字体。
    """
    key = f"{course_name}_{teacher}"
    hash_object = hashlib.md5(key.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    hue = (hash_int % 100) / 100.0
    saturation = 0.95
    value = 0.40 # 保持深色，便于白底阅读
    return colorsys.hsv_to_rgb(hue, saturation, value)

def parse_data(raw_data):
    parsed = []
    for item in raw_data:
        name, teacher, day, periods_str, room = item
        parts = periods_str.split('-')
        if len(parts) < 2: parts = periods_str.split('/') # 兼容
        start = int(parts[0])
        end = int(parts[-1])
        parsed.append({
            "name": name,
            "teacher": teacher,
            "day": day,
            "start": start,
            "end": end,
            "room": room,
            "duration": end - start + 1
        })
    return parsed

def compute_column_packing(events):
    """
    对一组课程进行列填充，返回需要的总列数，并给每个事件分配列索引。
    """
    events.sort(key=lambda x: (x['start'], -x['duration']))
    columns = [] # 记录每一列的结束时间
    
    for event in events:
        placed = False
        for i, col_end in enumerate(columns):
            if event['start'] > col_end:
                columns[i] = event['end']
                event['col_idx'] = i
                placed = True
                break
        if not placed:
            columns.append(event['end'])
            event['col_idx'] = len(columns) - 1
            
    return len(columns)

# ==========================================
# 3. 绘图逻辑
# ==========================================

def draw_dynamic_schedule(data):
    events = parse_data(data)
    
    # 1. 计算每一天需要的列数（宽度）
    day_widths = {}
    day_events_map = {}
    
    for day in range(1, 8):
        d_events = [e for e in events if e['day'] == day]
        day_events_map[day] = d_events
        if not d_events:
            day_widths[day] = 1 # 最小宽度
            continue
        
        # 计算该天最大冲突数
        max_cols = compute_column_packing(d_events)
        day_widths[day] = max(1, max_cols) # 至少为1

    # 2. 计算X轴坐标映射
    # x_offset[day] 表示该天开始的 x 坐标
    current_x = 0
    day_x_start = {}
    for day in range(1, 8):
        day_x_start[day] = current_x
        current_x += day_widths[day]
    
    total_width = current_x
    
    # 3. 设置画布
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'sans-serif']
    
    # 动态计算图片宽度，保证每个“列单元”有足够的物理像素宽度
    unit_width_inch = 2.5 # 每个最小列宽 2.5 英寸
    fig_width = total_width * unit_width_inch
    fig_height = 20 # 高度固定
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)
    
    # 设置坐标轴
    ax.set_ylim(14.5, 0.5)
    ax.set_xlim(0, total_width)
    
    # 绘制X轴标签（居中显示）
    days_cn = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    tick_locs = []
    tick_labels = []
    
    for day in range(1, 8):
        center = day_x_start[day] + day_widths[day] / 2
        tick_locs.append(center)
        tick_labels.append(days_cn[day-1])
        
        # 绘制天与天之间的分隔线
        if day < 7:
            ax.axvline(day_x_start[day] + day_widths[day], color='black', linewidth=2, linestyle='-')

    ax.set_xticks(tick_locs)
    ax.set_xticklabels(tick_labels, fontsize=24, fontweight='bold')
    ax.xaxis.tick_top()
    
    # Y轴
    ax.set_yticks(range(1, 15))
    ax.set_yticklabels([f"第{i}节" for i in range(1, 15)], fontsize=16)
    
    # 水平网格线
    for y in range(1, 15):
        ax.axhline(y + 0.5, color='#dddddd', linestyle='--', linewidth=1)

    # 4. 绘制课程
    for day in range(1, 8):
        d_events = day_events_map[day]
        start_x = day_x_start[day]
        
        for event in d_events:
            # 这里的 col_idx 是在当前天内的索引
            # 每一个事件占用的宽度是 1 个单位
            x = start_x + event['col_idx']
            y = event['start'] - 0.5
            w = 1.0 # 占满一个单位宽
            h = event['duration']
            
            # 颜色
            color = get_text_color(event['name'], event['teacher'])
            
            # 背景框 (白色，带灰色边框)
            # 留一点间隙 margin
            margin = 0.05
            rect = patches.Rectangle(
                (x + margin, y + margin), 
                w - 2*margin, 
                h - 2*margin, 
                linewidth=1.5, 
                edgecolor='#cccccc', 
                facecolor='white',
                zorder=2
            )
            ax.add_patch(rect)
            
            # 左侧颜色条
            bar_width = 0.1
            bar = patches.Rectangle(
                (x + margin, y + margin),
                bar_width,
                h - 2*margin,
                facecolor=color,
                edgecolor=None,
                zorder=3
            )
            ax.add_patch(bar)
            
            # 文本
            text_str = f"{event['name']}\n{event['teacher']}\n@{event['room']}"
            ax.text(
                x + 0.5, # 居中
                y + h/2, 
                text_str, 
                ha='center', 
                va='center', 
                fontsize=11, 
                color=color,
                fontweight='bold',
                wrap=True,
                zorder=4
            )

    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    
    filename = "math_schedule_dynamic.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    draw_dynamic_schedule(raw_data)