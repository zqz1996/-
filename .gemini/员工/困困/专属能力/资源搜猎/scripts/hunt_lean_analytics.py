import sys
import os
import json
import time

# Add ebook_toolbox to path
TOOLBOX_PATH = r"d:\zqzproject\.gemini\员工\困困\专属能力\资源搜猎\scripts\ebook_toolbox"
sys.path.append(TOOLBOX_PATH)

try:
    from Zlibrary import Zlibrary # type: ignore
    print("汪！Z-Library 模块加载成功！")
except ImportError:
    print("呜... 找不到 Zlibrary 模块，请检查路径。")
    sys.exit(1)

# Result Directory
LIBRARY_DIR = r"d:\zqzproject\.gemini\图书馆\精益数据分析"
if not os.path.exists(LIBRARY_DIR):
    os.makedirs(LIBRARY_DIR)

def hunt_book(book_name):
    print(f"汪！正在嗅探：{book_name}...")
    
    # 1. Login
    # Note: Zlibrary.py handles login via arguments or updates internal state. 
    # Let's try to load config manually or pass to init.
    CONFIG_FILE = os.path.join(TOOLBOX_PATH, "account", "web_accounts.json")
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            creds = config.get("zlibrary", {})
            email = creds.get("email")
            password = creds.get("password")
            remix_id = creds.get("remix_userid")
            remix_key = creds.get("remix_userkey")
            
            if remix_id and remix_key and remix_id != "Get_From_Browser_Cookie":
                 Z = Zlibrary(remix_userid=remix_id, remix_userkey=remix_key)
                 print("汪！使用 Remix Token 登录...")
            elif email and password:
                 Z = Zlibrary(email=email, password=password)
                 print("汪！使用账号密码登录...")
            else:
                 print("呜... 没有找到有效的账号配置。请检查 web_accounts.json")
                 return
    except Exception as e:
        print(f"配置读取失败: {e}")
        return

    # 2. Search
    query = "精益数据分析 阿利斯泰尔"
    try:
        results = Z.search(message=query, languages="chinese")
        if results and results.get("books"):
            print(f"汪！闻到了 {len(results['books'])} 本书的味道！")
            
            # Iterate to find EPUB
            best_book = None
            for book in results['books']:
                if book.get('extension', '').lower() == 'epub':
                    best_book = book
                    break
            
            # Fallback to first if no epub found
            if not best_book:
                best_book = results['books'][0]
                print("呜... 没找到 EPUB 版本，只能叼回来第一本了。")

            if best_book:  # Ensure best_book is not None before accessing
                title = best_book.get("title", "Unknown")
                ext = best_book.get("extension", "")
                author = best_book.get("author", "Unknown") # Store separately to avoid key error if dict handling changes
                print(f"目标锁定：{title} ({ext}) - 作者: {author}")
                
                # 3. Download
                print("正在试图叼回来... (这可能需要几分钟...)")
                filename, content = Z.downloadBook(best_book)
            
            if content:
                # Ensure filename ends with extension
                if not filename.endswith(f".{ext}"):
                    filename += f".{ext}"
                    
                save_path = os.path.join(LIBRARY_DIR, filename)
                with open(save_path, "wb") as f:
                    f.write(content)
                print(f"汪汪！成功！书在：{save_path}")
                
                # 4. Digest (Convert to MD)
                # Auto-call epub_to_md.py if it's an epub
                if "epub" in ext.lower():
                    print("正在执行消化程序 (Converting to MD)...")
                    import subprocess
                    converter_script = os.path.join(os.path.dirname(TOOLBOX_PATH), "epub_to_md.py")
                    proc = subprocess.run(["py", converter_script, save_path], shell=True)
                    
                    # Cleanup source if conversion apparently worked
                    # (Simple check: if .md file exists)
                    base_name = os.path.splitext(filename)[0]
                    md_path = os.path.join(LIBRARY_DIR, base_name + ".md")
                    
                    if os.path.exists(md_path):
                        print(f"汪！转换成功，正在清理残渣 (Deleting Source)...")
                        try:
                            os.remove(save_path)
                            print("清理完毕！")
                        except Exception as e:
                            print(f"呜... 垃圾桶盖住了 (Delete Failed): {e}")
                    else:
                        print("呜... 没看到 MD 文件，保留源文件以防万一。")
                    
            else:
                print("呜... 叼不回来 (下载失败)")
        else:
            print("呜... 什么都没闻到 (可能作者名字太难搜了？)。")
            
    except Exception as e:
        print(f"搜猎过程中摔倒了: {e}")

if __name__ == "__main__":
    hunt_book("精益数据分析")
