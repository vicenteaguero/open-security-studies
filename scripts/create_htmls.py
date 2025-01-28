# scripts/create_htmls.py

from bs4.formatter import HTMLFormatter
from bs4 import BeautifulSoup
import os
import shutil

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT_PATH, 'content')
LESSONS_DIR = os.path.join(CONTENT_DIR, 'lessons')
SAVE_LESSONS_DIR = os.path.join(ROOT_PATH, 'lessons')
DEFAULT_HTML_PATH = os.path.join(ROOT_PATH, '.default.html')

if __name__ == '__main__':

    base_htmls = [f for f in os.listdir(CONTENT_DIR) if f.endswith('.html')]
    lesson_htmls = [f for f in os.listdir(LESSONS_DIR) if f.endswith('.html')]

    for filename in base_htmls:
        subdir = os.path.splitext(filename)[0]
        if subdir == 'index':
            if os.path.isfile(os.path.join(ROOT_PATH, 'index.html')):
                os.remove(os.path.join(ROOT_PATH, 'index.html'))
        else:
            out_dir = os.path.join(ROOT_PATH, subdir)
            if os.path.isdir(out_dir):
                shutil.rmtree(out_dir)

    print('Base HTMLs:', base_htmls)
    print('Lesson HTMLs:', lesson_htmls)

    base_html_paths = [os.path.join(CONTENT_DIR, x) for x in base_htmls]
    lesson_html_paths = [os.path.join(LESSONS_DIR, x) for x in lesson_htmls]

    source_paths = base_html_paths+lesson_html_paths

    save_paths = list()

    for path in base_html_paths:
        base_name = os.path.splitext(os.path.basename(path))[0]
        if base_name == 'index':
            save_paths.append(os.path.join(ROOT_PATH, 'index.html'))
        else:
            save_paths.append(os.path.join(ROOT_PATH, base_name, 'index.html'))

    for path in lesson_html_paths:
        base_name = os.path.splitext(os.path.basename(path))[0]
        save_paths.append(os.path.join(SAVE_LESSONS_DIR, base_name, 'index.html'))

    with open(DEFAULT_HTML_PATH, encoding='utf-8') as file:
        default_layout_str = file.read()

    formatter = HTMLFormatter(indent=4)

    for src_path, out_path in zip(source_paths, save_paths):

        layout_soup = BeautifulSoup(default_layout_str, 'html.parser')

        with open(src_path, encoding='utf-8') as f:
            content_soup = BeautifulSoup(f, 'html.parser')

        container = layout_soup.find('div', class_='content')
        if container:
            container.clear()
            container.append(content_soup)

        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, 'w', encoding='utf-8') as out_file:
            out_file.write(layout_soup.prettify(formatter=formatter))
        print(f'Created: {os.path.relpath(out_path, ROOT_PATH)}')
