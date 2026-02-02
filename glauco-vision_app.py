import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện
st.set_page_config(page_title="GlaucoVision AI", layout="centered")
st.title("👁️ AI Visual Field Analyzer - Dr. Le Hong Ha, MD")

# 2. Lấy API Key từ Secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Sửa model name: Bỏ 'models/', dùng model mới
        model = genai.GenerativeModel("gemini-2.5-flash")  # Hoặc "gemini-2.5-flash-latest" nếu cần bản mới nhất
        
        uploaded_file = st.file_uploader("Chọn hình ảnh báo cáo...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Ảnh đã tải lên', use_container_width=True)
            
            if st.button("Phân tích báo cáo"):
                with st.spinner('Đang phân tích dữ liệu...'):
                    try:
                        prompt = """Bạn là một chuyên gia nhãn khoa. Hãy phân tích ảnh báo cáo Humphrey Field Analyzer này một cách chi tiết và toàn diện:
                        1. Trích xuất các chỉ số chính: MD (Mean Deviation), PSD (Pattern Standard Deviation), VFI (Visual Field Index), GHT (Glaucoma Hemifield Test), và các thông số khác như độ tin cậy (FL, FN, FP).
                        2. Nhận diện các tổn thương thị trường (nếu có): Mô tả loại defect (ví dụ: arcuate scotoma, nasal step, hemianopia), vị trí (bán cầu trên/dưới, trung tâm/ngoại vi), và tính chất (cục bộ hay tổng thể).
                        3. Xác định có tổn thương do glaucoma hay không: Dựa trên tiêu chuẩn HPA/HAP2, xác định có phù hợp với tổn thương glaucoma (đáp ứng ít nhất 3 tiêu chí: GHT bất thường, PSD p<5%, cụm ≥3 điểm trên PD với p<5% và ít nhất 1 p<1%). Nếu có, phân loại mức độ (nhẹ, trung bình, nặng) và đánh giá tiến triển (nếu có chuỗi xét nghiệm: possible/likely progression theo GPA, thay đổi MD/VFI, deepening/expansion của defect).
                        4. Phân tích các khả năng tổn thương do nguyên nhân khác: Liệt kê và giải thích các nguyên nhân không phải glaucoma có thể gây defect tương tự (ví dụ: hemianopia do đột quỵ não, quadrantanopia do u não, altitudinal defect do thiếu máu thị giác, central scotoma do bệnh lý hoàng điểm hoặc dây thần kinh khác).
                        5. Đưa ra nhận xét khách quan tổng thể: Tóm tắt tình trạng, mức độ nghiêm trọng, và các yếu tố cần lưu ý (như artifact, learning effect nếu reliability kém).
                        6. Đề xuất tiếp theo: 
                           - Nên thực hiện gì ngay (theo dõi, điều trị khẩn cấp nếu nặng)?
                           - Cận lâm sàng bổ sung (ví dụ: OCT RNFL/GCC, đo nhãn áp, gonioscopy, MRI não nếu nghi nguyên nhân khác, thị trường lặp lại)?
                           - Phác đồ điều trị gợi ý (nếu glaucoma: thuốc nhỏ mắt như prostaglandin, beta-blocker; laser trabeculoplasty; phẫu thuật nếu tiến triển; nếu nguyên nhân khác: tham khảo chuyên khoa thần kinh, tim mạch, v.v.).
                        Lưu ý: Kết quả này chỉ mang tính tham khảo, không thay thế chẩn đoán y khoa. Khuyến nghị tham khảo Bác sĩ Chuyên gia nhãn khoa để đánh giá đầy đủ.
                        """
                        # Gọi generate_content với model mới
                        response = model.generate_content([prompt, image])
                        
                        st.subheader("Kết quả phân tích:")
                        st.markdown(response.text)
                        st.markdown("Visual Field Analyzer - Dr. Le Hong Ha, MD")
                    except Exception as e:
                        st.error(f"Lỗi API: {e}")
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")
else:
    st.sidebar.warning("Vui lòng cấu hình GEMINI_API_KEY trong mục Secrets.")
