import io
import json
import os
from datetime import date, timedelta
import pandas as pd
import streamlit as st

# 1. Cấu hình trang
st.set_page_config(
    page_title="Đăng Ký Ca Học Thanh Nhạc Ms GEMMA",
    page_icon="🎵",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111827 30%, #1f1631 100%);
        color: #f8fafc;
    }
    .music-header {
        text-align: center;
        background: linear-gradient(90deg, #f9a8d4, #c084fc, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.6rem;
        letter-spacing: 0.04em;
        margin-bottom: 0.2rem;
    }
    .music-subtitle {
        text-align: center;
        color: #d8b4fe;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1.2rem;
    }
    .date-banner {
        text-align: center;
        background: rgba(96, 165, 250, 0.1);
        border: 1px solid rgba(96, 165, 250, 0.4);
        border-radius: 14px;
        padding: 0.8rem 1rem;
        font-size: 1.08rem;
        color: #fef08a;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 24px rgba(59,130,246,0.12);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    [data-testid="stProgressBar"] > div {
        background: linear-gradient(90deg, #f472b6, #a78bfa, #60a5fa);
        border-radius: 999px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 45%, #f59e0b 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-size: 0.98rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.9rem 1.4rem !important;
        min-height: 46px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 10px 24px rgba(168, 85, 247, 0.38), inset 0 1px 0 rgba(255,255,255,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 14px 28px rgba(236, 72, 153, 0.42), inset 0 1px 0 rgba(255,255,255,0.25) !important;
        filter: saturate(1.15) !important;
    }
    .stButton > button:active {
        transform: translateY(0) scale(0.99) !important;
    }
    .stAlert, .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.18);
    }
    .stDataFrame {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stDateInput > div > div {
        background: rgba(15, 23, 42, 0.4);
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_FILE = "danh_sach_ca.json"

DEFAULT_SLOTS = {
    "Ca 1 (08:00 - 08:25)": None,
    "Ca 2 (08:25 - 08:50)": None,
    "Ca 3 (08:50 - 09:15)": None,
    "Ca 4 (09:15 - 09:40)": None,
    "Ca 5 (09:40 - 10:05)": None,
    "Ca 6 (10:05 - 10:30)": None,
    "Ca 7 (10:30 - 10:55)": None,
    "Ca 8 (10:55 - 11:20)": None,
    "Ca 9 (11:20 - 11:45)": None,
    "Ca 10 (11:45 - 12:10)": None,
}


def normalize_name(name):
  if not name:
    return ""
  return " ".join(str(name).split()).strip().casefold()


def get_this_saturday():
  """Tự động tính ngày Thứ 7 của tuần hiện tại"""
  today = date.today()
  days_ahead = (5 - today.weekday()) % 7
  return today + timedelta(days=days_ahead)


def load_all_data():
  if not os.path.exists(DATA_FILE):
    return {}
  try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      raw = json.load(f)

    # Tự động chuyển đổi cấu trúc dữ liệu cũ nếu có
    if raw and any(k.startswith("Ca ") for k in raw.keys()):
      sat_str = get_this_saturday().isoformat()
      migrated_slots = DEFAULT_SLOTS.copy()
      for ca, val in raw.items():
        if isinstance(val, dict):
          migrated_slots[ca] = val.get("hoc_vien")
        elif isinstance(val, str):
          migrated_slots[ca] = val
      return {sat_str: migrated_slots}

    return raw
  except Exception:
    return {}


def save_all_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


def get_slots_for_date(all_data, date_str):
  if date_str not in all_data:
    all_data[date_str] = DEFAULT_SLOTS.copy()
  return all_data[date_str]


# 2. TIÊU ĐỀ TRANG
st.markdown(
    '<h1 class="music-header">🎤 ĐĂNG KÝ CA HỌC THANH NHẠC</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="music-subtitle">🎼 Học thanh nhạc cùng Ms GEMMA 🎶</div>',
    unsafe_allow_html=True,
)

# 3. TỰ ĐỘNG TÍNH & HIỂN THỊ NGÀY THỨ 7 DƯỚI TIÊU ĐỀ
selected_date = get_this_saturday()
date_str = selected_date.isoformat()
date_formatted = selected_date.strftime("%d/%m/%Y")

st.markdown(
    f'<div class="date-banner">📅 Lịch học Thứ 7 tuần này: <b>{date_formatted}</b></div>',
    unsafe_allow_html=True,
)

# Tải dữ liệu riêng cho Thứ 7 tuần này
all_data = load_all_data()
current_slots = get_slots_for_date(all_data, date_str)
so_luong_da_dk = sum(1 for name in current_slots.values() if name)

# Tiến độ đăng ký
st.progress(so_luong_da_dk / 10)
st.caption(
    f"🎙️ Tiến độ ngày **{date_formatted}**: **{so_luong_da_dk}/10 ca** đã có"
    " học viên đăng ký"
)

st.divider()

# 4. KHI ĐÃ KÍN LỊCH HOẶC HIỂN THỊ TRẠNG THÁI CA
if so_luong_da_dk == 10:
  st.balloons()
  st.success(
      f"🎉 **TẤT CẢ 10 CA HỌC NGÀY {date_formatted} ĐÃ ĐƯỢC ĐĂNG KÝ KÍN LỊCH!**"
  )
  st.subheader(f"📊 Bảng Lịch Luyện Thanh Ngày {date_formatted}")

  df_data = []
  text_summary = (
      f"📋 LỊCH HỌC THANH NHẠC MS GEMMA ({date_formatted})\n"
      "-----------------------------------\n"
  )
  for idx, (ca_name, hoc_vien) in enumerate(current_slots.items(), start=1):
    df_data.append({"STT": idx, "Khung Giờ": ca_name, "Học Viên": hoc_vien})
    text_summary += f"{idx}. {ca_name}: {hoc_vien}\n"

  df = pd.DataFrame(df_data)
  st.dataframe(df, hide_index=True, use_container_width=True)

  st.subheader("💬 Sao chép tin nhắn để gửi nhóm Zalo:")
  st.code(text_summary, language="text")

  output = io.BytesIO()
  with pd.ExcelWriter(output, engine="openpyxl") as writer:
    df.to_excel(writer, index=False, sheet_name="Lich_Luyen_Thanh")
  excel_data = output.getvalue()

  st.download_button(
      label=f"📥 Tải file Excel lịch học ({date_formatted})",
      data=excel_data,
      file_name=f"Lich_Hoc_Thanh_Nhac_{date_formatted.replace('/', '_')}.xlsx",
      mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  )
else:
  st.subheader(f"📋 Tình Trạng Ca Học Ngày {date_formatted}")
  cols = st.columns(2)
  for i, (ca_name, hoc_vien) in enumerate(current_slots.items()):
    col = cols[i % 2]
    if hoc_vien:
      with col.container():
        st.markdown(
            f"<div style='background: rgba(239,68,68,0.10); border:1px solid rgba(248,113,113,0.45); border-radius: 12px; padding: 0.9rem 1rem; margin-bottom: 0.75rem;'>"
            f"<div style='font-size:0.8rem; color:#fca5a5; text-transform: uppercase; letter-spacing: 0.08em;'>Đã đăng ký</div>"
            f"<div style='font-size:1.05rem; font-weight:700; margin-top: 0.25rem;'>{ca_name}</div>"
            f"<div style='color:#fecaca; margin-top: 0.2rem;'>👤 {hoc_vien}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
      with col.container():
        st.markdown(
            f"<div style='background: rgba(34,197,94,0.10); border:1px solid rgba(74,222,128,0.45); border-radius: 12px; padding: 0.9rem 1rem; margin-bottom: 0.75rem;'>"
            f"<div style='font-size:0.8rem; color:#86efac; text-transform: uppercase; letter-spacing: 0.08em;'>Còn trống</div>"
            f"<div style='font-size:1.05rem; font-weight:700; margin-top: 0.25rem;'>{ca_name}</div>"
            f"<div style='color:#dcfce7; margin-top: 0.2rem;'>🎵 Chưa có người đăng ký</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

  st.divider()

  # 5. FORM ĐĂNG KÝ CA HỌC
  st.subheader("✍️ Đăng Ký Khung Giờ")
  available_slots = [
      ca for ca, hoc_vien in current_slots.items() if not hoc_vien
  ]

  with st.form("form_dang_ky", clear_on_submit=True):
    ho_ten = st.text_input("Họ và tên học viên:", placeholder="Nhập họ tên đầy đủ")
    ca_chon = st.selectbox("Chọn khung giờ bạn muốn học:", available_slots)
    submit_btn = st.form_submit_button("🎶 Xác Nhận Đăng Ký Ca Học")

  if submit_btn:
    ho_ten_clean = ho_ten.strip()
    if not ho_ten_clean:
      st.warning("⚠️ Vui lòng nhập họ và tên của bạn!")
    else:
      all_data = load_all_data()
      slots_now = get_slots_for_date(all_data, date_str)

      if slots_now.get(ca_chon) is not None:
        st.error(
            f"❌ **{ca_chon}** đã vừa được đăng ký bởi **{slots_now[ca_chon]}**!"
        )
      else:
        all_data[date_str][ca_chon] = ho_ten_clean
        save_all_data(all_data)
        st.success(
            f"🎉 **Đăng ký thành công!**\n\n• Học viên: **{ho_ten_clean}**\n• Ca"
            f" học: **{ca_chon}**\n• Ngày: **{date_formatted}**"
        )
        st.rerun()

# 6. XEM VÀ HỦY ĐĂNG KÝ CÁ NHÂN
st.divider()
st.subheader("📜 Xem & Hủy Đăng Ký Cá Nhân")

with st.form("form_lich_su", clear_on_submit=False):
  ho_ten_history = st.text_input(
      f"Nhập họ và tên để kiểm tra ca đã đăng ký ngày {date_formatted}:"
  )
  xem_lich_su = st.form_submit_button("🔍 Kiểm tra ca đã đăng ký")

if xem_lich_su or st.session_state.get("check_history"):
  st.session_state["check_history"] = True
  ho_ten_clean = ho_ten_history.strip().casefold()
  if ho_ten_clean:
    user_bookings = [
        ca
        for ca, name in current_slots.items()
        if name and name.strip().casefold() == ho_ten_clean
    ]
    if not user_bookings:
      st.info(
          f"Không tìm thấy ca đăng ký nào của **{ho_ten_history}** trong ngày"
          f" {date_formatted}."
      )
    else:
      st.success(
          f"**{ho_ten_history}** đã đăng ký {len(user_bookings)} ca ngày"
          f" {date_formatted}:"
      )
      for ca in user_bookings:
        st.markdown(f"- **{ca}**")

      ca_xoa = st.selectbox("Chọn ca muốn hủy:", user_bookings, key="ca_xoa_sel")
      if st.button("🗑️ Hủy đăng ký ca này"):
        all_data = load_all_data()
        if date_str in all_data and ca_xoa in all_data[date_str]:
          owner_name = all_data[date_str].get(ca_xoa)
          if normalize_name(owner_name) != normalize_name(ho_ten_history):
            st.warning(
                "⚠️ Chỉ có người đã nhập tên của mình mới được xóa ca của chính mình."
            )
          else:
            all_data[date_str][ca_xoa] = None
            save_all_data(all_data)
            st.success(
                f"✅ Đã hủy thành công **{ca_xoa}** ngày {date_formatted}!"
            )
            st.session_state["check_history"] = False
            st.rerun()