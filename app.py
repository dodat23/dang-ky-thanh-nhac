from datetime import date, timedelta
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình trang
st.set_page_config(
    page_title="Lịch Học Thanh Nhạc - Ms GEMMA",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Tùy chỉnh CSS Giao diện Tone Sáng, Animation & Tắt autocomplete
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Gradient Background Tone Sáng */
    .stApp {
        background: linear-gradient(135deg, #FAF8FF 0%, #FFF0F5 50%, #F0F7FF 100%);
        color: #2D3748;
    }

    /* Keyframes Animations */
    @keyframes float {
        0% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(2deg); }
        100% { transform: translateY(0px) rotate(0deg); }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 4px 15px rgba(233, 64, 87, 0.2); }
        50% { box-shadow: 0 8px 25px rgba(233, 64, 87, 0.4); }
        100% { box-shadow: 0 4px 15px rgba(233, 64, 87, 0.2); }
    }

    /* Animation mượt cho Pop-up Box (st.dialog) */
    @keyframes modalPop {
        0% {
            opacity: 0;
            transform: scale(0.82) translateY(20px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }

    @keyframes backdropFade {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Tùy chỉnh Cửa sổ Dialog / Modal */
    div[role="dialog"], div[data-testid="stDialog"], div[data-testid="stModal"] {
        animation: modalPop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) forwards !important;
        border-radius: 24px !important;
        border: 1px solid rgba(233, 64, 87, 0.25) !important;
        box-shadow: 0 20px 50px rgba(142, 36, 170, 0.2) !important;
        background: #FFFFFF !important;
    }

    div[data-testid="stDialog"] > div:first-child,
    div[role="dialog"] > div:first-child {
        backdrop-filter: blur(8px) !important;
        background-color: rgba(0, 0, 0, 0.35) !important;
        animation: backdropFade 0.3s ease-out forwards !important;
    }

    /* Header Container */
    .header-container {
        text-align: center;
        padding: 20px 10px 10px 10px;
        animation: fadeIn 0.8s ease-out;
    }

    .music-icon {
        font-size: 3.2rem;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
        margin-bottom: 5px;
    }

    .music-header {
        background: linear-gradient(135deg, #E91E63 0%, #9C27B0 50%, #673AB7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        letter-spacing: -0.5px;
        margin: 0;
    }

    .music-subtitle {
        color: #718096;
        font-weight: 500;
        font-size: 1.05rem;
        margin-top: 6px;
    }

    /* Date Banner Card */
    .date-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(233, 64, 87, 0.2);
        border-radius: 16px;
        padding: 14px 20px;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 600;
        color: #C2185B;
        box-shadow: 0 8px 20px rgba(233, 64, 87, 0.08);
        margin: 15px 0 25px 0;
        animation: fadeIn 1s ease-out;
    }

    /* Ca Học Cards */
    .ca-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.04);
        border: 1px solid #F1F5F9;
        transition: all 0.3s ease;
        margin-bottom: 15px;
    }

    .ca-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 15px 30px rgba(156, 39, 176, 0.1);
        border-color: #E1BEE7;
    }

    /* Student Badge Chip */
    .student-chip {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, #F3E5F5 0%, #FCE4EC 100%);
        color: #8E24AA;
        font-weight: 600;
        padding: 8px 14px;
        border-radius: 12px;
        margin: 4px;
        font-size: 0.95rem;
        box-shadow: 0 2px 6px rgba(142, 36, 170, 0.08);
        animation: fadeIn 0.4s ease-in-out;
    }

    /* Custom Form Styling */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.05);
        border: 1px solid #F3E8FF;
    }

    /* Custom Button */
    .stButton>button {
        background: linear-gradient(135deg, #E91E63 0%, #9C27B0 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 12px 24px !important;
        font-size: 1.05rem !important;
        width: 100%;
        transition: all 0.3s ease !important;
        animation: pulseGlow 3s infinite;
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 10px 25px rgba(233, 64, 87, 0.4) !important;
    }

    /* Custom Input Fields */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        background-color: #FAFAFA !important;
        color: #2D3748 !important;
    }

    .stTextInput input:focus {
        border-color: #AB47BC !important;
        box-shadow: 0 0 0 3px rgba(171, 71, 188, 0.15) !important;
    }

    @media (max-width: 768px) {
        .music-header { font-size: 1.7rem; }
        .music-subtitle { font-size: 0.95rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 3. Khai báo Hằng số
CA_1 = "Ca 1 (08:00 - 09:45)"
CA_2 = "Ca 2 (09:45 - 11:30)"
MAX_GUEST_PER_CA = 5


def get_current_week_saturday():
  today = date.today()
  saturday = today + timedelta(days=(5 - today.weekday()))
  return saturday


# 4. Kết nối Google Sheets & Quản lý Cache
conn = st.connection("gsheets", type=GSheetsConnection)


@st.cache_data(ttl=10)
def load_data():
  try:
    df = conn.read(ttl=10)
    if df is None:
      return pd.DataFrame(columns=["ngay", "ca", "hoc_vien"])
    return df
  except Exception:
    return pd.DataFrame(columns=["ngay", "ca", "hoc_vien"])


def save_booking(date_str, ca, name):
  df = load_data()
  new_row = pd.DataFrame([{"ngay": date_str, "ca": ca, "hoc_vien": name}])
  df = pd.concat([df, new_row], ignore_index=True)
  conn.update(data=df)
  st.cache_data.clear()


def delete_booking(date_str, ca, name):
  df = load_data()
  # Lọc bỏ dòng cần xóa và reset lại index hoàn toàn
  df = df[
      ~(
          (df["ngay"].astype(str) == str(date_str))
          & (df["ca"].astype(str) == str(ca))
          & (df["hoc_vien"].astype(str).str.casefold() == str(name).casefold())
      )
  ].reset_index(drop=True)
  conn.update(data=df)
  st.cache_data.clear()


# 5. Hàm hiển thị Cửa sổ Thông báo Pop-up Modal (st.dialog)
@st.dialog("🔔 THÔNG BÁO")
def show_popup_dialog(title, message, icon="✨"):
  st.markdown(
      f"<div style='text-align: center; font-size: 3.5rem;"
      f" margin-bottom: 5px;'>{icon}</div>",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"<h3 style='text-align: center; color: #8E24AA; margin-bottom:"
      f" 15px;'>{title}</h3>",
      unsafe_allow_html=True,
  )
  st.markdown(
      f"<div style='text-align: center; font-size: 1.05rem; color: #4A5568;"
      f" line-height: 1.6;'>{message}</div>",
      unsafe_allow_html=True,
  )
  st.write("")
  if st.button("Đóng / Xác nhận", use_container_width=True):
    st.session_state["popup_trigger"] = None
    st.rerun()


if (
    "popup_trigger" in st.session_state
    and st.session_state["popup_trigger"] is not None
):
  p = st.session_state["popup_trigger"]
  show_popup_dialog(p["title"], p["message"], p["icon"])

# 6. Giao diện Header
st.markdown(
    """
    <div class="header-container">
        <div class="music-icon">🎼</div>
        <h1 class="music-header">ĐĂNG KÝ HỌC THANH NHẠC</h1>
        <div class="music-subtitle">✨ Luyện giọng thăng hoa cùng Ms GEMMA ✨</div>
    </div>
    """,
    unsafe_allow_html=True,
)

selected_date = get_current_week_saturday()
date_str = selected_date.isoformat()
date_formatted = selected_date.strftime("%d/%m/%Y")

st.markdown(
    f"""
    <div class="date-card">
        📅 Lịch Học Thứ 7 Tuần Này: <span>{date_formatted}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# 7. Đọc dữ liệu từ Google Sheets
df_all = load_data()
df_today = (
    df_all[df_all["ngay"].astype(str) == str(date_str)]
    if not df_all.empty and "ngay" in df_all.columns
    else pd.DataFrame(columns=["ngay", "ca", "hoc_vien"])
)

list_ca1 = (
    df_today[df_today["ca"] == CA_1]["hoc_vien"].tolist()
    if not df_today.empty and "ca" in df_today.columns
    else []
)
list_ca2 = (
    df_today[df_today["ca"] == CA_2]["hoc_vien"].tolist()
    if not df_today.empty and "ca" in df_today.columns
    else []
)

total_booked = len(list_ca1) + len(list_ca2)

# Thanh tiến trình tổng
st.markdown("##### 🎙️ Tổng số học viên đã đăng ký tuần này")
st.progress(total_booked / 10)
st.caption(f"Trạng thái: **{total_booked}/10** chỗ đã có chủ")
st.write("")

# 8. Hiển thị 2 Ca Học trong Thẻ
col1, col2 = st.columns(2)

with col1:
  st.markdown(
      f"""
        <div class="ca-card">
            <h4 style="color:#C2185B; margin:0 0 8px 0;">🌅 Ca 1 (08:00 - 09:45)</h4>
            <div style="font-weight:600; color:#718096; margin-bottom:12px;">
                Chỗ đã đặt: <b style="color:#8E24AA;">{len(list_ca1)}/{MAX_GUEST_PER_CA}</b>
            </div>
        """,
      unsafe_allow_html=True,
  )
  if list_ca1:
    chips_html = "".join([
        f'<div class="student-chip">👤 {name}</div>' for name in list_ca1
    ])
    st.markdown(chips_html, unsafe_allow_html=True)
  else:
    st.info("Chưa có học viên đăng ký")
  st.markdown("</div>", unsafe_allow_html=True)

with col2:
  st.markdown(
      f"""
        <div class="ca-card">
            <h4 style="color:#C2185B; margin:0 0 8px 0;">🌤️ Ca 2 (09:45 - 11:30)</h4>
            <div style="font-weight:600; color:#718096; margin-bottom:12px;">
                Chỗ đã đặt: <b style="color:#8E24AA;">{len(list_ca2)}/{MAX_GUEST_PER_CA}</b>
            </div>
        """,
      unsafe_allow_html=True,
  )
  if list_ca2:
    chips_html = "".join([
        f'<div class="student-chip">👤 {name}</div>' for name in list_ca2
    ])
    st.markdown(chips_html, unsafe_allow_html=True)
  else:
    st.info("Chưa có học viên đăng ký")
  st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# 9. Form Đăng Ký HOẶC Hiển Thị Bảng Tổng Hợp Khi Đã Kín Chỗ
if total_booked >= 10:
  st.balloons()
  st.success(
      f"🎉 **Tất cả các ca học ngày {date_formatted} đã kín chỗ! Cảm ơn các"
      " bạn.**"
  )

  ca1_str = (
      "<br>".join([f"&nbsp;&nbsp;<b>{i+1}.</b> {n}" for i, n in enumerate(list_ca1)])
      if list_ca1
      else "<i>Trống</i>"
  )
  ca2_str = (
      "<br>".join([f"&nbsp;&nbsp;<b>{i+1}.</b> {n}" for i, n in enumerate(list_ca2)])
      if list_ca2
      else "<i>Trống</i>"
  )

  st.markdown(
      f"""
    <div style="background: #FFFFFF; border-radius: 20px; padding: 22px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1.5px solid #E1BEE7; margin-top: 15px;">
        <h4 style="color: #8E24AA; margin-top: 0; text-align: center; border-bottom: 2px solid #F3E5F5; padding-bottom: 10px;">
            📜 DANH SÁCH TỔNG HỢP 10 HỌC VIÊN TUẦN NÀY
        </h4>
        <div style="margin-top: 15px;">
            <p style="font-weight: 700; color: #C2185B; margin-bottom: 6px; font-size: 1.05rem;">🌅 Ca 1 (08:00 - 09:45):</p>
            <div style="color: #2D3748; line-height: 1.7; font-size: 1rem;">{ca1_str}</div>
        </div>
        <div style="margin-top: 20px;">
            <p style="font-weight: 700; color: #C2185B; margin-bottom: 6px; font-size: 1.05rem;">🌤️ Ca 2 (09:45 - 11:30):</p>
            <div style="color: #2D3748; line-height: 1.7; font-size: 1rem;">{ca2_str}</div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )
else:
  st.markdown("### ✍️ Đăng Ký Lịch Học")
  available_cas = []
  if len(list_ca1) < MAX_GUEST_PER_CA:
    available_cas.append(f"{CA_1} (Còn {MAX_GUEST_PER_CA - len(list_ca1)} chỗ)")
  if len(list_ca2) < MAX_GUEST_PER_CA:
    available_cas.append(f"{CA_2} (Còn {MAX_GUEST_PER_CA - len(list_ca2)} chỗ)")

  with st.form("form_dang_ky", clear_on_submit=True):
    ho_ten = st.text_input(
        "Họ và tên học viên:",
        placeholder="Nhập tên của bạn...",
        autocomplete="off",
    )
    ca_chon_raw = st.selectbox("Chọn ca học mong muốn:", available_cas)
    submit_btn = st.form_submit_button("🎶 XÁC NHẬN ĐĂNG KÝ")

  if submit_btn:
    ho_ten_clean = ho_ten.strip()
    if not ho_ten_clean:
      st.session_state["popup_trigger"] = {
          "title": "Chưa Nhập Tên",
          "message": "Vui lòng điền họ và tên học viên trước khi bấm đăng ký!",
          "icon": "⚠️",
      }
      st.rerun()
    else:
      all_registered_names = [n.casefold() for n in (list_ca1 + list_ca2)]
      if ho_ten_clean.casefold() in all_registered_names:
        st.session_state["popup_trigger"] = {
            "title": "Đã Đăng Ký Trước Đó",
            "message": (
                f"Học viên <b>{ho_ten_clean}</b> đã có tên trong danh sách đăng"
                f" ký ngày {date_formatted}.<br><br><i>Mỗi học viên chỉ đăng ký"
                " 1 ca/tuần.</i>"
            ),
            "icon": "❌",
        }
        st.rerun()
      else:
        selected_ca = CA_1 if CA_1 in ca_chon_raw else CA_2
        save_booking(date_str, selected_ca, ho_ten_clean)
        st.balloons()
        st.session_state["popup_trigger"] = {
            "title": "Đăng Ký Thành Công!",
            "message": (
                f"Chúc mừng học viên <b>{ho_ten_clean}</b>!<br><br>• Lịch"
                f" học: <b>Thứ 7 ({date_formatted})</b><br>• Ca học:"
                f" <b>{selected_ca}</b>"
            ),
            "icon": "🎉",
        }
        st.rerun()

# 10. Form Kiểm Tra & Hủy Ca
st.write("")
st.markdown("---")
st.markdown("### 🔍 Kiểm Tra & Hủy Lịch Đã Đăng Ký")

with st.form("form_lich_su", clear_on_submit=True):
  ho_ten_history = st.text_input(
      "Nhập họ và tên để kiểm tra:",
      placeholder="Tên học viên cần tìm...",
      autocomplete="off",
  )
  xem_lich_su = st.form_submit_button("🔎 Tra Cứu Lịch")

if xem_lich_su:
  search_clean = ho_ten_history.strip()
  if not search_clean:
    st.session_state["popup_trigger"] = {
        "title": "Thông Báo",
        "message": "Vui lòng nhập tên học viên để tra cứu!",
        "icon": "⚠️",
    }
    st.rerun()
  else:
    st.session_state["searched_name"] = search_clean

# Hiển thị kết quả tra cứu nếu có
searched_name = st.session_state.get("searched_name", "")
if searched_name:
  user_bookings = df_today[
      df_today["hoc_vien"].str.casefold() == searched_name.casefold()
  ]
  if user_bookings.empty:
    st.session_state["popup_trigger"] = {
        "title": "Không Tìm Thấy",
        "message": (
            f"Không tìm thấy thông tin đăng ký nào của <b>{searched_name}</b>"
            f" trong ngày {date_formatted}."
        ),
        "icon": "🔍",
    }
    st.session_state["searched_name"] = ""
    st.rerun()
  else:
    st.info(f"📋 Kết quả tra cứu cho học viên: **{searched_name}**")
    for _, row in user_bookings.iterrows():
      col_info, col_del = st.columns([3, 1])
      with col_info:
        st.write(f"📌 **{row['ca']}**")
      with col_del:
        if st.button("🗑️ Hủy ca", key=f"del_{row['ca']}_{row['hoc_vien']}"):
          delete_booking(date_str, row["ca"], row["hoc_vien"])
          st.session_state["searched_name"] = ""
          st.session_state["popup_trigger"] = {
              "title": "Đã Hủy Đăng Ký",
              "message": (
                  f"Đã hủy thành công ca học ngày {date_formatted} của"
                  f" học viên <b>{row['hoc_vien']}</b>."
              ),
              "icon": "✅",
          }
          st.rerun()