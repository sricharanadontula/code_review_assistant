
import json
import re
import streamlit as st

from review_engine import review_code, explain_code


MAX_CODE_CHARS = 50000
MAX_FILE_BYTES = 1024 * 1024  # 1 MB

SUPPORTED_EXTENSIONS = [
    "py", "java", "js", "ts", "jsx", "tsx",
    "c", "cpp", "h", "hpp", "cs", "go", "rs",
    "php", "rb", "swift", "kt", "sql", "txt",
]


st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="🔍",
    layout="wide",
)


st.title("AI Code Review & Explanation Assistant")

st.write(
    "Review code quality or learn how a program works. "
    "Submitted code is analyzed as text and is never executed."
)


mode = st.radio(
    "Choose a task",
    ["Review Code", "Explain Code"],
    horizontal=True,
)


language = st.selectbox(
    "Programming language",
    [
        "Python", "Java", "JavaScript", "TypeScript",
        "C", "C++", "C#", "Go", "Rust", "PHP",
        "Ruby", "Swift", "Kotlin", "SQL", "Other",
    ],
)


input_method = st.radio(
    "How would you like to provide your code?",
    ["Paste Code", "Upload File"],
    horizontal=True,
)


code = ""

if input_method == "Paste Code":

    code = st.text_area(
        "Paste your code here",
        height=400,
        max_chars=MAX_CODE_CHARS,
        placeholder="Paste your program here...",
        key="code_input",
    )

    st.caption(
        f"Code length: {len(code)} / "
        f"{MAX_CODE_CHARS} characters"
    )

else:

    uploaded_file = st.file_uploader(
        "Upload a source-code file",
        type=SUPPORTED_EXTENSIONS,
        help=(
            "Maximum file size: 1 MB. "
            "The file is read as text, never executed."
        ),
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        if len(file_bytes) > MAX_FILE_BYTES:
            st.error("The file exceeds the 1 MB upload limit.")

        else:
            try:
                code = file_bytes.decode("utf-8")

                if len(code) > MAX_CODE_CHARS:
                    st.error(
                        "The file exceeds the 50,000-character "
                        "processing limit."
                    )
                    code = ""

                else:
                    st.success(
                        f"Loaded {uploaded_file.name} "
                        f"({len(code)} characters)."
                    )

                    st.text_area(
                        "Uploaded source preview",
                        value=code,
                        height=250,
                        disabled=True,
                    )

            except UnicodeDecodeError:
                st.error(
                    "The file is not valid UTF-8 text. "
                    "Please upload a text-based source file."
                )


def display_explanation(explanation):
    """Display a code explanation in expandable sections."""

    section_names = [
        "1. CODE OVERVIEW",
        "2. IMPORTANT COMPONENTS",
        "3. EXECUTION FLOW",
        "4. LINE-BY-LINE EXPLANATION",
        "5. INPUT AND OUTPUT",
        "6. DEPENDENCIES AND LIMITATIONS",
    ]

    # Normalize line endings and remove common Markdown formatting
    # when matching headings.
    text = explanation.replace("\r\n", "\n").replace("\r", "\n")

    # Match headings with optional Markdown hashes and bold markers.
    heading_pattern = re.compile(
        r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?"
        r"(?:\*\*)?"
        r"(?P<heading>"
        r"[1-6][.)][ \t]+"
        r"(?:CODE OVERVIEW|IMPORTANT COMPONENTS|EXECUTION FLOW|"
        r"LINE-BY-LINE EXPLANATION|INPUT AND OUTPUT|"
        r"DEPENDENCIES AND LIMITATIONS)"
        r")"
        r"(?:\*\*)?[ \t]*:?[ \t]*$"
    )

    matches = list(heading_pattern.finditer(text))

    # Also support the common heading "### Overall Explanation".
    overall_pattern = re.compile(
        r"(?im)^[ \t]*(?:#{1,6}[ \t]*)?"
        r"(?:\*\*)?OVERALL EXPLANATION(?:\*\*)?[ \t]*:?[ \t]*$"
    )

    overall_match = overall_pattern.search(text)

    if not matches:
        # If Gemini returns unexpected formatting, still show its
        # response instead of hiding it.
        st.markdown(text)
        return

    sections = []

    # Include an overall explanation as a separate section if present.
    if overall_match:
        first_heading_start = matches[0].start()

        if overall_match.start() < first_heading_start:
            overall_content = text[
                overall_match.end():first_heading_start
            ].strip()

            if overall_content:
                sections.append(
                    ("Overall Explanation", overall_content)
                )

    # Preserve the text before the first recognized heading.
    preamble = text[:matches[0].start()].strip()

    if preamble and not overall_match:
        sections.append(("Introduction", preamble))

    for index, match in enumerate(matches):
        content_start = match.end()

        content_end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        heading = match.group("heading")
        content = text[content_start:content_end].strip()

        # Convert the model's heading to a consistent display title.
        title_text = re.sub(
            r"^[1-6][.)][ \t]*", "", heading
        ).strip().title()

        sections.append((title_text, content))

    # Remove duplicate section headings while preserving their order.
    displayed = set()

    for title_text, content in sections:
        if title_text in displayed:
            continue

        displayed.add(title_text)

        expanded_by_default = title_text in {
            "Overall Explanation",
            "Code Overview",
        }

        with st.expander(
            title_text,
            expanded=expanded_by_default,
        ):
            if content:
                st.markdown(content)
            else:
                st.caption(
                    "No explanation was provided for this section."
                )


if st.button(
    mode,
    type="primary",
    use_container_width=True,
):

    if not code.strip():
        st.warning(
            "Please paste some code or upload a valid file."
        )

    elif len(code) > MAX_CODE_CHARS:
        st.error(
            "The code is too long. Reduce it to "
            "50,000 characters or fewer."
        )

    else:

        spinner_message = (
            "Reviewing your code..."
            if mode == "Review Code"
            else "Preparing your explanation..."
        )

        with st.spinner(spinner_message):

            try:

                if mode == "Review Code":

                    result = review_code(code, language)

                    st.subheader("Identified Issues")

                    if result.identified_issues:
                        for issue in result.identified_issues:
                            st.markdown(f"- {issue}")
                    else:
                        st.success(
                            "No significant issues identified."
                        )

                    st.subheader("Improvement Suggestions")

                    if result.improvement_suggestions:
                        for suggestion in (
                            result.improvement_suggestions
                        ):
                            st.markdown(f"- {suggestion}")
                    else:
                        st.write(
                            "No specific improvements suggested."
                        )

                    st.subheader("Code Quality")
                    st.write(result.code_quality_level)

                    st.subheader("Review Summary")
                    st.write(result.review_summary)

                    st.subheader("JSON Output")

                    st.code(
                        json.dumps(
                            result.model_dump(),
                            indent=2,
                            ensure_ascii=False,
                        ),
                        language="json",
                    )

                else:

                    explanation = explain_code(code, language)

                    st.subheader("Code Explanation")

                    display_explanation(explanation)

            except Exception as error:

                st.error(
                    "The request failed. Check your API key, "
                    "model availability, internet connection, "
                    "and API usage limits."
                )

                with st.expander("Technical error details"):
                    st.code(str(error))


st.divider()

st.caption(
    "AI-generated feedback may be inaccurate. "
    "Always verify suggestions. This application does not "
    "execute submitted code."
)
