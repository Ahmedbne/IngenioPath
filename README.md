# IngenioPath
IngenioPath is an intelligent learning assistant designed to help users explore and understand content from PDF documents through interactive modes. It leverages Google's Gemini AI to provide a responsive and engaging learning experience.

## Features

IngenioPath offers several modes to interact with your PDF documents:

*   **Informative Mode:** Engage in a conversation with the AI to ask questions and get detailed answers based on the content of your uploaded PDF files. This mode is perfect for in-depth exploration and understanding of the material.
*   **Game Mode (Devinette):** Test your knowledge with a fun guessing game! You will provide clues related to the PDF content, and the AI will try to guess the concept or term.
*   **Quiz Mode:** Challenge yourself with quizzes generated from the PDF documents. This is a great way to assess your understanding and retention of the material.
*   **PDF Processing:** IngenioPath can process text from PDF files located in the `PDF/` directory. It extracts the text, divides it into manageable chunks, and creates a vector store for efficient information retrieval. (RAG)

## Technical Stack

IngenioPath is built using the following technologies:

*   **Streamlit:** For creating the interactive web application interface.
*   **Google Generative AI (Gemini):** Powers the AI-driven conversations, game logic, and quiz generation.
*   **Langchain:** Used as a framework to develop language model applications, facilitating PDF processing and interaction.
*   **FAISS:** For creating and managing the vector store, enabling efficient similarity searches within the document content.
*   **PyPDF2:** For extracting text from PDF documents.

## Setup and Usage

To get IngenioPath up and running on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> 
    cd IngenioPath 
    ```
    *(Replace `<repository_url>` with the actual URL of the repository)*

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Make sure you have Python installed. Then, install the required packages using `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Google API Key:**
    IngenioPath uses Google's Generative AI. You'll need a Google API key.
    *   Create a file named `.env` in the root directory of the project.
    *   Add your API key to the `.env` file like this:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY"
        ```
    *   Replace `"YOUR_API_KEY"` with your actual Google API key.

5.  **Add PDF Files:**
    Place any PDF documents you want to use with the application into the `PDF/` directory. If this directory doesn't exist, please create it in the root of the project.

6.  **Run the Application:**
    Once the dependencies are installed and the API key is set up, you can run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
    The application should open in your web browser. You can then select the desired mode and start interacting with IngenioPath.

## Future Improvements

We are continuously looking to enhance IngenioPath. Some potential future improvements include:

*   Support for more document formats (e.g., DOCX, TXT).
*   Advanced quiz customization options.
*   User accounts and personalized learning paths.
*   Integration with other learning platforms or APIs.
*   Enhanced game modes with more variety.

Contributions are welcome! If you have ideas or want to contribute, please feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
