import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình trang web trước
st.set_page_config(page_title="GlaucoVision AI", layout="centered")
st.title("👁️ GlaucoVision VF Analyzer")

# 2. Kiểm tra API Key từ Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        # PHẢI CẤU HÌNH TRƯỚC KHI KHAI BÁO MODEL
        genai.configure(api_key=api_key)
        
        # Khai báo model với cấu hình v1 để tránh lỗi 404
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        uploaded_file = st.file_uploader("Chọn hình ảnh báo cáo...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
            
            if st.button("Phân tích báo cáo"):
                with st.spinner('Đang phân tích dữ liệu...'):
                    try:
                        prompt = "Bạn là chuyên gia nhãn khoa. Phân tích chỉ số MD, PSD, VFI và tổn thương từ ảnh Humphrey này."
                        # Thêm request_options để ép sử dụng API bản ổn định
                        response = model.generate_content(
                            [prompt, image],
                            request_options={"api_version": "v1"}
                        )
                        st.subheader("Kết quả phân tích:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Lỗi khi gọi Gemini API: {e}")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
else:
    st.warning("Vui lòng cấu hình API Key ở thanh bên trái.")
