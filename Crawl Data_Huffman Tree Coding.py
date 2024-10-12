import urllib.request
from bs4 import BeautifulSoup
import re
from collections import Counter
import math


# Hàm lấy dữ liệu từ URL (sử dụng urllib):
def crawl_data_from_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')                      # Đọc và giải mã dữ liệu thành chuỗi
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu từ URL: {e}")
        return ""


# Hàm loại bỏ code HTML, chỉ giữ lại văn bản:
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    text = soup.get_text()  # Lấy toàn bộ văn bản, bỏ qua các thẻ HTML
    return text


# Hàm đếm tần suất xuất hiện của các ký tự ASCII:
def count_ascii_characters(text):
    # Bỏ các ký tự không cần đếm |, <, >:
    text = re.sub(r'[|<>]', '', text)

    # Chỉ giữ các ký tự ASCII (từ 0 đến 255):
    ascii_text = ''.join([char for char in text if ord(char) < 256])

    # Đếm tần suất của các ký tự ASCII:
    frequencies = Counter(ascii_text)

    # Tạo một bảng tần suất cho tất cả các ký tự ASCII (256 ký tự):
    ascii_frequencies = {chr(i): frequencies.get(chr(i), 0) for i in range(256)}

    return ascii_frequencies


# Hàm chia nhóm các ký tự có tần suất gần nhau:
def group_frequencies(frequencies, threshold=5):
    grouped_frequencies = {}

    # Sắp xếp các ký tự theo tần suất giảm dần:
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    current_group = []
    prev_freq = sorted_freq[0][1]

    for char, freq in sorted_freq:
        if abs(prev_freq - freq) <= threshold:
            current_group.append((char, freq))
        else:
            grouped_frequencies[prev_freq] = current_group
            current_group = [(char, freq)]
        prev_freq = freq

    if current_group:
        grouped_frequencies[prev_freq] = current_group

    return grouped_frequencies


# Hàm tính số bit tối thiểu cần thiết để mã hóa mỗi ký tự:
def calculate_min_bits(frequencies):
    total_chars = sum(frequencies.values())
    return math.ceil(math.log2(total_chars))


# Hàm chính để chạy chương trình:
if __name__ == "__main__":
    # Nhập URL từ bàn phím
    url = input("Nhập URL của trang web: ")

    # Crawl dữ liệu từ URL:
    raw_html = crawl_data_from_url(url)

    if raw_html:
        print("Đã lấy dữ liệu thành công, đang bắt đầu xử lý...")

        # Loại bỏ code HTML:
        cleaned_text = clean_html(raw_html)

        # Đếm tần suất xuất hiện của các ký tự ASCII:
        frequencies = count_ascii_characters(cleaned_text)

        # Chia các nhóm tần suất gần nhau:
        grouped_frequencies = group_frequencies(frequencies)

        # In kết quả nhóm tần suất:
        print("* Nhóm các ký tự với tần suất gần bằng nhau:")
        for group, chars in grouped_frequencies.items():
            print(f"\nTần suất {group}:")
            for char, freq in chars:
                if char == ' ':
                    print("'Space'", freq)
                elif char == '\n':
                    print("'Newline'", freq)
                else:
                    print(f"'{char}': {freq}")

        # Tính số bit tối thiểu cần để mã hóa:
        min_bits = calculate_min_bits(frequencies)
        print(f"\nSố bit tối thiểu cần thiết để mã hóa: {min_bits} bits")

    else:
        print("Không thể lấy dữ liệu từ URL cung cấp.")