import subprocess
import re

def check_device_connected():
    command = ["adb", "devices"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    devices = result.stdout.strip().split('\n')[1:]
    if not devices or devices[0].strip() == '':
        print("未检测到设备，请插入设备后重新运行。")
        return False
    return True

def get_device_resolution():
    command = ["adb", "shell", "wm", "size"]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    match = re.search(r'(\d+)x(\d+)', result.stdout)
    if match:
        width, height = map(int, match.groups())
        print(f"设备分辨率：{width}x{height}")
        return width, height
    else:
        print("无法获取设备分辨率。")
        return None

def adb_tap(x, y):
    command = ["adb", "shell", "input", "tap", str(x), str(y)]
    subprocess.run(command, check=True)
    print(f"已点击坐标 ({x}, {y})")

def adb_input(text):
    command = ["adb", "shell", "input", "text", f'"{text}"']
    subprocess.run(command, check=True)
    print(f"已输入文本: {text}")

def adb_swipe(x1, y1, x2, y2):
    command = ["adb", "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2)]
    subprocess.run(command, check=True)
    print(f"已从坐标 ({x1}, {y1}) 滑动到坐标 ({x2}, {y2})")

def main():
    if not check_device_connected():
        return

    resolution = get_device_resolution()
    if resolution:
        max_x, max_y = resolution
    else:
        max_x, max_y = 2032, 3048  # 默认分辨率

    while True:
        print("请选择操作：")
        print("1. 点击")
        print("2. 输入")
        print("3. 滑动")
        print("4. 退出")
        choice = input("请输入选项（1/2/3/4）：")

        if choice == "1":
            x = input(f"请输入x坐标（0-{max_x}）：")
            y = input(f"请输入y坐标（0-{max_y}）：")
            try:
                x = int(x)
                y = int(y)
                if 0 <= x <= max_x and 0 <= y <= max_y:
                    adb_tap(x, y)
                else:
                    print("坐标超出范围，请重新输入！")
            except ValueError:
                print("输入无效，请输入整数坐标！")
        elif choice == "2":
            text = input("请输入要输入的文本：")
            adb_input(text)
        elif choice == "3":
            x1 = input(f"请输入起始x坐标（0-{max_x}）：")
            y1 = input(f"请输入起始y坐标（0-{max_y}）：")
            x2 = input(f"请输入结束x坐标（0-{max_x}）：")
            y2 = input(f"请输入结束y坐标（0-{max_y}）：")
            try:
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                if (0 <= x1 <= max_x and 0 <= y1 <= max_y and
                    0 <= x2 <= max_x and 0 <= y2 <= max_y):
                    adb_swipe(x1, y1, x2, y2)
                else:
                    print("坐标超出范围，请重新输入！")
            except ValueError:
                print("输入无效，请输入整数坐标！")
        elif choice == "4":
            print("退出程序。")
            break
        else:
            print("无效选项，请重新输入！")

if __name__ == "__main__":
    main()