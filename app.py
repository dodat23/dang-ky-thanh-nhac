import streamlit as st
import json
import os
from datetime import datetime, timedelta

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hệ Thống Đăng Ký Thanh Nhạc",
    page_icon="🎶",
    layout="centered"
)

# CSS tùy chỉnh giao diện tối chuyên nghiệp, phong cách Studio âm nhạc
st.markdown("""
    <style>
    /* Toàn bộ nền trang */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Tùy chỉnh ô nhập liệu và selectbox */
    .stTextInput > div > div > input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    .stSelectbox > div > div > div {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    
    /* Nút bấm chính */
    div.stButton > button {
        border-radius: 10px;
        font-weight: bold;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        border: none;
        width: 100%;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
    }

    /* Thẻ Card hiển thị thông tin ca học */
    .card {
        padding: 22px;
        border-radius: 16px;
        background: #1e293b;
        border: 1px solid #334155;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    
    /* Tiêu đề trong card */
    .card h4 {
        color: #38bdf8;
        margin-bottom: 8px;
    }

    /* Thanh thông báo info */
    .stAlert {
        background-color: #1e293b;
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "data_dang_ky.json"
CA_HOC_MAC_DINH = {
    "Ca 1 (8:00 - 9:45)": 5,
    "Ca 2 (9:45 - 11:30)": 5
}

def lay_ngay_thu_7_gan_nhat():
    ngay_hien_tai = datetime.now()
    so_ngay_den_thu_7 = (5 - ngay_hien_tai.weekday()) % 7
    thu_7 = ngay_hien_tai + timedelta(days=so_ngay_den_thu_7)
    return thu_7.strftime("%d/%m/%Y")

def tai_du_lieu():
    tuan_hien_tai = datetime.now().strftime("%Y-W%V")
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data.get("tuan") != tuan_hien_tai:
                return tao_du_lieu_moi(tuan_hien_tai)
            return data
    else:
        return tao_du_lieu_moi(tuan_hien_tai)

def tao_du_lieu_moi(tuan_hien_tai):
    data = {
        "tuan": tuan_hien_tai,
        "ngay_thu_7": lay_ngay_thu_7_gan_nhat(),
        "dang_ky": {
            "Ca 1 (8:00 - 9:45)": [],
            "Ca 2 (9:45 - 11:30)": []
        }
    }
    luu_du_lieu(data)
    return data

def luu_du_lieu(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = tai_du_lieu()
ngay_thu_7 = data["ngay_thu_7"]

# Tiêu đề trang
st.markdown("<h1 style='text-align: center; color: #a855f7;'>🎶 ĐĂNG KÝ HỌC THANH NHẠC</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>✨ Luyện giọng thăng hoa cùng phòng thu lớp mình ✨</p>", unsafe_allow_html=True)

st.info(f"📅 **Lịch học Thứ 7 tuần này:** `{ngay_thu_7}` (Thời gian: **8:00 - 11:30**)\n\n*💡 Hệ thống tự động reset danh sách đăng ký vào Thứ Hai hàng tuần.*")

# Thống kê sĩ số tổng quan
tong_so_hoc_vien = sum(len(ds) for ds in data["dang_ky"].values())
st.markdown(f"🎤 **Tổng số học viên đã đăng ký tuần này:** `{tong_so_hoc_vien}/10 chỗ`")
st.progress(tong_so_hoc_vien / 10)

st.write("")

# Hiển thị 2 ca học dưới dạng 2 cột thẻ card tối màu
col1, col2 = st.columns(2)

with col1:
    siso_1 = len(data["dang_ky"]["Ca 1 (8:00 - 9:45)"])
    st.markdown(f"""
        <div class="card">
            <h4>🌅 Ca 1 (8:00 - 9:45)</h4>
            <p style="color: #94a3b8; font-size: 14px;">Trạng thái: <b style="color: #38bdf8;">{siso_1}/5</b> chỗ đã đặt</p>
            <hr style="border-color: #334155; margin: 5px 0 10px 0;">
    """, unsafe_allow_html=True)
    if siso_1 == 0:
        st.caption("Chưa có học viên đăng ký")
    else:
        for idx, hv in enumerate(data["dang_ky"]["Ca 1 (8:00 - 9:45)"], 1):
            st.write(f"{idx}. {hv}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    siso_2 = len(data["dang_ky"]["Ca 2 (9:45 - 11:30)"])
    st.markdown(f"""
        <div class="card">
            <h4>☀️ Ca 2 (9:45 - 11:30)</h4>
            <p style="color: #94a3b8; font-size: 14px;">Trạng thái: <b style="color: #38bdf8;">{siso_2}/5</b> chỗ đã đặt</p>
            <hr style="border-color: #334155; margin: 5px 0 10px 0;">
    """, unsafe_allow_html=True)
    if siso_2 == 0:
        st.caption("Chưa có học viên đăng ký")
    else:
        for idx, hv in enumerate(data["dang_ky"]["Ca 2 (9:45 - 11:30)"], 1):
            st.write(f"{idx}. {hv}")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# Form đăng ký
st.subheader("✍️ Đăng Ký Lịch Học")
with st.container():
    ten_hoc_vien = st.text_input("Họ và tên học viên:", placeholder="Nhập tên của bạn...")
    
    ca_chon = st.selectbox(
        "Chọn ca học mong muốn:", 
        list(CA_HOC_MAC_DINH.keys()),
        format_func=lambda x: f"{x} (Còn {5 - len(data['dang_ky'][x])} chỗ)"
    )

    if st.button("Xác Nhận Đăng Ký"):
        ten_chuan_hoa = ten_hoc_vien.strip()
        if not ten_chuan_hoa:
            st.error("Vui lòng nhập tên của bạn!")
        else:
            da_dang_ky = False
            ca_cu = ""
            for ca, ds in data["dang_ky"].items():
                if ten_chuan_hoa in ds:
                    da_dang_ky = True
                    ca_cu = ca
                    break
            
            if da_dang_ky:
                st.warning(f"Bạn **{ten_chuan_hoa}** đã đăng ký ca **{ca_cu}** rồi! Mỗi người chỉ được chọn 1 ca.")
            else:
                if len(data["dang_ky"][ca_chon]) >= 5:
                    st.error(f"Ca **{ca_chon}** đã đủ 5/5 học viên. Vui lòng chọn ca còn lại!")
                else:
                    data["dang_ky"][ca_chon].append(ten_chuan_hoa)
                    luu_du_lieu(data)
                    st.success(f"🎉 Chúc mừng **{ten_chuan_hoa}** đã đăng ký thành công ca **{ca_chon}**!")
                    st.rerun()

st.divider()

# Khu vực kiểm tra & hủy lịch cá nhân
st.subheader("🔍 Kiểm Tra & Hủy Lịch Đã Đăng Ký")
with st.container():
    ten_kiem_tra = st.text_input("Nhập họ và tên để tìm lịch:", placeholder="Tên học viên cần tìm...", key="input_check")
    if st.button("Tra Cứu Lịch"):
        if not ten_kiem_tra.strip():
            st.warning("Vui lòng nhập tên để tìm kiếm.")
        else:
            tim_thay = False
            for ca, ds in data["dang_ky"].items():
                if ten_kiem_tra.strip() in ds:
                    tim_thay = True
                    st.info(f"Học viên **{ten_kiem_tra.strip()}** đang có lịch ở **{ca}**.")
                    if st.button("Hủy đăng ký ca này (để đổi ca)"):
                        data["dang_ky"][ca].remove(ten_kiem_tra.strip())
                        luu_du_lieu(data)
                        st.success("Đã hủy lịch thành công! Bạn có thể chọn lại ca mới ở trên.")
                        st.rerun()
                    break
            if not tim_thay:
                st.warning(f"Không tìm thấy dữ liệu đăng ký nào cho tên **{ten_kiem_tra.strip()}** trong tuần này.")