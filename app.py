import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime, timedelta

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Hệ Thống Đăng Ký Lớp Thanh Nhạc",
    page_icon="🎵",
    layout="centered"
)

# CSS giao diện phong cách Âm Nhạc, Responsive & Modal thông báo trung tâm
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #fdf2f8 0%, #fff1f2 50%, #fae8ff 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1f2937;
    }

    @keyframes floatNotes {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-6px) rotate(5deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }
    
    .music-header {
        text-align: center;
        animation: floatNotes 4s ease-in-out infinite;
    }

    /* Tối ưu Input gọn gàng tuyệt đối */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #1f2937;
        border: 1.5px solid #f472b6;
        border-radius: 14px;
        padding: 12px 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 10px rgba(244, 114, 182, 0.08);
        font-size: 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #db2777;
        box-shadow: 0 0 0 4px rgba(219, 39, 119, 0.2);
    }

    /* Nút bấm phong cách giai điệu bùng nổ */
    div.stButton > button {
        border-radius: 14px;
        font-weight: 700;
        background: linear-gradient(135deg, #ec4899 0%, #be185d 100%);
        color: white;
        border: none;
        width: 100%;
        padding: 12px 20px;
        box-shadow: 0 8px 20px rgba(236, 72, 153, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        letter-spacing: 0.5px;
        cursor: pointer;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, #db2777 0%, #9d174d 100%);
        box-shadow: 0 12px 25px rgba(236, 72, 153, 0.6);
    }
    div.stButton > button:active {
        transform: translateY(1px);
    }

    /* Thẻ Card Ca học */
    .card {
        padding: 24px;
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
        border: 1.5px solid rgba(244, 114, 182, 0.4);
        box-shadow: 0 12px 30px -6px rgba(244, 114, 182, 0.15);
        margin-bottom: 18px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 18px 35px -6px rgba(236, 72, 153, 0.28);
        border-color: #ec4899;
    }
    .card h4 {
        color: #be185d;
        margin-bottom: 8px;
        font-weight: 800;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #f472b6 0%, #be185d 100%);
        border-radius: 12px;
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

# Tiêu đề
st.markdown("""
    <div class="music-header">
        <h1 style='color: #be185d; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 0;'>
            🎶 Đăng ký ca học thanh nhạc 🎤
        </h1>
        <p style='color: #6b7280; font-size: 17px; margin-top: 5px;'>
            🎵 <i>Luyện thanh thăng hoa cùng Ms Gemma</i> 🎵
        </p>
    </div>
""", unsafe_allow_html=True)

st.info(f"📅 **Lịch hòa ca Thứ 7 tuần này:** `{ngay_thu_7}` (Thời gian: **8:00 - 11:30**)")

tong_so_hoc_vien = sum(len(ds) for ds in data["dang_ky"].values())
st.markdown(f"🎧 **Tổng số giọng ca đã đăng ký tuần này:** `{tong_so_hoc_vien}/10 chỗ`")
st.progress(tong_so_hoc_vien / 10)

st.write("")

# Hiển thị 2 ca học
col1, col2 = st.columns(2)

with col1:
    siso_1 = len(data["dang_ky"]["Ca 1 (8:00 - 9:45)"])
    st.markdown(f"""
        <div class="card">
            <h4>🎼 Ca 1 (8:00 - 9:45)</h4>
            <p style="color: #4b5563; font-size: 14px;">Trạng thái: <b style="color: #be185d;">{siso_1}/5</b> giọng ca đã nhận</p>
            <hr style="border-color: #fbcfe8; margin: 8px 0 12px 0;">
    """, unsafe_allow_html=True)
    if siso_1 == 0:
        st.caption("Chưa có học viên đăng ký")
    else:
        for idx, hv in enumerate(data["dang_ky"]["Ca 1 (8:00 - 9:45)"], 1):
            st.write(f"**{idx}.** 🎤 {hv}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    siso_2 = len(data["dang_ky"]["Ca 2 (9:45 - 11:30)"])
    st.markdown(f"""
        <div class="card">
            <h4>🎹 Ca 2 (9:45 - 11:30)</h4>
            <p style="color: #4b5563; font-size: 14px;">Trạng thái: <b style="color: #be185d;">{siso_2}/5</b> giọng ca đã nhận</p>
            <hr style="border-color: #fbcfe8; margin: 8px 0 12px 0;">
    """, unsafe_allow_html=True)
    if siso_2 == 0:
        st.caption("Chưa có học viên đăng ký")
    else:
        for idx, hv in enumerate(data["dang_ky"]["Ca 2 (9:45 - 11:30)"], 1):
            st.write(f"**{idx}.** 🎶 {hv}")
    st.markdown("</div>", unsafe_allow_html=True)


# ================= PHẦN ĐĂNG KÝ LỊCH HỌC =================
st.divider()
st.subheader("✍️ Đăng Ký Luyện Thanh")

if tong_so_hoc_vien < 10:
    with st.container():
        if 'clear_input' in st.session_state and st.session_state['clear_input']:
            st.session_state['ten_input'] = ""
            st.session_state['clear_input'] = False

        # Thêm autocomplete="off" để tắt hoàn toàn lịch sử gợi ý của trình duyệt
        ten_hoc_vien = st.text_input("Nhập tên", key="ten_input", label_visibility="collapsed", autocomplete="off")
        
        cac_ca = list(data["dang_ky"].keys())
        if len(data["dang_ky"][cac_ca[0]]) >= 5:
            st.session_state["ca_dang_ky"] = cac_ca[1]

        ca_duoc_chon = st.selectbox(
            "Chọn ca học",
            options=cac_ca,
            format_func=lambda ca: f"{ca} - {len(data['dang_ky'][ca])}/5 học viên",
            key="ca_dang_ky"
        )

        if st.button("🎶 Xác Nhận Đăng Ký Ca Học"):
            ten_chuan_hoa = ten_hoc_vien.strip()
            if not ten_chuan_hoa:
                st.caption("Vui lòng nhập họ và tên của bạn trước khi đăng ký.")
            else:
                da_dang_ky = False
                ca_cu = ""
                for ca, ds in data["dang_ky"].items():
                    if ten_chuan_hoa in ds:
                        da_dang_ky = True
                        ca_cu = ca
                        break
                
                if da_dang_ky:
                    st.caption(f"Bạn {ten_chuan_hoa} đã đăng ký ca {ca_cu} rồi. Mỗi người chỉ được chọn một ca.")
                else:
                    if len(data["dang_ky"][ca_duoc_chon]) >= 5:
                        st.caption(f"Ca {ca_duoc_chon} đã đủ 5/5 học viên. Vui lòng chọn ca còn chỗ.")
                    else:
                        data["dang_ky"][ca_duoc_chon].append(ten_chuan_hoa)
                        luu_du_lieu(data)
                        st.session_state['clear_input'] = True
                        st.rerun()


# ================= PHẦN KIỂM TRA & HỦY LỊCH CÁ NHÂN =================
st.divider()
st.subheader("🔍 Tra Cứu Ca Học")
with st.container():
    if 'clear_check' in st.session_state and st.session_state['clear_check']:
        st.session_state['input_check'] = ""
        st.session_state['clear_check'] = False

    # Tắt autocomplete cho ô tra cứu
    ten_kiem_tra = st.text_input("Tra cứu", key="input_check", label_visibility="collapsed", autocomplete="off")
    
    if st.button("🎵 Tra Cứu Ca Học"):
        st.session_state['search_name'] = ten_kiem_tra.strip()

if 'search_name' in st.session_state and st.session_state['search_name']:
    name_to_find = st.session_state['search_name']
    tim_thay = False
    for ca, ds in data["dang_ky"].items():
        if name_to_find in ds:
            tim_thay = True
            st.markdown(f"Giọng ca **{name_to_find}** hiện đang luyện tập ở **{ca}**.")
            
            if st.button(f"❌ Xác nhận HỦY lịch của {name_to_find}", key="btn_huy_lich_action"):
                data["dang_ky"][ca].remove(name_to_find)
                luu_du_lieu(data)
                del st.session_state['search_name']
                st.session_state['clear_check'] = True
                st.rerun()
            break
            
    if not tim_thay:
        st.caption(f"Không tìm thấy dữ liệu đăng ký cho tên {name_to_find} trong tuần này.")


# ================= CHỈ HIỆN SHEET KHI ĐỦ 10/10 HỌC VIÊN =================
if tong_so_hoc_vien == 10:
    st.divider()
    st.success("📊 **Bảng Sheet tổng hợp hòa ca chính thức được mở:**")
    st.subheader("📋 Danh Sách Học Từng Ca")
    
    sheet_col1, sheet_col2 = st.columns(2)

    with sheet_col1:
        st.markdown("#### **🎼 Ca 1 (8:00 - 9:45)**")
        ds_ca1 = data["dang_ky"]["Ca 1 (8:00 - 9:45)"]
        df_ca1 = pd.DataFrame({
            "STT": range(1, len(ds_ca1) + 1),
            "Họ và Tên": ds_ca1,
            "Trạng thái": ["Đã xác nhận🎤"] * len(ds_ca1)
        })
        st.dataframe(df_ca1, use_container_width=True, hide_index=True)

    with sheet_col2:
        st.markdown("#### **🎹 Ca 2 (9:45 - 11:30)**")
        ds_ca2 = data["dang_ky"]["Ca 2 (9:45 - 11:30)"]
        df_ca2 = pd.DataFrame({
            "STT": range(1, len(ds_ca2) + 1),
            "Họ và Tên": ds_ca2,
            "Trạng thái": ["Đã xác nhận🎶"] * len(ds_ca2)
        })
        st.dataframe(df_ca2, use_container_width=True, hide_index=True)

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
        label="📥 Tải xuống file danh sách ca sĩ toàn lớp (CSV)",
        data=csv_data,
        file_name=f"Danh_sach_thanh_nhac_{ngay_thu_7.replace('/', '_')}.csv",
        mime="text/csv"
    )