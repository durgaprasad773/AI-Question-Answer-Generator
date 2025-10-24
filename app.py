import streamlit as st
import openai  # Ensure openai is in requirements.txt

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
    - Remember
    - Understand
    - Apply
    - Analyze
    - Evaluate
    - Create
    """)

# ---------------- Input Section ----------------
col1, col2 = st.columns(2)

with col1:
    marks = st.number_input("Marks per Question", min_value=1, max_value=100, value=5)
    topics = st.text_area(
        "Topics (one per line or comma-separated)",
        height=100,
        placeholder="e.g., Data Structures, Algorithms, Database Management"
    )

with col2:
    bloom_level = st.selectbox("Bloom's Level", ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"])
    num_questions = st.number_input("Number of Questions", min_value=1, max_value=20, value=5)

# ---------------- Optional Sections ----------------
st.subheader("📖 Syllabus Content (Optional)")
syllabus_content = st.text_area(
    "Provide detailed syllabus content (optional)",
    height=150,
    placeholder="Paste your syllabus content here. If provided, this will be used instead of topics."
)

st.subheader("💬 Additional Guidelines (Optional)")
additional_comments = st.text_area(
    "Add any specific instructions or preferences",
    height=100,
    placeholder="e.g., Focus on practical applications, avoid theoretical questions."
)

st.subheader("📝 Example Format")
example_format = st.text_area(
    "Example question & answer format",
    height=150,
    placeholder="""Example:
Q1. What is a binary search tree? (2 marks)
Answer: A binary search tree is a node-based structure where each node has two children. Left child is smaller, right child is greater.
"""
)

# ---------------- Generate Button ----------------
if st.button("🚀 Generate Questions & Answers", use_container_width=True):
    if not api_key:
        st.error("⚠️ Please enter your OpenAI API key!")
    elif not topics.strip() and not syllabus_content.strip():
        st.error("⚠️ Please enter either topics or syllabus content!")
    else:
        try:
            openai.api_key = api_key

            # Prepare topics string
            topics_list = [t.strip() for t in topics.replace("\n", ",").split(",") if t.strip()]
            topics_str = ", ".join(topics_list)

            # Prepare prompt
            prompt = f"""
Generate {num_questions} questions ({marks} marks each) for Bloom's level {bloom_level}.
Topics/Syllabus: {topics_str if topics_str else syllabus_content}
Additional guidelines: {additional_comments if additional_comments else 'N/A'}

Follow this format:
{example_format}

Output:
Q[number]. [Question text] ({marks} marks)
Answer: [Detailed answer]
"""

            with st.spinner("🤖 Generating questions and answers..."):
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role":"system","content":"You are an expert educator who creates high-quality exam questions and answers based on Bloom's Taxonomy."},
                        {"role":"user","content":prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2500
                )

                generated_content = response.choices[0].message["content"].strip()

                # Display results
                st.success("✅ Questions & Answers Generated Successfully!")
                st.markdown("---")
                st.markdown(
                    f"<div style='background-color:#f0f2f6;padding:20px;border-radius:10px;border-left:5px solid #1f77b4;'>{generated_content.replace(chr(10),'<br>')}</div>",
                    unsafe_allow_html=True
                )

                # Text area for copying
                st.text_area("📄 Copy below:", value=generated_content, height=300)

                # Download button
                st.download_button(
                    label="💾 Download as Text",
                    data=generated_content,
                    file_name="questions_and_answers.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Check your API key and try again.")

# ---------------- Footer ----------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#666;'>💡 Tip: Make sure your OpenAI API key has sufficient credits and permissions.</div>",
    unsafe_allow_html=True
)
