# PDF Chatbot Streamlit App

This is a Streamlit web application that allows users to upload a PDF, extract its text, and ask questions about the content using a chatbot powered by LangChain and OpenAI's GPT-3.5-turbo model. The app generates a LaTeX file containing the conversation history, which can be compiled into a PDF report.

## Features
- Upload a text-based PDF file to extract its content.
- Ask questions about the PDF content via a chat interface.
- Receive AI-generated responses powered by OpenAI's GPT-3.5-turbo model.
- Download the conversation history as a LaTeX (.tex) file for PDF compilation.
- Error handling for OpenAI API rate limits and other issues.

## Requirements
- **Python**: 3.8 or higher
- **Dependencies**:
  - `streamlit`
  - `langchain-openai`
  - `langchain-core`
  - `PyPDF2`
- **OpenAI API Key**: Obtain from [OpenAI Platform](https://platform.openai.com/).
- **LaTeX Distribution**: TeX Live or similar (optional, for compiling the output `.tex` file to PDF).
- **Text-based PDF**: The input PDF must contain extractable text (not scanned images).

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/pdf-chatbot-app.git
   cd pdf-chatbot-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install streamlit langchain-openai langchain-core PyPDF2
   ```

3. **Set Up OpenAI API Key**:
   - Obtain an API key from [OpenAI Platform](https://platform.openai.com/).
   - Set the environment variable:
     ```bash
     export OPENAI_API_KEY="your-actual-key"
     ```
   - Alternatively, enter the API key in the app's interface when prompted.

4. **Install LaTeX (Optional)**:
   - To compile the generated `.tex` file to PDF, install a LaTeX distribution like [TeX Live](https://www.tug.org/texlive/).

## Usage
1. **Run the Streamlit App**:
   ```bash
   streamlit run pdf_chatbot_app.py
   ```
   - Open the provided URL (e.g., `http://localhost:8501`) in a web browser.

2. **Interact with the App**:
   - Upload a text-based PDF file using the file uploader.
   - Enter your OpenAI API key if not set via environment variable.
   - Ask questions about the PDF content in the text input field.
   - View responses in the chat interface.
   - Download the conversation history as `chatbot_report.tex` using the download button.

3. **Compile the LaTeX File** (Optional):
   - After downloading `chatbot_report.tex`, compile it to PDF:
     ```bash
     latexmk -pdf chatbot_report.tex
     ```

## Example Interaction
1. Upload `sample.pdf`.
2. Ask: "What is the main topic of the PDF?"
   - Response: "The main topic is [AI-generated response]."
3. Ask: "Who is the author?"
   - Response: "The PDF does not specify an author."
4. Download `chatbot_report.tex` and compile to PDF.

## Troubleshooting
- **OpenAI API Quota Error (429)**:
  - Indicates you’ve exceeded your API usage limit. Check your [OpenAI account](https://platform.openai.com/) for billing and credit details.
  - Consider upgrading your plan or purchasing additional credits.
  - Alternatively, explore xAI's API at [https://x.ai/api](https://x.ai/api) for similar functionality.
- **PDF Extraction Issues**:
  - Ensure the PDF is text-based. For scanned PDFs, use an OCR tool like `pytesseract`.
- **LaTeX Compilation Errors**:
  - Verify that a LaTeX distribution (e.g., TeX Live) is installed.
  - Run `latexmk -pdf chatbot_report.tex` in the directory containing the file.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bugs, feature requests, or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, contact [Your Name] at [your.email@example.com] or open an issue on GitHub.