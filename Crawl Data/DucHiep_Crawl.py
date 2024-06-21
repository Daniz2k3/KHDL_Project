
#  Cào dữ liệu bằng cách dùng selenium

""" Cào dữ liệu (web scraping) bằng Selenium là quá trình sử dụng thư viện Selenium để tự động hóa trình duyệt web nhằm truy cập, 
thu thập và trích xuất dữ liệu từ các trang web. Selenium là một công cụ mạnh mẽ thường được sử dụng cho kiểm thử tự động
các ứng dụng web, nhưng nó cũng rất hiệu quả trong việc cào dữ liệu từ các trang web động, nơi mà nội dung được tải động thông qua JavaScript.
"""


# Các bước để cài đặt 
import numpy as np
from selenium import webdriver
import csv
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options


# Khởi tạo ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")  # Tắt hỗ trợ GPU

# Cấu hình đường dẫn ChromeDriver
chrome_options.add_argument("webdriver.chrome.driver=/usr/lib/chromium-browser/chromedriver")

# Khởi tạo ChromeDriver với các tùy chọn
driver = webdriver.Chrome(options=chrome_options)

# Truy cập tới web batdongsan.vn
driver.get("https://batdongsan.vn/ban-nha/p304") # chữ p304 tương ứng với page 304
sleep(random.randint(5,10))

# Khởi tạo biến đếm trang
count = 304  # page bắt đầu lấy

# Vòng lặp qua các trang
while count <= 305:  # page kết thúc
    try:
        print("Crawl Page " + str(count))
        
        # Lấy các thông tin bên ngoài các item

        # Lấy link và tên
        elems = driver.find_elements(By.CSS_SELECTOR, ".name [href]")
        title = [elem.text for elem in elems][:-5]  # Lấy tên và bỏ đi 5 mục cuối
        links = [elem.get_attribute('href') for elem in elems][:-5]  # Lấy link và bỏ đi 5 mục cuối
        
        # Lấy giá nhà
        elems_price = driver.find_elements(By.CSS_SELECTOR, ".meta .price")
        price = [elem.text for elem in elems_price]  # Lấy giá

        # Lấy thời gian đăng bán
        elems = driver.find_elements(By.CSS_SELECTOR, ".timeago ")
        time = [elem.get_attribute('datetime') for elem in elems]  # Lấy thời gian đăng bán

        # Lấy diện tích
        dientich1 = []
        for i in range(1, len(title) + 1):
            try:
                elems_dientich = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div[1]/div[1]/div/div/div[2]/div/div[{i}]/div/div[2]/div[2]/span[2]")
                dientich1.append(elems_dientich.text)  # Lấy diện tích
            except NoSuchElementException:
                dientich1.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

        # Tạo DataFrame từ các thông tin bên ngoài
        df1 = pd.DataFrame(list(zip(title, price, links, time)), columns=['title', 'price', 'link_item', 'time'])
        df1['idx'] = np.arange(0, len(df1))  # Thêm cột chỉ số

        df2 = pd.DataFrame(list(zip(dientich1, list(range(len(dientich1))))), columns=['dientich1', 'idx'])

        df3 = df1.merge(df2, on='idx')  # Kết hợp các DataFrame lại với nhau
        
        # Lấy các thông tin bên trong các item
        dientich, phongwc, phongngu, diachi, huongnha, huongbancong, loainha, tinh, huyen = [], [], [], [], [], [], [], [], []
        for i in range(len(title)):
            driver.get(links[i])  # Truy cập vào từng liên kết
            try:
                elems_phongwc = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[3]")
                phongwc.append(elems_phongwc.text)  # Lấy số phòng WC
            except NoSuchElementException:
                phongwc.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_diachi = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[6]")
                diachi.append(elems_diachi.text)  # Lấy địa chỉ
            except NoSuchElementException:
                diachi.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_phongngu = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[2]")
                phongngu.append(elems_phongngu.text)  # Lấy số phòng ngủ
            except NoSuchElementException:
                phongngu.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_huongnha = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[4]")
                huongnha.append(elems_huongnha.text)  # Lấy hướng nhà
            except NoSuchElementException:
                huongnha.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_huongbancong = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[5]")
                huongbancong.append(elems_huongbancong.text)  # Lấy hướng ban công
            except NoSuchElementException:
                huongbancong.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_dientich = driver.find_element(By.XPATH, f"/html/body/div[6]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div[2]/ul/li[1]")
                dientich.append(elems_dientich.text)  # Lấy diện tích
            except NoSuchElementException:
                dientich.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_loainha = driver.find_element(By.XPATH, f"/html/body/div[4]/div/div/ul/li[2]/a")
                loainha.append(elems_loainha.text)  # Lấy loại nhà
            except NoSuchElementException:
                loainha.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_tinh = driver.find_element(By.XPATH, f"/html/body/div[4]/div/div/ul/li[3]/a")
                tinh.append(elems_tinh.text)  # Lấy tỉnh
            except NoSuchElementException:
                tinh.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            try:
                elems_huyen = driver.find_element(By.XPATH, f"/html/body/div[4]/div/div/ul/li[4]/a")
                huyen.append(elems_huyen.text)  # Lấy huyện
            except NoSuchElementException:
                huyen.append("")  # Nếu không tìm thấy, thêm chuỗi rỗng

            driver.back()  # Quay lại trang trước

        # Tạo các DataFrame cho từng thuộc tính
        df_dientich = pd.DataFrame(list(zip(dientich, list(range(len(dientich))))), columns=['dientich', 'idx'])
        df_phongwc = pd.DataFrame(list(zip(phongwc, list(range(len(phongwc))))), columns=['phongwc', 'idx'])
        df_diachi = pd.DataFrame(list(zip(diachi, list(range(len(diachi))))), columns=['diachi', 'idx'])
        df_phongngu = pd.DataFrame(list(zip(phongngu, list(range(len(phongngu))))), columns=['phongngu', 'idx'])
        df_huongnha = pd.DataFrame(list(zip(huongnha, list(range(len(huongnha))))), columns=['huongnha', 'idx'])
        df_huongbancong = pd.DataFrame(list(zip(huongbancong, list(range(len(huongbancong))))), columns=['huongbancong', 'idx'])
        df_loainha = pd.DataFrame(list(zip(loainha, list(range(len(loainha))))), columns=['loainha', 'idx'])
        df_tinh = pd.DataFrame(list(zip(tinh, list(range(len(tinh))))), columns=['tinh', 'idx'])
        df_huyen = pd.DataFrame(list(zip(huyen, list(range(len(huyen))))), columns=['huyen', 'idx'])
        
        # Kết hợp các DataFrame lại với nhau
        result = df_dientich.merge(df_phongwc, on='idx').merge(df_diachi, on='idx').merge(df_phongngu, on='idx').merge(df_huongnha, on='idx').merge(df_huongbancong, on='idx').merge(df_loainha, on='idx').merge(df_tinh, on='idx').merge(df_huyen, on='idx')

        # Kết hợp result với df3 để tạo data
        data = df3.merge(result, on='idx')

        # Lưu dữ liệu vào file CSV
        if count == 304:
            data.to_csv('page(304-305).csv', index=False, encoding='utf-8-sig')  # Lưu dữ liệu vào file CSV, lần đầu tiên với header
        else:
            data.to_csv('page(304-305).csv', mode='a', header=False, index=False, encoding='utf-8-sig')  # Append dữ liệu vào file CSV

        # Xóa các DataFrame cũ để giải phóng bộ nhớ
        del df1, df2, df3, df_dientich, df_phongwc, df_diachi, df_phongngu, df_huongnha, df_huongbancong, df_loainha, df_tinh, df_huyen, result, data

        # Chuyển sang trang tiếp theo
        next_pagination_cmt = driver.find_element(By.XPATH, "/html/body/div[6]/div/div/div[1]/div[2]/div/ul/li[8]")
        next_pagination_cmt.click()  # Click vào nút chuyển trang
        print("Clicked on button next page!")
        sleep(random.randint(1, 3))  # Chờ ngẫu nhiên từ 1 đến 3 giây để tránh bị chặn bởi trang web
        count += 1  # Tăng biến đếm trang lên
    except ElementNotInteractableException:
        print("Element Not Interactable Exception!")
        break  # Thoát khỏi vòng lặp nếu không thể tương tác với phần tử

# Đóng trình duyệt sau khi hoàn thành
driver.quit()

""" QUÁ TRÌNH CÀO DỮ LIỆU CỦA EM : em đã sử dụng
 * By.CSS_SELECTOR : là cú pháp được sử dụng để chọn các phần tử trong tài liệu HTML dựa trên các yếu tố như ID, lớp (class), 
   thuộc tính, v.v. Đây là phương pháp rất mạnh mẽ và linh hoạt cho phép bạn chọn các phần tử một cách nhanh chóng và hiệu quả.
 * By.XPath là một ngôn ngữ để chọn các nút trong tài liệu XML (và HTML). 
   XPath cung cấp nhiều cách linh hoạt và mạnh mẽ để tìm kiếm các phần tử trên trang web dựa trên cấu trúc của tài liệu.
EM SỬ DỤNG PHƯƠNG PHÁP DÙNG THƯ VIỆN SELENIUM LÀ VÌ : 
   Trang web có một số ngôi nhà không cung cấp API điều đó không thể cào dữ liệu được vì thế em quyết định dùng thư viện SELENIUM
   
   Lợi ích của việc sử dụng SELENIUM :
   - Không cần API: Không phải trang web nào cũng cung cấp API, trong nhiều trường hợp, để lấy được dữ liệu cần thiết, 
                    bạn phải cào trực tiếp từ trang web.
   - Truy cập toàn bộ nội dung trang: Selenium cho phép bạn truy cập vào toàn bộ nội dung trang web như một người dùng thực thụ
                                      bao gồm cả các phần tử được tải động (sử dụng JavaScript) mà có thể không có trong API
   - Không cần phải tìm hiểu API: Đôi khi API có thể phức tạp, yêu cầu các khóa API hoặc có giới hạn tốc độ
                                  sử dụng Selenium có thể đơn giản hơn vì bạn chỉ cần mô phỏng các hành động của người dùng trên trang web
   - Xử lý CAPTCHA và bảo mật: Một số trang web có thể sử dụng CAPTCHA hoặc các biện pháp bảo mật khác để ngăn chặn việc cào dữ liệu
                               Selenium có thể được sử dụng cùng với các công cụ khác để vượt qua các biện pháp này
Tuy nhiên hiệu suất cào lại thấp hơn tại vì nó phải mở trình duyệt web ảo rồi cào chứ không truy cập trực tiếp đến để cào

"""
# Đọc file vừa mới cào về
data= pd.read_csv('page(304-305).csv')
data


# Xử lý data
#Xử lý cột giá
def convert_to_billion(price):
    # Loại bỏ khoảng trắng
    price = price.replace(' ', '')
    # Nếu là tỷ
    if 'tỷ' in price:
        return float(price.replace('tỷ', ''))
    # Nếu là triệu
    elif 'triệu' in price:
        return float(price.replace('triệu', '')) / 1000
    # Nếu là thỏa thuận
    elif 'Thỏa thuận' in price:
        return np.nan
    else:
        return None  # Trong trường hợp giá trị không hợp lệ
        
# Áp dụng hàm chuyển đổi cho cột price
data['Giá'] = data['price'].apply(convert_to_billion)
# Xóa cột 'price'
data = data.drop(columns=['price'])

# Xử lý cột diện tích
data['Diện tích(m2)'] = data['dientich1'].str[:-2]
data['Diện tích(m2)'].info()
data = data.drop(columns=['dientich1'])

# Tại vì dữ liệu các cột, phong wc, phong ngủ,.... tại các nhà có nhà có và có nhà không nên có thể mã xpath của chúng cũng có thể giống nhau nên ta cần lọc chúng ra

# Xử lý cột diện tích
def fix_rows_dt(row):
    if pd.notna(row['huongbancong']) and row['huongbancong'].startswith('Diện tích:'):
        row['dientich'], row['huongbancong'] = row['huongbancong'], row['dientich']
    elif pd.notna(row['phongwc']) and row['phongwc'].startswith('Diện tích:'):
        row['phongwc'], row['dientich'] = row['dientich'], row['phongwc']
    elif pd.notna(row['phongngu']) and row['phongngu'].startswith('Diện tích:'):
        row['phongngu'], row['dientich'] = row['dientich'], row['phongngu']    
    elif pd.notna(row['diachi']) and row['diachi'].startswith('Diện tích:'):
        row['diachi'], row['dientich'] = row['dientich'], row['diachi']
    elif pd.notna(row['huongnha']) and row['huongnha'].startswith('Diện tích:'):
        row['dientich'], row['huongnha'] = row['huongnha'], row['dientich']
    return row

data = data.apply(fix_rows_dt, axis=1)

# Xử lý cột phòng ngủ
def fix_rows_pn(row):
    if pd.notna(row['huongbancong']) and row['huongbancong'].startswith('Phòng ngủ:'):
        row['phongngu'], row['huongbancong'] = row['huongbancong'], row['phongngu']
    elif pd.notna(row['phongwc']) and row['phongwc'].startswith('Phòng ngủ:'):
        row['phongwc'], row['phongngu'] = row['phongngu'], row['phongwc']  
    elif pd.notna(row['diachi']) and row['diachi'].startswith('Phòng ngủ:'):
        row['diachi'], row['phongngu'] = row['phongngu'], row['diachi']
    elif pd.notna(row['huongnha']) and row['huongnha'].startswith('Phòng ngủ:'):
        row['phongngu'], row['huongnha'] = row['huongnha'], row['phongngu']
    elif pd.notna(row['dientich']) and row['dientich'].startswith('Phòng ngủ:'):
        row['phongngu'], row['dientich'] = row['dientich'], row['phongngu']    
    return row

data = data.apply(fix_rows_pn, axis=1)

#Xử lý cột phòng wc
def fix_rows_wc(row):
    if pd.notna(row['huongbancong']) and row['huongbancong'].startswith('Phòng WC:'):
        row['phongwc'], row['huongbancong'] = row['huongbancong'], row['phongwc']
    elif pd.notna(row['diachi']) and row['diachi'].startswith('Phòng WC:'):
        row['diachi'], row['phongwc'] = row['phongwc'], row['diachi']
    elif pd.notna(row['huongnha']) and row['huongnha'].startswith('Phòng WC:'):
        row['phongwc'], row['huongnha'] = row['huongnha'], row['phongwc']
    elif pd.notna(row['phongngu']) and row['phongngu'].startswith('Phòng WC:'):
        row['phongwc'], row['phongngu'] = row['phongngu'], row['phongwc']
    elif pd.notna(row['dientich']) and row['dientich'].startswith('Phòng WC:'):
        row['dientich'], row['phongwc'] = row['phongwc'], row['dientich']    
    return row

data = data.apply(fix_rows_wc, axis=1)

#Xử lý cột hướng nhà
def fix_rows_hn(row):
    if pd.notna(row['dientich']) and row['dientich'].startswith('Hướng nhà:'):
        row['dientich'], row['huongnha'] = row['huongnha'], row['dientich']
    elif pd.notna(row['phongwc']) and row['phongwc'].startswith('Hướng nhà:'):
        row['phongwc'], row['huongnha'] = row['huongnha'], row['phongwc']
    elif pd.notna(row['phongngu']) and row['phongngu'].startswith('Hướng nhà:'):
        row['phongngu'], row['huongnha'] = row['huongnha'], row['phongngu']    
    elif pd.notna(row['diachi']) and row['diachi'].startswith('Hướng nhà:'):
        row['diachi'], row['huongnha'] = row['huongnha'], row['diachi']
    elif pd.notna(row['huongbancong']) and row['huongbancong'].startswith('Hướng nhà:'):
        row['huongbancong'], row['huongnha'] = row['huongnha'], row['huongbancong']
    return row

data = data.apply(fix_rows_hn, axis=1)

#Xử lý cột hướng ban công
def fix_rows_hbc(row):
    if pd.notna(row['dientich']) and row['dientich'].startswith('Hướng ban công:'):
        row['dientich'], row['huongbancong'] = row['huongbancong'], row['dientich']
    elif pd.notna(row['phongwc']) and row['phongwc'].startswith('Hướng ban công:'):
        row['phongwc'], row['huongbancong'] = row['huongbancong'], row['phongwc']
    elif pd.notna(row['phongngu']) and row['phongngu'].startswith('Hướng ban công:'):
        row['phongngu'], row['huongbancong'] = row['huongbancong'], row['phongngu']    
    elif pd.notna(row['diachi']) and row['diachi'].startswith('Hướng ban công:'):
        row['diachi'], row['huongbancong'] = row['huongbancong'], row['diachi']
    elif pd.notna(row['huongnha']) and row['huongnha'].startswith('Hướng ban công:'):
        row['huongbancong'], row['huongnha'] = row['huongnha'], row['huongbancong']
    return row

data = data.apply(fix_rows_hbc, axis=1)

#Xử lý cột địa chỉ
def fix_rows_dc(row):
    if pd.notna(row['dientich']) and row['dientich'].startswith('Địa chỉ:'):
        row['dientich'], row['diachi'] = row['diachi'], row['dientich']
    elif pd.notna(row['phongwc']) and row['phongwc'].startswith('Địa chỉ:'):
        row['phongwc'], row['diachi'] = row['diachi'], row['phongwc']
    elif pd.notna(row['phongngu']) and row['phongngu'].startswith('Địa chỉ:'):
        row['phongngu'], row['diachi'] = row['diachi'], row['phongngu']    
    elif pd.notna(row['huongbancong']) and row['huongbancong'].startswith('Địa chỉ:'):
        row['diachi'], row['huongbancong'] = row['huongbancong'], row['diachi']
    elif pd.notna(row['huongnha']) and row['huongnha'].startswith('Địa chỉ:'):
        row['diachi'], row['huongnha'] = row['huongnha'], row['diachi']
    return row

data = data.apply(fix_rows_dc, axis=1)


data = data.drop(columns='diachi')
data = data.drop(columns='dientich')
data = data.drop(columns='idx')
#Chuẩn hóa cột phòng wc loại bỏ các ký tự, chỉ giữ lại số
data['phongwc'] = pd.to_numeric(data['phongwc'].str.extract(r'(\d+)', expand=False), errors='coerce')

#Chuẩn hóa cột phòng ngủ loại bỏ các ký tự, chỉ giữ lại số
data['phongngu'] = pd.to_numeric(data['phongngu'].str.extract(r'(\d+)', expand=False), errors='coerce')

#Đổi tên các cột
data = data.rename(columns={'phongngu': 'Số phòng ngủ'})
data = data.rename(columns={'phongwc': 'Số phòng WC'})
data = data.rename(columns={'title': 'Tiêu đề'})
data = data.rename(columns={'link_item': 'Link'})
data = data.rename(columns={'time': 'Thời gian đăng'})
data = data.rename(columns={'tinh': 'Tỉnh/Thành'})
data = data.rename(columns={'huyen': 'Quận/Huyện'})
data = data.rename(columns={'huongnha': 'Hướng nhà'})
data = data.rename(columns={'huongbancong': 'Hướng ban công'})
data = data.rename(columns={'loainha': 'Loại nhà'})

#Định dạng lại type của cột thời gian đăng và cột diện tích
# Chuyển đổi cột 'Thời gian đăng' thành kiểu datetime
data['Thời gian đăng'] = pd.to_datetime(data['Thời gian đăng'])
# Lấy chỉ phần ngày (loại bỏ phần giờ)
data['Thời gian đăng'] = data['Thời gian đăng'].dt.date
# Chuyển đổi định dạng thời gian
data['Thời gian đăng'] = pd.to_datetime(data['Thời gian đăng']).dt.strftime('%d/%m/%Y')

# Chuyển đổi cột 'diện tích' sang kiểu float
data['Diện tích(m2)'] = data['Diện tích(m2)'].astype(float)

#Chuyển đổi thứ tự các cột trong data frame
data = data.reindex(columns=['Tiêu đề', 'Diện tích(m2)', 'Số phòng ngủ', 'Số phòng WC', 'Thời gian đăng', 'Tỉnh/Thành', 'Quận/Huyện', 'Hướng nhà', 'Hướng ban công', 'Loại nhà', 'Giá', 'Link'])

result = data
result.to_csv('df(page304-305).csv', index=False, encoding='utf-8-sig')

# Như vậy file data đã cào và xử lý hoàn chỉnh là df(page304-305).csv


