import os
import streamlit as st
import google.generativeai as genai
from from google.generativeai import types

# 1. إعداد واجهة الموقع الأنيقة للمطور العقاري
st.set_page_config(page_title="مقتنص الفرص العقارية بالذكاء الاصطناعي", layout="centered")
st.title("🦅 نظام التنقيب الذكي عن الفرص العقارية (VIP)")
st.subheader("اكتشف الأراضي والعقارات بأقل من سعر السوق بـ 15% فما فوق")

# 2. خانة إدخال البيانات للعميل
st.write("---")
aqar_input = st.text_area(
    "أدخل بيانات العقار أو رابط المزاد (مثال: أرض في حي النرجس معروضة بـ 4500 ريال للمتر):",
    height=150,
    placeholder="انسخ بيانات المزاد أو العقار المعروض من منصة إنفاذ أو موقع عقار والصقها هنا..."
)

# 3. زر تشغيل الذكاء الاصطناعي ومسح السوق
if st.button("🚀 ابدأ تحليل الجدوى والتحقق من الأسعار الآن"):
    if not aqar_input:
        st.warning("الرجاء إدخال بيانات العقار أولاً.")
    else:
        with st.spinner("جاري فحص بورصة العقار والتحقق من الأسعار الحالية عبر جوجل..."):
            try:
                # تشغيل العقل الذكي الخاص بك بناءً على الكود الذي أرسلته
                client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
                
                # صياغة الأمر مدمجاً مع مدخلات المستخدم لضمان دقة التحليل العقاري السعودي
                prompt_text = f"""
                أنت مستشار عقاري سعودي ومحلل مالي محترف لفرص الاستثمار العقاري.
                استخدم أداة البحث المتاحة لديك للتحقق من أسعار الصفقات الحقيقية والحديثة في بورصة العقار السعودية لنفس الحي المذكور في المدخلات.
                ثم قارنها بالبيانات المدخلة بالأسفل لتحديد ما إذا كانت 'فرصة لقطة' (خصم 15% أو أكثر عن سعر السوق).
                
                صغ التقرير النهائي في جداول احترافية ومنظمة تحتوي على:
                1. اسم الفرصة وموقعها (الحي والمدينة).
                2. السعر الحالي المعروض (للمتر والإجمالي).
                3. السعر العادل المتوقع في السوق بناءً على أسعار البورصة الحالية.
                4. صافي الوفر المالي ونسبة الخصم (Profit Margin) التي سيحصل عليها المطور.
                5. التوصية الاستثمارية النهائية (لماذا يجب قنص هذه الأرض فوراً؟).
                
                البيانات المدخلة: {aqar_input}
                """
                
                contents = [types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])]
                tools = [types.Tool(googleSearch=types.GoogleSearch())]
                
                generate_content_config = types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
                    tools=tools,
                )
                
                # جلب النتيجة وعرضها مباشرة على الموقع
                response_placeholder = st.empty()
                full_response = ""
                
                for chunk in client.models.generate_content_stream(
                    model="gemini-3-flash-preview",
                    contents=contents,
                    config=generate_content_config,
                ):
                    if chunk.text:
                        full_response += chunk.text
                        response_placeholder.markdown(full_response)
                        
                st.success("🎯 تم الانتهاء من تحليل الفرصة بنجاح!")
                
            except Exception as e:
                st.error(f"حدث خطأ في الاتصال، تأكد من إعداد مفتاح GEMINI_API_KEY. تفاصيل الخطأ: {e}")
