import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans
from PIL import Image
import easyocr
import time
import base64

# Setup page
st.set_page_config(page_title="Design Feedback Pro", page_icon="🎨", layout="centered")

# Light/Dark Mode Toggle
theme = st.selectbox("Choose Theme", ["Light", "Dark"])

if theme == "Dark":
    bg_color = "#121212"
    text_color = "white"
    card_color = "#1E1E1E"
else:
    bg_color = "#FFFFFF"
    text_color = "black"
    card_color = "#F5F5F5"

# Start background div
st.markdown(
    f"""
    <div style="background-color: {bg_color}; color: {text_color}; padding: 20px; border-radius: 10px;">
    """,
    unsafe_allow_html=True,
)

st.title("🎨 AI-Powered Design Feedback Pro")
st.write("Upload your design, and get instant, professional feedback!")

uploaded_file = st.file_uploader("Upload your design image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show uploaded image
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    st.image(image, caption="Uploaded Design", use_column_width=True)

    progress = st.progress(0)

    # Prepare feedback storage
    feedback_text = ""
    suggestions = []

    with st.spinner("Analyzing colors..."):
        time.sleep(1)
        img_small = cv2.resize(img_array, (64, 64))

        if len(img_small.shape) == 2:
            img_small = cv2.cvtColor(img_small, cv2.COLOR_GRAY2RGB)

        img_small = img_small.reshape((-1, 3))
        kmeans = KMeans(n_clusters=5, random_state=42).fit(img_small)
        colors = np.round(kmeans.cluster_centers_).astype(int)

        light_colors = sum(1 for c in colors if np.mean(c) > 180)
        dark_colors = sum(1 for c in colors if np.mean(c) < 75)
        progress.progress(30)

    with st.spinner("Checking layout..."):
        time.sleep(1)
        height, width = img_array.shape[0], img_array.shape[1]
        ratio = round(width / height, 2)
        progress.progress(60)

    with st.spinner("Detecting typography..."):
        time.sleep(1)
        reader = easyocr.Reader(['en'], gpu=False)
        results = reader.readtext(np.array(image))
        num_text_blocks = len(results)
        progress.progress(100)

    st.success("✅ Analysis Complete!")

    # Color Analysis
    st.subheader("🎨 Color Analysis")
    cols = st.columns(5)
    for idx, color in enumerate(colors):
        with cols[idx]:
            hex_color = '#%02x%02x%02x' % tuple(color)
            st.color_picker("", hex_color, label_visibility="collapsed")

    # Color scoring
    if light_colors > 3:
        st.warning("Too light: Add more contrast.")
        color_score = 6 + min(3, (light_colors - 3) * 2)
        suggestions.append(
            "The design appears overly bright with many light tones. "
            "Consider introducing deeper shades or bold accents to create stronger contrast, "
            "which improves readability and gives your design a more professional finish."
        )
    elif dark_colors > 3:
        st.warning("Too dark: Brighten a bit.")
        color_score = 6 + min(3, (dark_colors - 3) * 2)
        suggestions.append(
            "The overall tone seems very dark, which might make content harder to see. "
            "Try adding lighter highlights or vibrant elements to ensure better visual hierarchy, "
            "making important parts stand out more clearly."
        )
    else:
        st.success("Good color balance!")
        color_score = 10

    st.write(f"Color Score: {color_score}")

    # Layout Analysis
    st.subheader("📐 Layout Analysis")
    st.write(f"Aspect Ratio: {width} x {height} ({ratio}:1)")

    if ratio > 2 or ratio < 0.5:
        st.warning("Unusual aspect ratio. Might not fit standard screens.")
        layout_score = max(5, 10 - abs(ratio - 1) * 2)
        suggestions.append(
            "Your design uses an uncommon aspect ratio, which may cause issues on standard devices like mobiles or laptops. "
            "Consider adjusting it to a more common ratio like 16:9 or 4:3 to ensure consistent appearance across various screens."
        )
    else:
        st.success("Good aspect ratio!")
        layout_score = 10

    st.write(f"Layout Score: {layout_score}")

    # Typography Detection
    st.subheader("🔤 Typography Detection")
    st.write(f"Detected *{num_text_blocks}* text blocks.")

    if num_text_blocks > 15:
        st.warning("Too much text. Simplify the design.")
        text_score = 6 + min(3, (num_text_blocks - 15) * 0.5)
        suggestions.append(
            "There seems to be a heavy use of text, which might overwhelm the viewer. "
            "Simplify your content by highlighting key points with headings and using concise messaging, "
            "which enhances clarity and improves user engagement."
        )
    elif num_text_blocks == 0:
        st.warning("No text detected. Is that intentional?")
        text_score = 5
        suggestions.append(
            "No text was detected in your design. While minimalism can be beautiful, "
            "consider adding brief, guiding text to provide context or instructions to users, "
            "ensuring better understanding and interaction."
        )
    else:
        st.success("Good amount of text!")
        text_score = 10

    st.write(f"Text Score: {text_score}")

    st.markdown("---")

    # Final Score calculation
    final_score = round((color_score + layout_score + text_score) / 3, 1)
    st.write(f"Final Score: {final_score}")

    st.subheader("🏆 Your Design Score:")
    if final_score >= 9:
        st.markdown('<p style="font-size: 20px; font-weight: bold; color: #4CAF50;">Excellent! Your design is almost perfect! 🌟</p>', unsafe_allow_html=True)
    elif final_score >= 7:
        st.markdown('<p style="font-size: 20px; font-weight: bold; color: #FFC107;">Good work! A few tweaks can make it awesome.</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size: 20px; font-weight: bold; color: #F44336;">Needs improvement. Focus on balance and readability.</p>', unsafe_allow_html=True)

    # UX Improvement Suggestions
    st.subheader("💡 Suggestions for Better UX:")

    if suggestions:
        for sug in suggestions:
            if "light" in sug:
                icon = "🌞"
                bg = "#FFEB3B"
            elif "dark" in sug:
                icon = "🌑"
                bg = "#607D8B"
            elif "text" in sug:
                icon = "📝"
                bg = "#8BC34A"
            else:
                icon = "✨"
                bg = "#03A9F4"

            st.markdown(f"""
            <div style="background-color:{bg}; padding:10px; margin-bottom:10px; border-radius:8px; box-shadow:2px 2px 10px rgba(0, 0, 0, 0.1); font-size:14px;">
                <strong>{icon} {sug}</strong>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("✅ No major issues. Great job!")

    # Prepare Feedback Text
    feedback_text += f"Design Score: {final_score}/10\n\n"
    feedback_text += "Color Analysis:\n"
    feedback_text += f"Light colors: {light_colors}\nDark colors: {dark_colors}\n\n"
    feedback_text += f"Layout (Aspect Ratio): {ratio}:1\n\n"
    feedback_text += f"Typography: {num_text_blocks} text blocks detected\n\n"
    feedback_text += "Suggestions:\n"
    for sug in suggestions:
        feedback_text += f"- {sug}\n"

    st.markdown("---")
    st.subheader("📥 Download or Copy Your Feedback")

    # Download Feedback
    b64 = base64.b64encode(feedback_text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{uploaded_file.name.split(".")[0]}_feedback.txt">📄 Download Feedback as .txt</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Copy Feedback
    st.text_area("📋 Feedback Text (Select + Copy):", feedback_text, height=300)

else:
    st.info("👆 Please upload a design image to start.")

# End background div
st.markdown("</div>", unsafe_allow_html=True)
