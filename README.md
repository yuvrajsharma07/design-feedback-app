# design-feedback-app
An AI-powered Streamlit app that analyzes uploaded design images and provides instant feedback on color balance, layout proportions, and typography using machine learning and OCR. Ideal for designers seeking quick and professional UI/UX insights.
# 🎨 Design Feedback Pro

**Design Feedback Pro** is a Streamlit-based web app that provides instant, AI-powered feedback on uploaded design images. It analyzes color balance, layout ratio, and typography using KMeans clustering and OCR (EasyOCR).

## 🚀 Features

- 🔍 **Color Analysis** – Detects dominant colors and evaluates light/dark balance.
- 📐 **Layout Evaluation** – Assesses aspect ratio for responsiveness.
- 🔤 **Typography Detection** – Uses OCR to identify and count text blocks.
- 💡 **Smart Suggestions** – Offers actionable tips to improve UX.
- 📥 **Downloadable Feedback** – Save results as a .txt file or copy directly.

## 🛠 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
