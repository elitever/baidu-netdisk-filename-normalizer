import os
import re
import shutil
import emoji

# 修复：新版 emoji 无 get_emoji_regexp()，自定义一个通用 emoji 匹配器
EMOJI_PATTERN = re.compile("[" 
    u"\U0001F600-\U0001F64F"  # 表情
    u"\U0001F300-\U0001F5FF"  # 符号 & 图形
    u"\U0001F680-\U0001F6FF"  # 交通 & 地图
    u"\U0001F1E0-\U0001F1FF"  # 国旗
    "]+", flags=re.UNICODE)

SPECIAL_CHARS_PATTERN = re.compile(r"[^\w\d\.\-()\u4e00-\u9fa5]")  # 允许中英文、数字、. - () 下划线

# 记录失败项
failed_log = []

def safe_name(name):
    name = EMOJI_PATTERN.sub("_", name)
    name = SPECIAL_CHARS_PATTERN.sub("_", name)
    name = re.sub(r"_+", "_", name)  # 合并多个下划线
    return name.strip("_")  # 去头尾

def batch_rename(base_path):
    for dirpath, dirnames, filenames in os.walk(base_path, topdown=False):
        for filename in filenames:
            old = os.path.join(dirpath, filename)
            new_name = safe_name(filename)
            new = os.path.join(dirpath, new_name)
            try:
                if old != new and os.path.exists(old):
                    os.rename(old, new)
                    print(f"重命名：{old} -> {new}")
            except Exception as e:
                failed_log.append((old, str(e)))

        for dirname in dirnames:
            old = os.path.join(dirpath, dirname)
            new_name = safe_name(dirname)
            new = os.path.join(dirpath, new_name)
            try:
                if old != new and os.path.exists(old):
                    os.rename(old, new)
                    print(f"重命名：{old} -> {new}")
            except Exception as e:
                failed_log.append((old, str(e)))

if __name__ == "__main__":
    base = os.getcwd()
    batch_rename(base)

    # 输出失败项日志
    if failed_log:
        print("\n以下文件/文件夹重命名失败：")
        for path, err in failed_log:
            print(f"[失败] {path} 错误: {err}")
    else:
        print("\n✅ 所有项目成功重命名！")
