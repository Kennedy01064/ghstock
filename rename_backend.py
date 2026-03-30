import os

def rename_package(directory, old_name, new_name):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content.replace(old_name, new_name)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {path}")

if __name__ == "__main__":
    target_dir = r"c:\Users\HP\Desktop\Stock\backend"
    rename_package(target_dir, "api_v2", "backend")
