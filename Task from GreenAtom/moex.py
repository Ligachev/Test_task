import sys
import datetime
import pymorphy2

import requests
import xml.etree.ElementTree as ET
from lxml.etree import Element
from requests import Response
import xlwt
from xlwt import Workbook, Worksheet, XFStyle

import smtplib
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


"""
moex.py скрипт для создания и отправки отчета по индикативным валютным парам.
Разбит на части:
Request на API moex.com;
Обработка response;
Создание файла exel и запись обработанной информации;
Отправка готового отчета по email.
"""


def get_res(date_last: str, date_now: str, currency: str) -> Response:
    """
    Request на API moex.com, обработка исключений.
    """
    try:
        res = requests.get(
            url='https://moex.com/export/derivatives/currency-rate.aspx',
            params=f'language=ru&currency={currency}&moment_start={date_last}&moment_end={date_now}'
        )
        if res.status_code < 400:
            return res
        else:
            print("Connection Error!")
            sys.exit()
    except requests.ConnectionError:
        print("Connection Error!")
        sys.exit()


def get_elem_tree(res: Response) -> Element:
    """
    Обработка pesponse, постороение ElementTree.
    """
    with open('moex.xml', 'w') as f:
        f.write(res.text)
    return ET.ElementTree(file='moex.xml')


_cur_inf = {
        "A": "Дата",
        "B": "Курс",
        "C": "Изменение",
        "D": "Дата",
        "E": "Курс",
        "F": "Изменение",
        "G": "Евро/доллар"
    }


def iter_trees(usd_xml_trees: Element, eur_xml_trees: Element) -> int:
    """
    Итерация по ElementTree.
    """
    book = xlwt.Workbook()
    sheet = create_sheet(book)
    row = 0
    for usd, eur in zip(usd_xml_trees.iter(), eur_xml_trees.iter()):
        data_usd = usd.attrib
        data_eur = eur.attrib
        if usd.tag == 'rtsdata':
            write_to_book(sheet, row, _cur_inf)
        if usd.tag == 'rate':
            if row > 0:
                _cur_inf['C'] = _cur_inf['B'] - get_float(data_usd)
                _cur_inf['F'] = _cur_inf['E'] - get_float(data_eur)
                write_to_book(sheet, row, _cur_inf)
                row += 1

            _cur_inf['A'] = data_usd['moment'][:-3]
            _cur_inf['B'] = get_float(data_usd)
            _cur_inf['D'] = data_eur['moment'][:-3]
            _cur_inf['E'] = get_float(data_eur)
            _cur_inf['G'] = _cur_inf['E']/_cur_inf['B']

            if row == 0:
                row += 1
                continue

    rows = (len(sheet._Worksheet__rows))
    book.save("MOEX_currency.xls")
    return rows


def get_float(data: dict) -> float:
    return float(data['value'])


def create_sheet(book: Workbook) -> Worksheet:
    sheet = book.add_sheet("currency")
    return sheet


def write_to_book(sheet: Worksheet, row: int, cur_inf: dict):
    """
    Запись обработанной информации в Worksheet.
    """
    row = sheet.row(row)
    style = XFStyle()
    for index, value in enumerate(cur_inf.values()):
        if (row != 0) and (index != 0 or 3):
            style.num_format_str = '"₽"#,##0.0000;"₽"#,##0.0000'
        sheet.col(index).width = 4000
        row.write(index, value, style=style)


def get_correct_declension(rows: int) -> str:
    """
    Выбор правильной формы для склонения "строки".
    """
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse('строка')[0]
    v1, v2, v3 = word.inflect({'sing', 'nomn'}), word.inflect({'gent'}), word.inflect({'plur', 'gent'})

    if 14 >= rows >= 11:
        return v3.word
    elif str(rows)[-1] == '1':
        return v1.word
    elif '4' >= str(rows)[-1] >= '2':
        return v2.word
    else:
        return v3.word


def send_message(rows_int: int, rows_str: str):
    """
    Послать отчет с вложением на email.
    """
    msg = MIMEMultipart()

    password = "1234qwerASDF"
    msg['From'] = "sendmassages7@gmail.com"
    msg['To'] = "a.ligachev@gmail.com"

    msg['Subject'] = 'Итоговый файл отчета'
    message = f"Отчет по индикативным курсам валют.\nВалютные пары USD/RUB и EUR/RUB.\n{rows_int} {rows_str}."
    msg.attach(MIMEText(message))

    fp = open(r"./MOEX_currency.xls", 'rb')
    record = MIMEBase('application', 'octet-stream')
    record.set_payload(fp.read())
    encode_base64(record)
    record.add_header('Content-Disposition', 'attachment',
                      filename="MOEX_currency.xls")
    msg.attach(record)

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())


def main():
    """
    Основная функция.
    Определен период и валютные пары.
    """
    date_now = datetime.date.today()
    date_last = (date_now - datetime.timedelta(31))
    currency = ['USD_RUB', 'EUR_RUB']
    response = [get_res(date_last.isoformat(), date_now.isoformat(), cur) for cur in currency]
    usd_xml_trees, eur_xml_trees = [get_elem_tree(res) for res in response]
    rows_int = iter_trees(usd_xml_trees, eur_xml_trees)
    rows_str = get_correct_declension(rows_int)
    send_message(rows_int, rows_str)


if __name__ == '__main__':
    main()

