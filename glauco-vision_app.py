import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện
st.set_page_config(page_title="GlaucoVision AI", layout="centered")
st.title("👁️ GlaucoVision VF Analyzer")

# 2. Lấy API Key từ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # SỬA LỖI 404: Khai báo model kèm cấu hình API version v1
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        uploaded_file = st.file_uploader("Chọn hình ảnh báo cáo...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
            
            if st.button("Phân tích báo cáo"):
                with st.spinner('Đang phân tích dữ liệu...'):
                    try:
                        prompt ="""Bạn là một chuyên gia nhãn khoa. Hãy phân tích ảnh báo cáo Humphrey Field Analyzer này:
                        1. Trích xuất các chỉ số MD, PSD, VFI.
                        2. Nhận diện các tổn thương thị trường (nếu có).
                        3. Đưa ra nhận xét khách quan. 
                        Lưu ý: Kết quả này chỉ mang tính tham khảo, không thay thế chẩn đoán y khoa.
                        """
                        # ÉP HỆ THỐNG SỬ DỤNG VERSION v1 (Bỏ qua v1beta gây lỗi 404)
                        response = model.generate_content(
                            [prompt, image],
                            request_options={"api_version": "v1"}
                        )
                        
                        st.subheader("Kết quả phân tích:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Lỗi API: {e}")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
else:
    st.sidebar.warning("Vui lòng cấu hình GEMINI_API_KEY trong mục Secrets của Streamlit.")
    st.info("💡 Mẹo: Vào Settings -> Secrets trên Streamlit Cloud để dán Key.")
