import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="GlaucoVision AI", layout="centered")
st.title("👁️ GlaucoVision VF Analyzer")

# Ưu tiên lấy Key từ Secrets, nếu không có thì lấy từ Sidebar
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Sử dụng model flash để ổn định nhất
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        uploaded_file = st.file_uploader("Chọn hình ảnh báo cáo...", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
            
            if st.button("Phân tích báo cáo"):
                with st.spinner('Đang phân tích dữ liệu...'):
                    try:
                        prompt = "Bạn là bác sĩ nhãn khoa. Hãy trích xuất các chỉ số MD, PSD, VFI và tổn thương từ ảnh Humphrey này."
                        # Gọi API với cấu hình đơn giản nhất để tránh lỗi v1beta
                        response = model.generate_content([prompt, image])
                        st.subheader("Kết quả phân tích:")
                        st.write(response.text)
                    except Exception as e:
                        if "permission_denied" in str(e).lower():
                            st.error("Lỗi: API Key của bạn không có quyền sử dụng model này. Hãy kiểm tra lại tại Google AI Studio.")
                        else:
                            st.error(f"Lỗi: {e}")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
else:
    st.warning("Vui lòng nhập API Key ở thanh bên trái để bắt đầu.")
