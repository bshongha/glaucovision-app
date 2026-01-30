import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="GlaucoVision AI", layout="centered")
st.title("👁️ GlaucoVision VF Analyzer")

# Phần cấu hình API Key bí mật
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Cấu hình an toàn để model không từ chối phân tích ảnh y tế
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)

    uploaded_file = st.file_uploader("Tải lên ảnh Humphrey report...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
        
        if st.button("Bắt đầu phân tích"):
            with st.spinner('Đang đọc dữ liệu...'):
                prompt = "Phân tích báo cáo thị trường Humphrey này. Trích xuất MD, PSD, VFI và đưa ra nhận xét chuyên môn. Lưu ý: Đây là thông tin tham khảo."
                response = model.generate_content([prompt, image])
                st.subheader("Kết quả:")
                st.write(response.text)
else:
    st.info("Vui lòng cung cấp API Key để tiếp tục.")
