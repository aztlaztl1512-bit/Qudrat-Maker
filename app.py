import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import io

# إعدادات واجهة الموقع
st.set_page_config(page_title="مصمم نماذج القدرات", layout="centered")

st.markdown("<h1 style='text-align: center;'>📝 صانع اختبارات القدرات</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>ثانوية الأمير عبدالمجيد</p>", unsafe_allow_html=True)

# دالة معالجة النص العربي
def fix_ar(text):
    if not text: return ""
    return get_display(arabic_reshaper.reshape(text))

# دالة رسم كرت السؤال
def create_card(q_text, opts, ans):
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # تحميل الخط (تأكد من وجود الملف بنفس الاسم في المستودع)
    font_path = "Tajawal-Bold.ttf" 
    try:
        f_q = ImageFont.truetype(font_path, 35)
        f_opt = ImageFont.truetype(font_path, 30)
    except:
        # خط بديل في حال لم يجد الخط
        f_q = ImageFont.load_default()
        f_opt = ImageFont.load_default()

    # رسم الأشكال الهندسية (نفس تصميمك)
    draw.rounded_rectangle([1020, 150, 1150, 520], radius=25, fill=(205, 126, 110)) 
    draw.rounded_rectangle([100, 150, 1000, 480], radius=20, fill=(245, 245, 245))  
    draw.rounded_rectangle([100, 480, 1000, 530], radius=5, fill=(255, 82, 82))     

    # كتابة النصوص
    draw.text((970, 190), fix_ar(q_text), fill=(50, 50, 100), font=f_q, anchor="rm")
    labels = ['أ', 'ب', 'ج', 'د']
    coords = [(750, 300), (350, 300), (750, 380), (350, 380)]
    for i, (opt, pos) in enumerate(zip(opts, coords)):
        draw.text(pos, fix_ar(f"{labels[i]}) {opt}"), fill=(0,0,0), font=f_opt, anchor="rm")
    
    draw.text((550, 505), fix_ar(f"الإجابة: {ans}"), fill=(255,255,255), font=f_q, anchor="mm")
    return img

# --- إدارة حالة الأسئلة (ميزة المربعات المتعددة وزر +) ---
if 'questions_list' not in st.session_state:
    st.session_state.questions_list = [{'q': '', 'a': '', 'b': '', 'c': '', 'd': '', 'ans': 'أ'}]

# عرض مربعات الأسئلة
for i, item in enumerate(st.session_state.questions_list):
    with st.container(border=True):
        st.subheader(f"السؤال رقم {i+1}")
        st.session_state.questions_list[i]['q'] = st.text_area("نص السؤال", key=f"q{i}", height=70)
        c1, c2 = st.columns(2)
        st.session_state.questions_list[i]['a'] = c1.text_input("خيار أ", key=f"a{i}")
        st.session_state.questions_list[i]['b'] = c2.text_input("خيار ب", key=f"b{i}")
        st.session_state.questions_list[i]['c'] = c1.text_input("خيار ج", key=f"c{i}")
        st.session_state.questions_list[i]['d'] = c2.text_input("خيار د", key=f"d{i}")
        st.session_state.questions_list[i]['ans'] = st.selectbox("الإجابة الصحيحة", ['أ', 'ب', 'ج', 'د'], key=f"ans{i}")

# زر الإضافة +
if st.button("➕ إضافة سؤال جديد"):
    st.session_state.questions_list.append({'q': '', 'a': '', 'b': '', 'c': '', 'd': '', 'ans': 'أ'})
    st.rerun()

# --- زر الحفظ PDF ---
st.divider()
if st.button("📥 حفظ كافة الأسئلة في ملف PDF واحد", use_container_width=True):
    images = []
    for q in st.session_state.questions_list:
        if q['q'].strip() != "":
            img_card = create_card(q['q'], [q['a'], q['b'], q['c'], q['d']], q['ans'])
            images.append(img_card)
    
    if images:
        pdf_buffer = io.BytesIO()
        # تحويل الصور إلى PDF مجمع
        images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=images[1:])
        st.download_button("تحميل ملف PDF الآن", data=pdf_buffer.getvalue(), file_name="قدرات.pdf", mime="application/pdf")
    else:
        st.warning("يرجى كتابة سؤال واحد على الأقل.")
