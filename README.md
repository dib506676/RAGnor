# RAGnor

> Get instant insight from your documents using a Retrieval-Augmented Generation (RAG) approach with an intuitive Streamlit interface.

---

## 🚀 Overview

**RAGnor** is a Streamlit-based web app that enables users to upload a PDF document, provide their Google API key, and ask natural language questions to extract meaningful insights from the file. It uses a retrieval-augmented generation pipeline to provide answers grounded in the document content.

---

## 🔧 Features

* ✅ Drag-and-drop PDF upload (max size: 200MB)
* ✅ Secure Google API key input
* ✅ Ask questions based on uploaded PDF
* ✅ Accurate responses using RAG technique

---

## 📄 Usage Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/dib506676/RAGnor.git
cd RAGnor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

---

## 🔍 How to Use It

1. Open the app in your browser (Streamlit will automatically do this after running the command).
2. On the **left sidebar**, use the file uploader to drag and drop your PDF document (limit: 200MB).
3. Click the **Upload** button below the file uploader.
4. In the main panel:

   * Enter your **Google API Key**. You can get one from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   * Type a question about the PDF content in the input field labeled `ask a question from pdf file`.
5. Press Enter and view the generated response with relevant context extracted from the document.

---

## Frontend

<img width="1454" alt="Screenshot 2025-06-16 at 2 12 28 PM" src="https://github.com/user-attachments/assets/a1fae11b-78e2-4d2d-8713-ef1fbcc40867" />

## 📁 Project Structure

```
.
├── app.py               # Main Streamlit app
├── requirements.txt     # Python dependencies
├── utils/               # Utility functions for processing
└── README.md            # Project documentation
```

---

## 🧰 Tech Stack

* **Frontend**: Streamlit
* **Backend**: Python, Google API (MakerSuite)
* **PDF Parsing**: PyPDF2 / pdfplumber
* **LLM Integration**: Google MakerSuite or similar
* **Vector DB**: FASSI
---

## 📢 Contact

For any queries or feedback, open an issue or contact [@dib506676](https://github.com/dib506676).

---

Enjoy using **RAGnor** to unlock insights from your PDFs!
