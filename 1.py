import tkinter as tk
from tkinter import ttk, messagebox
import ipaddress
from tkinter import PhotoImage
from PIL import ImageTk, Image


# 验证输入的IP地址是否有效
def validate_ip(ip_input):
    try:
        ipaddress.ip_address(ip_input)
        return True
    except ValueError:
        # 弹出错误提示框，提示无效的IP地址
        messagebox.showerror("Invalid IPv6", "请输入有效的128bit IPv6地址，范围从0000:0000:0000:0000:0000:0000:0000:0000始")
        return False


# 更新计算结果
def update_results():
    ip_input = entry_ip_address.get()
    if not validate_ip(ip_input):
        return
    subnet_value = int(subnet_mask_scale.get())
    subnet_mask_str = mask_options[subnet_value - 1]
    combo_subnet_mask.set(subnet_mask_str)
    try:
        network = ipaddress.ip_network(f"{ip_input}/{subnet_value}", strict=False)

        global results
        results = {
            "最大地址数": network.num_addresses,
            "可用第一个地址:\n(即网络地址)":str(network.network_address ).upper() if network.num_addresses >= 2 else '该地址空间仅属于单个主机，\n所以唯一的可用地址即为它本身',
            "可用最后一个地址:\n(即广播地址)":str(network.broadcast_address ).upper() if network.num_addresses >= 2 else '无',
            "掩码16进制表示": str(network.netmask).upper(),
            "掩码10进制表示": '/'+str(subnet_value),
        }
        update_results_display(results)
    except ValueError as e:
        # 弹出错误提示框，提示输入有误
        messagebox.showerror("Error", "请检查您的输入并重试。")


# 显示计算结果
def update_results_display(results):
    # 清空现有的结果显示
    for widget in results_frame.winfo_children():
        widget.destroy()
    # 逐行显示新的结果
    for i, (label, value) in enumerate(results.items()):
        tk.Label(results_frame, text=f"{label}:").grid(row=i, column=0, sticky='e')
        tk.Label(results_frame, text=f"{value}").grid(row=i, column=1, sticky='w')


# 当滑动条值变化时更新下拉框
def update_combobox_from_scale(value):
    selected_index = int(float(value)) - 1
#拖动滑块后，以下代码负责实时显示index的值
    combo_subnet_mask.set(mask_options[selected_index])


# 复制结果到剪贴板
def copy_to_clipboard():
    keys_to_copy = ["最大地址数", "可用第一个地址:\n(即网络地址)", "可用第一个地址", "可用最后一个地址:\n(即广播地址)","掩码16进制表示","掩码10进制表示"]
    result_text = "\n".join(f"{key}: {results[key]}" for key in keys_to_copy if key in results)
    root.clipboard_clear()
    root.clipboard_append(result_text)
    # 弹出提示框，提示复制成功
    messagebox.showinfo("复制成功", "选定的计算结果已复制到剪贴板。")

def update_scale_value(event):
    selected_mask = combo_subnet_mask.get()  # 获取下拉菜单中选择的子网掩码选项
    # 从选项中解析出子网掩码的长度
    subnet_mask_length = int(selected_mask.split('/')[1])
    # 设置滑动条的值为对应的子网掩码长度
    subnet_mask_scale.set(subnet_mask_length)

# 主窗体设置
root = tk.Tk()
root.title("IPv6 掩码计算器")
root.geometry("380x400")

# 在窗口中创建Label来显示图片
#img_label = tk.Label(root, image=img)
#img_label.pack(side=tk.LEFT, padx=10, pady=10)  # 放置在右侧，并设置边距

# 输入IP地址
tk.Label(root, text="请输入IP地址:").pack(anchor='w', padx=10, pady=2)
entry_ip_address = tk.Entry(root)
entry_ip_address.insert(0, "2001:0000:0000:0000:0000:0000:0000:0000")  # 设置默认IP地址示例
entry_ip_address.pack(fill='x', padx=20, pady=5)

# 子网掩码滑动条和下拉菜单
tk.Label(root, text="请选择掩码，可拖动滑块选择：").pack(anchor='w', padx=10, pady=2)
mask_options = [f"{ipaddress.IPv6Address((0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF << (128 - i)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)}/{i}".upper() for i in range(1, 129)]
subnet_mask_scale = ttk.Scale(root, from_=1, to_=128, orient='horizontal', command=update_combobox_from_scale)
subnet_mask_scale.pack(fill='x', padx=20, pady=2)
subnet_mask_scale.set(24)  # 设置默认位置

combo_subnet_mask = ttk.Combobox(root, values=mask_options, state="readonly")
combo_subnet_mask.pack(fill='x', padx=20, pady=2)
combo_subnet_mask.bind("<<ComboboxSelected>>", update_scale_value)# 绑定下拉菜单事件，使滑动条的值随之改变


# 结果显示框架
results_frame = tk.Frame(root)
results_frame.pack(fill='x', padx=10, pady=10)

# 按钮框架
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# 复制结果按钮
clipboard_button = tk.Button(button_frame, text="复制结果", command=copy_to_clipboard)
clipboard_button.pack(side='left', padx=5)

# 结果更新按钮
calculate_button = tk.Button(button_frame, text="计算", command=update_results)
calculate_button.pack(side='left', padx=5)

root.mainloop()