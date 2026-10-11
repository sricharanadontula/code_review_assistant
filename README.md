# 🔍 AI Code Review & Explanation Assistant

An AI-powered application that helps developers review code quality, identify potential issues, receive improvement suggestions, and understand code through beginner-friendly explanations.

Built using **Python, Streamlit, and Google's Gemini API**, this project provides an interactive interface for both code review and code explanation.

## 🚀 Features

### 1. AI Code Review
- Identifies potential coding issues and possible bugs.
- Suggests improvements for readability and maintainability.
- Evaluates code quality as Low, Medium, or High.
- Generates a concise review summary.
- Returns structured JSON output.

### 2. Code Explanation
- Explains the overall purpose of a program.
- Identifies important functions, variables, libraries, and components.
- Describes the program's execution flow.
- Provides grouped, line-by-line explanations with source line numbers.
- Explains expected inputs, outputs, dependencies, and limitations.
- Displays explanations in expandable sections for easy navigation.

### 3. Flexible Code Input
- Paste code directly into the application.
- Upload supported source-code files.
- Supports Python, Java, JavaScript, C, C++, SQL, and other programming languages.

### 4. Safety and Validation
- Analyzes submitted code as text without executing it.
- Validates input length and uploaded file size.
- Uses environment variables and deployment secrets to protect API credentials.

## 🛠️ Technology Stack

- **Programming Language:** Python
- **Frontend:** Streamlit
- **AI Model API:** Google Gemini API
- **Data Validation:** Pydantic
- **Libraries:** Google Gen AI SDK, python-dotenv
- **Version Control:** Git and GitHub
- **Deployment:** Streamlit Community Cloud

## 📁 Project Structure

```text
Code_Review_Generator/
│
├── app.py               # Streamlit user interface
├── review_engine.py     # AI review and explanation logic
├── schemas.py           # Structured response validation
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment configuration
├── .gitignore           # Excludes secrets and local files
└── README.md            # Project documentation
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version supported by your dependencies
- Git
- A Google Gemini API key

### 1. Clone the repository

```bash
git clone https://github.com/sricharanadontula/code_review_assistant.git
cd code_review_assistant
```

### 2. Create a virtual environment

**Windows:**

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder with your actual API key.

**Important:** Never commit your `.env` file or expose your API key publicly.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser, usually at:

```text
http://localhost:8501
```

## 📖 How to Use

1. Open the application.
2. Select **Review Code** or **Explain Code**.
3. Choose the programming language.
4. Paste your code or upload a supported source file.
5. Click the corresponding action button.
6. Review the generated results.

For code review, the application displays identified issues, improvement suggestions, code quality, a review summary, and structured JSON.

For code explanation, the application presents the overview, important components, execution flow, line-by-line explanation, input/output, and dependencies in expandable sections.

## 📋 Code Review Output

The code review engine produces a structured response with the following fields:

```json
{
  "identified_issues": [
    "Potential issue identified in the submitted code"
  ],
  "improvement_suggestions": [
    "Consider improving naming and readability"
  ],
  "code_quality_level": "Medium",
  "review_summary": "A concise summary of the code review"
}
```

*The example above illustrates the expected response format. Actual results depend on the submitted code.*

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | API key used to access the Gemini model |

For deployment, configure `GEMINI_API_KEY` through the hosting platform's secrets settings rather than committing credentials to the repository.

## ☁️ Deployment

This application can be deployed using Streamlit Community Cloud.

1. Push the project to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create an app and select this repository.
4. Set the branch to `main` and the main file to `app.py`.
5. Add your `GEMINI_API_KEY` in the app's Secrets settings.
6. Deploy and test the public application.

**Live Demo:** Add your deployed Streamlit URL here after deployment.

## ⚠️ Limitations

- AI-generated feedback may be inaccurate or incomplete.
- The application performs static analysis through an AI model; it does not execute the submitted code.
- The model may miss certain bugs, security vulnerabilities, or language-specific issues.
- Explanation quality depends on the submitted code and the AI model's response.
- API availability, rate limits, and usage costs depend on the Gemini API configuration.

Always verify generated recommendations before applying them to production code.

## 🔮 Future Enhancements

- Support for additional programming languages.
- More detailed security and performance analysis.
- Downloadable code review reports.
- Code comparison and review history.
- Automated test-case suggestions.
- Improved error handling and response validation.

## 👩‍💻 Author

**Sricharana Dontula**

B.Tech – Computer Science and Engineering (AI & ML)

GitHub: [@sricharanadontula](https://github.com/sricharanadontula)

---

⭐ If you find this project useful, consider giving the repository a star.

*This project was developed to explore AI-powered developer tools, code quality analysis, and beginner-friendly programming education.*
