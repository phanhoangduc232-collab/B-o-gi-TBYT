# -*- coding: utf-8 -*-
"""
Danh mục 20 hạng mục thiết bị y tế theo YCBG số 2717/YCBG-BVE ngày 14/7/2026.
Số lượng (SL) và Đơn vị tính (DVT) đã được ĐỐI CHIẾU LẠI với bản scan gốc của YCBG
(bao gồm 2 chỗ sửa lỗi: TB02 = 18 (không phải 182), TB17 = 1 (không phải 13)).
"""

CATEGORIES = [
    {"ma": "TB01", "ten": "Bơm tiêm điện", "dvt": "Cái", "sl": 64, "nhom": "I. Thiết bị Hồi sức - Cấp cứu"},
    {"ma": "TB02", "ten": "Bơm tiêm điện (có kết nối từ xa, chuyên dụng cho Phòng phẫu thuật)", "dvt": "Cái", "sl": 18, "nhom": "I. Thiết bị Hồi sức - Cấp cứu"},
    {"ma": "TB03", "ten": "Bơm truyền dịch", "dvt": "Cái", "sl": 57, "nhom": "I. Thiết bị Hồi sức - Cấp cứu"},
    {"ma": "TB04", "ten": "Máy điện tim ≥ 12 kênh", "dvt": "Cái", "sl": 14, "nhom": "I. Thiết bị Hồi sức - Cấp cứu"},
    {"ma": "TB05", "ten": "Máy vỗ rung lồng ngực cao tần", "dvt": "Cái", "sl": 10, "nhom": "I. Thiết bị Hồi sức - Cấp cứu"},
    {"ma": "TB06", "ten": "Máy X-quang di động kỹ thuật số DR", "dvt": "Cái", "sl": 1, "nhom": "II. Thiết bị Chẩn đoán hình ảnh"},
    {"ma": "TB07", "ten": "Máy bơm tiêm điện 2 nòng (dùng cho phòng chụp CLVT)", "dvt": "Cái", "sl": 1, "nhom": "II. Thiết bị Chẩn đoán hình ảnh"},
    {"ma": "TB08", "ten": "Hệ thống máy đốt sóng cao tần (RFA)", "dvt": "Hệ thống", "sl": 1, "nhom": "II. Thiết bị Chẩn đoán hình ảnh"},
    {"ma": "TB09", "ten": "Hệ thống nội soi tiêu hóa (kèm AI và mô hình giả lập nội soi đại tràng)", "dvt": "Hệ thống", "sl": 1, "nhom": "III. Hệ thống Nội soi thăm dò chức năng"},
    {"ma": "TB10", "ten": "Hệ thống nội soi tiêu hóa (kèm AI)", "dvt": "Hệ thống", "sl": 1, "nhom": "III. Hệ thống Nội soi thăm dò chức năng"},
    {"ma": "TB11", "ten": "Máy kích thích điện một chiều xuyên sọ", "dvt": "Cái", "sl": 3, "nhom": "IV. Thiết bị thần kinh và sức khỏe tâm thần"},
    {"ma": "TB12", "ten": "Máy điện não vi tính", "dvt": "Cái", "sl": 1, "nhom": "IV. Thiết bị thần kinh và sức khỏe tâm thần"},
    {"ma": "TB13", "ten": "Máy lưu huyết não", "dvt": "Cái", "sl": 1, "nhom": "IV. Thiết bị thần kinh và sức khỏe tâm thần"},
    {"ma": "TB14", "ten": "Máy đa ký giấc ngủ", "dvt": "Cái", "sl": 2, "nhom": "IV. Thiết bị thần kinh và sức khỏe tâm thần"},
    {"ma": "TB15", "ten": "Hệ thống thăm dò chức năng hô hấp bằng phương pháp dao động xung ký", "dvt": "Hệ thống", "sl": 1, "nhom": "V. Thiết bị hô hấp"},
    {"ma": "TB16", "ten": "Máy chụp CT Conebeam", "dvt": "Cái", "sl": 1, "nhom": "VI. Thiết bị chuyên khoa Răng Hàm Mặt"},
    {"ma": "TB17", "ten": "Hệ thống khoan cắt xương dùng trong phẫu thuật hàm mặt", "dvt": "Hệ thống", "sl": 1, "nhom": "VI. Thiết bị chuyên khoa Răng Hàm Mặt"},
    {"ma": "TB18", "ten": "Máy đo thị trường", "dvt": "Cái", "sl": 1, "nhom": "VII. Thiết bị chuyên khoa Mắt"},
    {"ma": "TB19", "ten": "Máy chụp cắt lớp võng mạc OCT", "dvt": "Cái", "sl": 1, "nhom": "VII. Thiết bị chuyên khoa Mắt"},
    {"ma": "TB20", "ten": "Máy bào da", "dvt": "Cái", "sl": 1, "nhom": "VIII. Thiết bị chuyên khoa Thẩm mỹ và phẫu thuật tạo hình"},
]

CATEGORY_BY_MA = {c["ma"]: c for c in CATEGORIES}

FILE_TAGS = [
    ("catalogue", "Catalogue / tài liệu kỹ thuật chính hãng"),
    ("luu_hanh", "Giấy phép/Số lưu hành thiết bị y tế"),
    ("pl3", "Phụ lục III - Bảng đáp ứng kỹ thuật hàng hóa chào giá"),
    ("pl4", "Phụ lục IV - Kê khai cấu hình và thông số kỹ thuật chi tiết"),
    ("khac", "Tài liệu khác"),
]
