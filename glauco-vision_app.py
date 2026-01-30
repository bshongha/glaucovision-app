import streamlit as st
import google.generativeai as genai
from PIL import Image

# Cấu hình trang web
st.set_page_config(page_title="GlaucoVision AI", layout="centered")
st.title("👁️ GlaucoVision VF Analyzer")
st.write("Tải lên ảnh báo cáo Humphrey để phân tích.")

# Nhập API Key (Khi chạy thực tế sẽ dùng Secrets để bảo mật)
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
    genai.configure(api_key=api_key)
        # Sử dụng đúng tên model phiên bản ổn định nhất hiện tại
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 

        uploaded_file = st.file_uploader("Chọn hình ảnh báo cáo...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
        
        if st.button("Phân tích báo cáo"):
                with st.spinner('Đang phân tích dữ liệu...'):
                    try:
                prompt = """
                Bạn là một chuyên gia nhãn khoa. Hãy phân tích ảnh báo cáo Humphrey Field Analyzer này.
                1. Trích xuất các chỉ số MD, PSD, VFI.
                2. Nhận diện các tổn thương thị trường (nếu có).
                3. Đưa ra nhận xét khách quan. 
                Lưu ý: Kết quả này chỉ mang tính tham khảo, không thay thế chẩn đoán y khoa.
                """
            # Thực hiện gọi API
        response = model.generate_content([prompt, image])
                        st.subheader("Kết quả phân tích:")
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"Lỗi khi gọi Gemini API: {e}")
    except Exception as e:
        st.error(f"Lỗi cấu hình: {e}")
