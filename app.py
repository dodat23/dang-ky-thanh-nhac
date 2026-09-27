import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hệ Thống Đăng Ký Thanh Nhạc",
    page_icon="🎶",
    layout="centered"
)

# CSS tùy chỉnh giao diện Hồng - Trắng tinh tế, thanh lịch
st.markdown("""
    <style>
    .stApp {
        background-color: #fff5f7;
        color: #1f2937;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1f2937;
        border: 1px solid #f472b6;
        border-radius: 10px;
    }
    .stSelectbox > div > div > div {
        background-color: #ffffff;
        color: #1f2937;
        border: 1px solid #f472b6;
        border-radius: 10px;
    }
    div.stButton > button {
        border-radius: 10px;
        font-weight: bold;
        background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%);
        color: white;
        border: none;
        width: 100%;
        padding: 10px;
        box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #db2777 0%, #e11d48 100%);
        box-shadow: 0 6px 16px rgba(236, 72, 153, 0.5);
    }
    .card {
        padding: 22px;
        border-radius: 16px;
        background: #ffffff;
        border: 1px solid #fbcfe8;
        box-shadow: 0 10px 15px -3px rgba(244, 114, 182, 0.15);
        margin-bottom: 20px;
    }
    .card h4 {
        color: #db2777;
        margin-bottom: 8px;
    }
    .stAlert {
        background-color: #ffffff;
        color: #1f2937;
        border: 1px solid #fbcfe8;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

DATA_FILE = "data_dang_ky.json"

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
st.markdown("<h1 style='text-align: center; color: #db2777;'>🎶 ĐĂNG KÝ HỌC THANH NHẠC</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>✨ Luyện giọng thăng hoa cùng lớp học ✨</p>", unsafe_allow_html=True)

st.info(f"📅 **Lịch học Thứ 7 tuần này:** `{ngay_thu_7}` (Thời gian: **8:00 - 11:30**)\n\n*💡 Hệ thống tự động reset danh sách đăng ký vào Thứ Hai hàng tuần.*")

# Thống kê sĩ số tổng quan
tong_so_hoc_vien = sum(len(ds) for ds in data["dang_ky"].values())
st.markdown(f"🎤 **Tổng số học viên đã đăng ký tuần này:** `{tong_so_hoc_vien}/10 chỗ`")
st.progress(tong_so_hoc_vien / 10)

st.write("")

# Hiển thị 2 ca học dưới dạng 2 cột thẻ card trắng viền hồng
col1, col2 = st.columns(2)

with col1:
    siso_1 = len(data["dang_ky"]["Ca 1 (8:00 - 9:45)"])
    st.markdown(f"""
        <div class="card">
            <h4>🌅 Ca 1 (8:00 - 9:45)</h4>
            <p style="color: #4b5563; font-size: 14px;">Trạng thái: <b style="color: #db2777;">{siso_1}/5</b> chỗ đã đặt</p>
            <hr style="border-color: #fbcfe8; margin: 5px 0 10px 0;">
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
            <p style="color: #4b5563; font-size: 14px;">Trạng thái: <b style="color: #db2777;">{siso_2}/5</b> chỗ đã đặt</p>
            <hr style="border-color: #fbcfe8; margin: 5px 0 10px 0;">
    """, unsafe_allow_html=True)
    if siso_2 == 0:
        st.caption("Chưa có học viên đăng ký")
    else:
        for idx, hv in enumerate(data["dang_ky"]["Ca 2 (9:45 - 11:30)"], 1):
            st.write(f"{idx}. {hv}")
    st.markdown("</div>", unsafe_allow_html=True)


# ================= PHẦN ĐĂNG KÝ LỊCH HỌC (TỰ ĐỘNG CHUYỂN CA KHI CA 1 ĐẦY) =================
st.divider()
st.subheader("✍️ Đăng Ký Lịch Học")

if tong_so_hoc_vien < 10:
    with st.container():
        # Xóa sạch ô nhập tên bằng cách dùng key trong session_state nếu vừa submit xong
        if 'clear_input' in st.session_state and st.session_state['clear_input']:
            st.session_state['ten_input'] = ""
            st.session_state['clear_input'] = False

        ten_hoc_vien = st.text_input("Họ và tên học viên:", placeholder="Nhập tên của bạn...", key="ten_input")
        
        # Tự động xác định ca học: Nếu Ca 1 chưa đủ 5 người thì ưu tiên Ca 1, ngược lại tự động đẩy sang Ca 2
        if len(data["dang_ky"]["Ca 1 (8:00 - 9:45)"]) < 5:
            ca_tu_dong = "Ca 1 (8:00 - 9:45)"
            st.info("💡 Hệ thống tự động xếp bạn vào **Ca 1 (8:00 - 9:45)**.")
        else:
            ca_tu_dong = "Ca 2 (9:45 - 11:30)"
            st.info("💡 Ca 1 đã đủ 5 người. Hệ thống tự động xếp bạn vào **Ca 2 (9:45 - 11:30)**.")

        if st.button("Xác Nhận Đăng Ký"):
            ten_chuan_hoa = ten_hoc_vien.strip()
            if not ten_chuan_hoa:
                st.error("Vui lòng nhập tên của bạn!")
            else:
                # Kiểm tra xem học viên đã đăng ký chưa
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
                    if len(data["dang_ky"][ca_tu_dong]) >= 5:
                        st.error(f"Ca **{ca_tu_dong}** đã đủ 5/5 học viên!")
                    else:
                        data["dang_ky"][ca_tu_dong].append(ten_chuan_hoa)
                        luu_du_lieu(data)
                        st.session_state['clear_input'] = True
                        st.success(f"🎉 Chúc mừng **{ten_chuan_hoa}** đã đăng ký thành công **{ca_tu_dong}**!")
                        st.rerun()
else:
    st.success("🎉 **Lớp học đã hoàn tất đăng ký đủ 10/10 học viên!** Form đăng ký đã tạm đóng.")


# ================= PHẦN KIỂM TRA & HỦY LỊCH CÁ NHÂN =================
st.divider()
st.subheader("🔍 Kiểm Tra & Hủy Lịch Đã Đăng Ký")
with st.container():
    if 'clear_check' in st.session_state and st.session_state['clear_check']:
        st.session_state['input_check'] = ""
        st.session_state['clear_check'] = False

    ten_kiem_tra = st.text_input("Nhập họ và tên để tìm lịch:", placeholder="Tên học viên cần tìm...", key="input_check")
    
    if st.button("Tra Cứu Lịch"):
        st.session_state['search_name'] = ten_kiem_tra.strip()

# Xử lý kết quả tìm kiếm và hiển thị nút hủy trực tiếp
if 'search_name' in st.session_state and st.session_state['search_name']:
    name_to_find = st.session_state['search_name']
    tim_thay = False
    for ca, ds in data["dang_ky"].items():
        if name_to_find in ds:
            tim_thay = True
            st.info(f"Học viên **{name_to_find}** hiện đang đăng ký ở **{ca}**.")
            
            if st.button(f"❌ Xác nhận HỦY lịch của {name_to_find}", key="btn_huy_lich_action"):
                data["dang_ky"][ca].remove(name_to_find)
                luu_du_lieu(data)
                del st.session_state['search_name']
                st.session_state['clear_check'] = True
                st.success("Đã hủy lịch thành công! Ô nhập tên đã được làm sạch.")
                st.rerun()
            break
            
    if not tim_thay:
        st.warning(f"Không tìm thấy dữ liệu đăng ký cho tên **{name_to_find}** trong tuần này.")


# ================= CHỈ HIỆN SHEET KHI ĐỦ 10/10 HỌC VIÊN =================
if tong_so_hoc_vien == 10:
    st.divider()
    st.success("📊 **Bảng Sheet tổng hợp chính thức được mở:**")
    st.subheader("📋 Chi Tiết Danh Sách Từng Ca")
    
    sheet_col1, sheet_col2 = st.columns(2)

    with sheet_col1:
        st.markdown("#### **Ca 1 (8:00 - 9:45)**")
        ds_ca1 = data["dang_ky"]["Ca 1 (8:00 - 9:45)"]
        df_ca1 = pd.DataFrame({
            "STT": range(1, len(ds_ca1) + 1),
            "Họ và Tên": ds_ca1,
            "Trạng thái": ["Đã xác nhận"] * len(ds_ca1)
        })
        st.dataframe(df_ca1, use_container_width=True, hide_index=True)

    with sheet_col2:
        st.markdown("#### **Ca 2 (9:45 - 11:30)**")
        ds_ca2 = data["dang_ky"]["Ca 2 (9:45 - 11:30)"]
        df_ca2 = pd.DataFrame({
            "STT": range(1, len(ds_ca2) + 1),
            "Họ và Tên": ds_ca2,
            "Trạng thái": ["Đã xác nhận"] * len(ds_ca2)
        })
        st.dataframe(df_ca2, use_container_width=True, hide_index=True)

    # Nút tải xuống file tổng hợp
    danh_sach_tong_hop = []
    for ca, ds_hv in data["dang_ky"].items():
        for hv in ds_hv:
            danh_sach_tong_hop.append({
                "Họ và Tên": hv,
                "Ca Học": ca,
                "Ngày Học": ngay_thu_7
            })

    df_tong = pd.DataFrame(danh_sach_tong_hop)
    csv_data = df_tong.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Tải xuống file Excel/CSV tổng hợp cả lớp",
        data=csv_data,
        file_name=f"Danh_sach_thanh_nhac_{ngay_thu_7.replace('/', '_')}.csv",
        mime="text/csv"
    )