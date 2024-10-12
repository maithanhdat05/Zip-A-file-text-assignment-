import urllib.request
import re
from collections import Counter


# Hàm crawl dữ liệu từ link (sử dụng urllib):
def crawl_articles(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')          # Đọc dữ liệu và giải mã thành chuỗi văn bản
    except urllib.error.URLError as e:
        print(f"Lỗi khi lấy dữ liệu từ URL: {e}")
        return ""


# Hàm loại bỏ code HTML:
def remove_html_tags(text):
    clean = re.compile('<.*?>')                             # Biểu thức chính quy để tìm các thẻ HTML
    return re.sub(clean, '', text)                     # Thay thế các thẻ HTML bằng chuỗi rỗng


# Hàm đếm số lần xuất hiện của các ký tự:
def count_character_frequencies(text):
    # Bỏ các ký tự không cần thiết: |, <, >
    text = re.sub(r'[|<>]', '', text)

    # Chỉ giữ lại các ký tự ASCII, bao gồm dấu cách và các dấu câu, loại bỏ những ký tự ngoài bảng ASCII:
    ascii_text = ''.join([char for char in text if ord(char) < 256])

    # Đếm tần suất xuất hiện của các ký tự:
    frequencies = Counter(ascii_text)

    return frequencies


# Hàm làm tròn tần suất gần bằng nhau (lệch từ 1-5):
def adjust_frequencies(frequencies, threshold=5):
    adjusted_frequencies = {}

    # Sắp xếp các ký tự theo tần suất:
    sorted_chars = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

    # Điều chỉnh các tần suất gần bằng nhau:
    prev_char, prev_freq = sorted_chars[0]
    adjusted_frequencies[prev_char] = prev_freq

    for char, freq in sorted_chars[1:]:
        if abs(prev_freq - freq) <= threshold:
            adjusted_frequencies[char] = prev_freq                   # Nếu gần bằng, gán giá trị bằng nhau
        else:
            adjusted_frequencies[char] = freq                        # Ngược lại, giữ nguyên tần suất
        prev_char, prev_freq = char, adjusted_frequencies[char]

    return adjusted_frequencies


# Hàm chính:
if __name__ == "__main__":
    # Nhập URL từ bàn phím
    url = input("Nhập URL của trang web: ")

    # Crawl dữ liệu từ link:
    input_text = crawl_articles(url)

    if input_text:
        print("Đã lấy dữ liệu thành công, bắt đầu xử lý...")

        # Loại bỏ code HTML:
        cleaned_text = remove_html_tags(input_text)

        # Đếm tần suất xuất hiện của các ký tự ASCII:
        frequencies = count_character_frequencies(cleaned_text)

        # Điều chỉnh các tần suất gần bằng nhau (lệch từ 1-5):
        adjusted_frequencies = adjust_frequencies(frequencies)

        # In kết quả:
        print("Tần suất xuất hiện của các ký tự (bao gồm dấu cách, dấu câu):")
        for char, freq in adjusted_frequencies.items():
            if char == ' ':
                print("'Space':", freq)
            elif char == '\n':
                print("'Newline':", freq)
            else:
                print(f"'{char}': {freq}")
    else:
        print("Không thể lấy dữ liệu từ URL cung cấp.")