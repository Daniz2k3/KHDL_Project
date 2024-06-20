# -*- coding: utf-8 -*-
"""crawl_data_An.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12pJCWPdHv739BKXyH6eR9k4WWBJDUX5X
"""

import re
import time
from time import sleep

from bs4 import BeautifulSoup

# !pip install beautifulsoup4
# !pip install selenium
# #dùng để truy cập web bằng webdriver
# !apt-get update
# !apt install chromium-chromedriver
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


def get_html_content(url):
    # Khởi tạo ChromeDriver với các tùy chọn
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Chạy trình duyệt ẩn danh
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # Tắt hỗ trợ GPU
    # Thêm User-Agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    )

    # Cấu hình đường dẫn ChromeDriver
    chrome_options.add_argument(
        "webdriver.chrome.driver=/usr/lib/chromium-browser/chromedriver"
    )

    # Khởi tạo ChromeDriver với các tùy chọn
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    time.sleep(1)  # Thời gian chờ để trang web tải xong

    html_content = driver.page_source
    driver.quit()
    return html_content


url = "https://batdongsan.vn/ban-nha/"
html_content = get_html_content(url)
print(html_content)


def extract_links_from_divs(soup):
    try:
        target_divs1 = soup.find(
            "div", class_="uk-grid uk-grid-small uk-grid-width-1-1"
        )
        if not target_divs1:
            return []
        target_divs = target_divs1.find_all("div", class_="name")
        all_links = [
            link.get("href")
            for div in target_divs
            for link in div.find_all("a")
            if link.get("href")
        ]
        return all_links
    except Exception as e:
        print(f"Error parsing website: {e}")
        return []


def extract_name(soup):
    # Tìm tất cả các phần tử có class cụ thể
    elements = soup.find_all("div", class_="name")

    for element in elements:

        if element.get_text(strip=True):

            next_sibling = element.find_next("a")
            if next_sibling:
                return next_sibling.get_text(strip=True)

    return None


def extract_local(soup):
    # Tìm tất cả các phần tử có class cụ thể
    elements = soup.find_all(
        "div", class_="project-global-profile-block-001 author-custom"
    )

    for element in elements:

        if element.get_text(strip=True):

            next_sibling = element.find_next("span")
            if next_sibling:
                return next_sibling.get_text(strip=True)

    return None


def extract_price(soup):
    # Tìm tất cả các phần tử có class cụ thể
    elements = soup.find_all("h1", class_="uk-panel-title")

    for element in elements:

        if element.get_text(strip=True):

            next_sibling = element.find_next("strong", class_="price")
            if next_sibling:
                return next_sibling.get_text(strip=True)

    return None


def convert_to_ty(gia):
    if "tỷ" in gia:
        # Xóa chữ 'tỷ' và chuyển đổi sang số float
        return float(gia.replace("tỷ", "").strip())
    elif "triệu" in gia:
        # Xóa chữ 'triệu', chuyển đổi sang số float và chia cho 1000 để chuyển sang đơn vị 'tỷ'
        return float(gia.replace("triệu", "").strip()) / 1000
    else:
        # Trường hợp không có đơn vị 'tỷ' hoặc 'triệu', có thể xử lý tùy ý, ví dụ: trả về None hoặc giá trị mặc định
        return None


from bs4 import BeautifulSoup


# Hàm trích xuất thông tin diện tích
def extract_dientich123(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Diện tích" in strong_tag.text:
            return li.get_text(separator=" ").replace("Diện tích:", "").strip()
    return None


# Hàm trích xuất thông tin địa chỉ
def extract_diachi123(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Địa chỉ" in strong_tag.text:
            return li.get_text(separator=" ").replace("Địa chỉ:", "").strip()
    return None


# Hàm trích xuất thông tin giá
def extract_gia(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Giá" in strong_tag.text:
            return li.get_text(separator=" ").replace("Giá:", "").strip()
    return None


# Hàm trích xuất thông tin số phòng ngủ
def extract_sophongngu123(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Phòng ngủ" in strong_tag.text:
            return li.get_text(separator=" ").replace("Phòng ngủ:", "").strip()
    return None


# Hàm trích xuất thông tin số phòng WC
def extract_sophongwc(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Phòng WC" in strong_tag.text:
            return li.get_text(separator=" ").replace("Phòng WC:", "").strip()
    return None


def extract_matin(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Mã tin" in strong_tag.text:
            return li.get_text(separator=" ").replace("Mã tin:", "").strip()
    return None


from datetime import datetime

from bs4 import BeautifulSoup


# Hàm trích xuất thông tin số tháng từ thuộc tính datetime trong thẻ <time>
def extract_ngaydang123(soup):
    list_items = soup.select(".uk-list li")

    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Ngày đăng" in strong_tag.text:
            time_tag = li.select_one("time")
            if time_tag and time_tag.has_attr("datetime"):
                # Lấy giá trị datetime
                datetime_value = time_tag["datetime"]
                post_date = datetime.strptime(datetime_value, "%Y-%m-%d %H:%M:%S")
                # Trả về chuỗi định dạng ngày/tháng/năm
                formatted_date = f"{post_date.day}/{post_date.month}/{post_date.year}"
                return formatted_date
    return None


from bs4 import BeautifulSoup

# Tạo đối tượng BeautifulSoup


def extract_email(soup):
    mail_div = soup.find("div", class_="more email")
    if mail_div:
        # Tìm thẻ <a> bên trong thẻ <div> đó
        mail_link = mail_div.find("a")
        if mail_link and mail_link.has_attr("href"):
            # Lấy giá trị của thuộc tính href
            email = mail_link["href"]
            # Loại bỏ 'mailto:' từ giá trị href để chỉ lấy địa chỉ email
            email = email.replace("mailto:", "")
            return email
        else:
            return None
    else:
        return None


def extract_sdt(soup):
    mail_div = soup.find("div", class_="more phone")
    if mail_div:
        # Tìm thẻ <a> bên trong thẻ <div> đó
        mail_link = mail_div.find("a")
        if mail_link and mail_link.has_attr("href"):
            # Lấy giá trị của thuộc tính href
            email = mail_link["href"]
            # Loại bỏ 'mailto:' từ giá trị href để chỉ lấy sdt
            email = email.replace("tel:", "")
            return email
        else:
            return None
    else:
        return None


from bs4 import BeautifulSoup


def extract_thanhpho(soup):
    # Tìm thẻ <ul> có class là 'uk-breadcrumb'
    mail_div = soup.find("ul", class_="uk-breadcrumb")
    if mail_div:
        # Tìm tất cả thẻ <li> bên trong thẻ <ul> đó
        mail_items = mail_div.find_all("li")
        if len(mail_items) >= 3:
            # Lấy thẻ <a> bên trong thẻ <li> thứ 3
            mail_link = mail_items[2].find("a")
            if mail_link:
                # Lấy nội dung văn bản của thẻ <a>
                location = mail_link.get_text(strip=True)
                return location
    return None


def extract_quan(soup):
    # Tìm thẻ <ul> có class là 'uk-breadcrumb'
    mail_div = soup.find("ul", class_="uk-breadcrumb")
    if mail_div:
        # Tìm tất cả thẻ <li> bên trong thẻ <ul> đó
        mail_items = mail_div.find_all("li")
        if len(mail_items) >= 4:
            # Lấy thẻ <a> bên trong thẻ <li> thứ 3
            mail_link = mail_items[3].find("a")
            if mail_link:
                # Lấy nội dung văn bản của thẻ <a>
                location = mail_link.get_text(strip=True)
                return location
    return None


def extract_loainha(soup):
    # Tìm thẻ <ul> có class là 'uk-breadcrumb'
    mail_div = soup.find("ul", class_="uk-breadcrumb")
    if mail_div:
        # Tìm tất cả thẻ <li> bên trong thẻ <ul> đó
        mail_items = mail_div.find_all("li")
        if len(mail_items) >= 2:
            # Lấy thẻ <a> bên trong thẻ <li> thứ 3
            mail_link = mail_items[1].find("a")
            if mail_link:
                # Lấy nội dung văn bản của thẻ <a>
                location = mail_link.get_text(strip=True)
                return location
    return None


def extract_huongnha(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Hướng nhà" in strong_tag.text:
            return li.get_text(separator=" ").replace("Hướng nhà:", "").strip()
    return None


def extract_huongbancong(soup):
    list_items = soup.select(".uk-list li")
    for li in list_items:
        strong_tag = li.select_one("strong")
        if strong_tag and "Hướng ban công" in strong_tag.text:
            return li.get_text(separator=" ").replace("Hướng ban công:", "").strip()
    return None


import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_html_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def extract_info(url, data=[], links_=[]):

    for i, link1 in zip(range(1, len(links_) + 1), links_):
        content = get_html_content(link1)  # Fetch HTML content from the URL
        link = BeautifulSoup(content, "html.parser")  # Parse the HTML
        title_element = link.find("h1", class_="uk-panel-title")
        if title_element:
            title = title_element.text
        else:
            title = "None"
        ten = extract_name(link)
        diachi = extract_diachi123(link)
        gia = extract_price(link)

        sophongngu = extract_sophongngu123(link)
        sonhawc = extract_sophongwc(link)
        dientich = extract_dientich123(link)
        matin = extract_matin(link)
        ngaydang = extract_ngaydang123(link)
        email = extract_email(link)
        sdt = extract_sdt(link)
        huongnha = extract_huongnha(link)
        bancong = extract_huongbancong(link)
        loainha = extract_loainha(link)
        quan = extract_quan(link)
        thanhpho = extract_thanhpho(link)
        print(
            f"ten: {ten}, diachi: {diachi}, gia: {gia}, dientich: {dientich}, sophongngu: {sophongngu}, sonhawc: {sonhawc}, matin: {matin}, ngaydang: {ngaydang}, email: {email}, sdt: {sdt}"
        )

        row = {
            "Tiêu đề": title,
            "Diện tích(m2)": dientich,
            "Số phòng ngủ": sophongngu,
            "Số phòng WC": sonhawc,
            "Thời gian đăng": ngaydang,
            "Tỉnh/Thành": thanhpho,
            "Quận/Huyện": quan,
            "Hướng nhà": huongnha,
            "Hướng ban công": bancong,
            "Loại nhà": loainha,
            "Giá(Tỷ)": gia,
            "link": link1,
        }

        data.append(row)


def get_next_page_url(soup):
    next_link = soup.select_one('.uk-pagination a[rel="next"]')
    if next_link:
        return next_link["href"]
    else:
        return None


def crawl_info(start_url, num_pages):
    all_info = []
    current_url = start_url
    pages_crawled = 0

    while current_url and pages_crawled < num_pages:
        content = get_html_content(current_url)

        if content:
            soup = BeautifulSoup(content, "html.parser")
            print(get_next_page_url(soup))
            links_ = extract_links_from_divs(soup)
            print(links_)
            extract_info(soup, all_info, links_)
            next_url = get_next_page_url(soup)
            current_url = next_url
            print(current_url)
            pages_crawled += 1
        else:
            break

    return all_info


start_url = "https://batdongsan.vn/ban-nha/p2"
all_info = crawl_info(start_url, num_pages=2)
df = pd.DataFrame(all_info)

# Save the DataFrame to a CSV file
df.to_csv("page(291-320).csv", index=False, encoding="utf-8-sig")
