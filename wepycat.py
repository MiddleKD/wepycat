import os
from glob import glob
import argparse
import queue
from tqdm import tqdm
from crawler import (crawl_website, load_driver, kill_driver,
                     download_single, download_file)
from utils import (extract_url_from_html_content, 
                   extract_file_paths_from_html_content, 
                   save_html, open_html_file)
from flask_builder import make_flask_app_py, save_flask_app_file

def parse_argument():
    parser = argparse.ArgumentParser(description="Copy webpage source from webwave")

    parser.add_argument("--url", type=str, help="target url to copy")
    parser.add_argument("--page_name", type=str, help="web page directory name")

    return parser.parse_args()

def recursive_crawl_html_and_innerurl():
    crawl_url_queue = queue.Queue()
    crawl_url_queue.put(root_url)
    crawl_done_urls = set()

    load_driver()
    while not crawl_url_queue.empty():
        target_url = crawl_url_queue.get()
        if target_url in crawl_done_urls:
            continue

        html_content = crawl_website(target_url)
        urls = extract_url_from_html_content(html_content, root_url=root_url)
        
        if target_url == root_url:
            save_html(html_content, os.path.join(page_dir_name, "home.html"))
        else:
            save_html(html_content, os.path.join(page_dir_name, 
                                                target_url.replace(root_url+"/","")+".html"))

        crawl_done_urls.add(target_url)
        for url in urls:
            if url in crawl_done_urls:
                continue
            else:
                crawl_url_queue.put(url)
    kill_driver()
    
    return crawl_done_urls

if __name__ == "__main__":
    args = parse_argument()

    root_url = args.url
    page_dir_name = "./"+args.page_name
    os.makedirs(page_dir_name, exist_ok=False)

    inner_urls = recursive_crawl_html_and_innerurl()
    print(f"\"{root_url}\" has {len(inner_urls)} recursive inner url:\n {inner_urls}")

    download_single(f"{root_url}/manifest.json", os.path.join(page_dir_name, "manifest.json"))
    html_fns = glob(os.path.join(page_dir_name, "*.html"))

    for html_fn in html_fns:
        print("PROCESSING", html_fn)

        html_content = open_html_file(html_fn)
        file_paths = extract_file_paths_from_html_content(html_content)

        print("Image paths:", len(file_paths["images"]))
        print("CSS paths:", len(file_paths["css"]))
        print("JavaScript paths:", len(file_paths["js"]))

        print("IMAGE FILE CRAWL")
        for cur in tqdm(file_paths["images"]):
            if cur.startswith("./"): continue
            cur_file_path = download_file(url=cur, root_http='https://yourbrand-18274.kxcdn.com')
            html_content = html_content.replace(cur, cur_file_path)

        print("CSS FILE CRAWL")
        for cur in tqdm(file_paths["css"]):
            if cur.startswith("./"): continue
            cur_file_path = download_file(url=cur, root_http='https://yourbrand-18274.kxcdn.com')
            html_content = html_content.replace(cur, cur_file_path)

        print("JS FILE CRAWL")
        for cur in tqdm(file_paths["js"]):
            if cur.startswith("./"): continue
            if "service-worker.js" in cur: continue
            if "datePickerService.js" in cur: continue

            cur_file_path = download_file(url=cur, root_http='https://yourbrand-18274.kxcdn.com')
            html_content = html_content.replace(cur, cur_file_path)
        
        html_content = html_content.replace(f"{root_url}/", "./")
        html_content = html_content.replace('data-element-type="button', 'data-element-type="image')

        with open(html_fn, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print("----------")

    print("Make Flask file")
    falsk_app_py = make_flask_app_py(page_dir_name)
    save_flask_app_file(falsk_app_py, os.path.join("flask_app", f"{page_dir_name.replace('./','')}_app.py"))

    print("All process is completed!")