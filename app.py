import streamlit as st
import openai  # Classic OpenAI import that works everywhere

# ---------------- Page Setup ----------------
st.set_page_config(page_title="AI Question Generator", layout="wide")

st.title("📚 AI Question & Answer Generator")
st.markdown("Generate questions and answers based on marks, topics, and Bloom's Taxonomy levels")

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    st.markdown("---")
    st.markdown("### Bloom's Taxonomy Levels")
    st.markdown("""
    - **Remember**: Recall facts and basic concepts  
    - **Understand**: Explain ideas or concepts  
    - **Apply**: Use information in new situations  
    - **Analyze**: Draw connections among ideas  
    - **Evaluate**: Justify a stand or decision  
    - **Create**: Produce new or original work  
    """)

# ---------------- Input Section ----------------
col1, col2 = st.columns(2)

with col1:
    marks = st.number_input("Marks per Question", min_value=1, max_value=100, value=5, step=1)
    topics = st.text_area(
        "Topics (one per line or comma-separated)",
        height=100,
        placeholder="e.g., Data Structures, Algorithms, Database Management"
    )

with col2:
    bloom_level = st.selectbox(
        "Bloom's Taxonomy Level",
        ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
    )
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5, step=1)

# ---------------- Syllabus Section ----------------
st.markdown("---")
st.subheader("📖 Syllabus Content (Optional)")
syllabus_content = st.text_area(
    "Provide detailed syllabus content (optional)",
    height=150,
    placeholder="Paste your syllabus content here. If provided, this will be used instead of topics.",
)

# ---------------- Additional Comments ----------------
st.subheader("💬 Additional Comments/Guidelines (Optional)")
additional_comments = st.text_area(
    "Add any specific guidelines or preferences",
    height=100,
    placeholder="e.g., Focus on practical applications, avoid theoretical questions, etc.",
)

# ---------------- Example Format ----------------
st.markdown("---")
st.subheader("📝 Question & Answer Format Example")
example_format = st.text_area(
    "Provide an example of how questions and answers should be formatted",
    height=150,
    placeholder="""Example:
Q1. What is a binary search tree? (2 marks)
Answer: A binary search tree is a node-based structure where each node has two children. The left child is smaller, and the right child is greater.

Q2. Explain the time complexity of binary search. (3 marks)
Answer: Binary search has a time complexity of O(log n)..."""
)

# ---------------- Generate Button ----------------
if st.button("🚀 Generate Questions & Answers", use_container_width=True):
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key in the sidebar!")
    elif not topics.strip() and not syllabus_content.strip():
        st.error("⚠️ Please enter either topics or syllabus content!")
    else:
        try:
            # Set API key
            openai.api_key = api_key

            # Prepare topics
            topics_list = [t.strip() for t in topics.replace('\n', ',').split(',') if t.strip()]
            topics_str = ", ".join(topics_list)

            # Prepare prompt
            prompt = f"""
Generate {num_questions} unique questions and answers based on the following:

- Marks per question: {marks}
- Bloom's Taxonomy Level: {bloom_level}
- Topics: {topics_str if topics_str else syllabus_content}
- Additional Comments: {additional_comments if additional_comments else 'N/A'}

Requirements:
1. Strictly generate {num_questions} questions.
2. Each question must carry {marks} marks.
3. Questions should align with the {bloom_level} level of Bloom's Taxonomy.
4. Follow the example format below:
{example_format}

Output format:
Q[number]. [Question text] ({marks} marks)
Answer: [Detailed answer]
"""

            with st.spinner("🤖 Generating questions and answers..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert educator who creates exam questions and answers based on Bloom's Taxonomy."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=2500
                )

                generated_content = response.choices[0].message["content"].strip()

                # ---------------- Display Results ----------------
                st.success("✅ Questions and Answers Generated Successfully!")
                st.markdown("---")
                st.markdown("### 📋 Generated Questions & Answers")

                st.markdown(
                    f"""
                    <div style="background-color:#f0f2f6;padding:20px;border-radius:10px;border-left:5px solid #1f77b4;">
                    {generated_content.replace('\n', '<br>')}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Text area for copy/download
                st.markdown("---")
                st.text_area("📄 Copy the content below:", value=generated_content, height=300, key="output_text")

                st.download_button(
                    label="💾 Download as Text",
                    data=generated_content,
                    file_name="questions_and_answers.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your API key and try again.")

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#666;">
        💡 Tip: Make sure your OpenAI API key has sufficient credits and permissions.
    </div>
    """,
    unsafe_allow_html=True
)
