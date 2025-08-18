import os

# 要匹配的双扩展名
TARGET_SUFFIX = ".baiduyun.uploading.cfg"

# 存储删除失败的文件
failed_deletions = []

def delete_target_files(base_path):
    count = 0
    for dirpath, _, filenames in os.walk(base_path):
        for filename in filenames:
            if filename.endswith(TARGET_SUFFIX):
                full_path = os.path.join(dirpath, filename)
                try:
                    os.remove(full_path)
                    print(f"✅ 已删除: {full_path}")
                    count += 1
                except Exception as e:
                    print(f"❌ 删除失败: {full_path}，错误: {e}")
                    failed_deletions.append((full_path, str(e)))
    print(f"\n🔎 共尝试删除 {count + len(failed_deletions)} 个文件，成功 {count} 个。")
    if failed_deletions:
        print("❗以下文件删除失败：")
        for path, error in failed_deletions:
            print(f"{path} -> 错误: {error}")

if __name__ == "__main__":
    base_dir = os.getcwd()
    delete_target_files(base_dir)
