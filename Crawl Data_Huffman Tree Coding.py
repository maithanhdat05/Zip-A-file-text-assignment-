import urllib.request
from bs4 import BeautifulSoup
import re
from collections import Counter
import math


# Hàm lấy dữ liệu từ URL (sử dụng urllib):
def crawl_data_from_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')                                  # Đọc và giải mã dữ liệu thành chuỗi
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu từ URL: {e}")
        return ""


# Hàm loại bỏ code HTML, chỉ giữ lại văn bản trong thẻ chứa nội dung chính:
def clean_html(raw_html, tag):
    soup = BeautifulSoup(raw_html, 'html.parser')

    # Tìm thẻ người dùng chọn (article, content, div,...)
    content = soup.find(tag)                                                       # Thay tag bằng thẻ cụ thể của trang web

    if content:
        text = content.get_text()                                                  # Lấy toàn bộ văn bản, bỏ qua các code HTML
    else:
        print(f"Không tìm thấy thẻ {tag}, dùng toàn bộ văn bản trang.")
        text = soup.get_text()                                                     # Lấy toàn bộ văn bản nếu không tìm thấy thẻ

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


# Hàm lấy văn bản từ URL và thẻ HTML do người dùng nhập:
def get_text(url, tag):
    raw_html = crawl_data_from_url(url)
    if raw_html:
        print(f"Đã lấy dữ liệu thành công từ {url}")
        return clean_html(raw_html, tag)
    else:
        print(f"Không thể lấy dữ liệu từ URL: {url}")
        return ""


# Hàm chính để chạy chương trình:
if __name__ == "__main__":
    # Nhập URL và thẻ HTML từ bàn phím
    url = input("Nhập URL của trang web: ")
    tag = input("Nhập thẻ HTML (ví dụ: 'article', 'content', 'div', v.v.): ")

    # Lấy văn bản từ URL và thẻ người dùng chỉ định
    cleaned_text = get_text(url, tag)

    if cleaned_text:
        # Đếm tần suất xuất hiện của các ký tự ASCII:
        frequencies = count_ascii_characters(cleaned_text)

        # Chia các nhóm tần suất gần nhau:
        grouped_frequencies = group_frequencies(frequencies)

        # Trả kết quả dưới dạng dictionary:
        result_dict = {group: dict(chars) for group, chars in grouped_frequencies.items()}
        print("Kết quả nhóm các ký tự với tần suất gần bằng nhau:", result_dict)

        # Tính số bit tối thiểu cần để mã hóa:
        min_bits = calculate_min_bits(frequencies)
        print(f"\nSố bit tối thiểu cần thiết để mã hóa: {min_bits} bits")
    else:
        print("Không thể lấy văn bản từ URL cung cấp.")