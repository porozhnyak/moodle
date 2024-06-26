from utils import asyncres
import os
from bs4 import BeautifulSoup
import imgkit
import asyncio
import aiohttp
# from credit.config import user_login, user_password
from utils import asyncres
import logging
import jinja2
from utils.parse_utils.getpage import get_page

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('response')

async def all_grades_screen(user_login, user_password, output_file='grades_table.png'):

    url = "https://distant.donnuet.ru/grade/report/overview/index.php"

    temp_file = 'temp_page.html'

    log = await asyncres.login(user_login, user_password)
    html = await get_page(log, url)
    
    with open('temp_page.html', 'w', encoding='utf-8') as f:
        f.write(html)

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'id': 'overview-grade'})  # Замените на соответствующий селектор

    resolution = (720, 1280)
    
    if table:
        table_html = str(table)
        
        # Загрузка HTML-шаблона с использованием jinja2
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template("BOT/utils/template.html")
        
        # Подстановка HTML-кода таблицы в шаблон и рендеринг
        rendered_html = template.render(table_html=table_html)

        options = {
            'format': 'jpg',
            'encoding': 'UTF-8',
            'width': resolution[0],  # Устанавливаем ширину изображения
            'height': resolution[1]
        }

        imgkit.from_string(rendered_html, output_file, options=options)
        result = f'Таблица с оценками успешно сохранена в {output_file}'
    else:
        result = 'Не удалось найти таблицу с оценками на странице.'


    if os.path.exists(temp_file):
        os.remove(temp_file)
    return result

# asyncio.run(all_grades_screen(user_login, user_password))