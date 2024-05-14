import re, io, os
from PIL import Image

def open_html_file(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content

def extract_file_paths_from_html_content(html_content):
    # 이미지 파일 경로 추출
    image_pattern = r'(?:["\']|:&quot;)([^{"\']+?\.)(png|jpg|jpeg|gif|webp)(?:["\']|&quot;)'
    image_paths = re.findall(image_pattern, html_content)

    # CSS 파일 경로 추출
    css_pattern = r'(?:["\']|:&quot;)([^{"\']+?\.css)(?:["\']|&quot;)'
    css_paths = re.findall(css_pattern, html_content)

    # JavaScript 파일 경로 추출
    js_pattern = r'(?:["\']|:&quot;)([^{"\']+?\.js)(?:["\']|&quot;)'
    js_paths = re.findall(js_pattern, html_content)

    # 파일 경로 리스트 반환
    return {
        "images": [path[0] + path[1] for path in image_paths],
        "css": css_paths,
        "js": js_paths
    }

def extract_url_from_html_content(html_content, root_url):
    url_pattern = fr'href=(?:["\']|:&quot;)((?!http)[/#][^"\']+?(?<!\.json))(?:["\']|&quot;)'
    urls = re.findall(url_pattern, html_content)

    return {root_url + cur for cur in urls}

def save_html(html_content, save_path):
    try:
        with open(save_path, mode="w") as f:
            f.write(html_content)
    except:
        print(f"Error occured saving {save_path}")
    return save_path

def convert_to_webp(input_data, output_path="./webp_data.webp", input_type="path"):
    
    if not output_path.endswith(".webp"):
        output_path = os.path.splitext(output_path)[0] + ".webp"

    if input_type == 'path':
        # 경로일 경우
        img = Image.open(input_data)
        img.save(output_path, 'WEBP')
        return output_path

    elif input_type == 'binary':
        # 바이너리일 경우
        img = Image.open(io.BytesIO(input_data))
        webp_bytes = io.BytesIO()
        img.save(webp_bytes, format='WEBP')
        webp_bytes.seek(0)
        with open(output_path, 'wb') as f:
            f.write(webp_bytes.getvalue())
        return output_path

    elif input_type == 'pil':
        # PIL 객체일 경우
        webp_bytes = io.BytesIO()
        input_data.save(webp_bytes, format='WEBP')
        webp_bytes.seek(0)
        with open(output_path, 'wb') as f:
            f.write(webp_bytes.getvalue())
        return output_path

    else:
        raise ValueError('Invalid input type. Must be "path", "binary", or "pil".')