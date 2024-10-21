import streamlit as st
import pandas as pd
from groq import Groq

from io import StringIO

# Initialize session state
if 'groq_client' not in st.session_state:
    st.session_state.groq_client = None

# Sidebar for API key and model settings
st.sidebar.header("LLM Configuration")

api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")
model = st.sidebar.selectbox("Select Model", ["mixtral-8x7b-32768", "llama3-8b-8192", "llama-3.1-8b-instant"])
max_tokens = st.sidebar.slider("Max Tokens", min_value=2048, max_value=32786, value=8192, step=256)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

st.sidebar.write(""" ### Notes: \n
**Knowledge (K)** \n 
Subject Matter Expertise (K): "Assesses depth and breadth of knowledge in the specific subject area."\n
Environmental Literacy (K): "Assesses understanding of environmental issues, their causes, impacts, and approaches to sustainability."\n
Theoretical Understanding (K): "Evaluates comprehension of fundamental theories and concepts."\n
Interdisciplinary Knowledge (K): "Measures ability to connect ideas across different disciplines."\n
Social Change Knowledge (K): "Assesses understanding of social structures and historical transformations." \n
Cultural Knowledge (K): "Assesses knowledge of cultural influences and their implications on tourism."\n
---
**Skills (S)** \n
Critical Thinking (S): "Assesses ability to analyze, evaluate, and synthesize information."\n
Systematic Decision-Making (S): "Assesses ability to use structured processes to make well-informed and impactful decisions."\n
Problem-Solving (S): "Evaluates capacity to identify, frame, and resolve complex problems."\n
Design Thinking and Innovation (S): "Assesses ability to apply design thinking methodologies to develop innovative and practical solutions."\n
Communication Skills (S): "Measures effectiveness in verbal, written, and visual communication."\n
Technical Proficiency (S): "Assesses mastery of relevant tools, technologies, or methodologies."\n
Creativity (S): "Assesses ability to generate original ideas and innovative solutions to challenges."\n
Digital Literacy (S): "Assesses ability to navigate, evaluate, and create information using digital technologies."\n
AI Literacy (S): "Measures proficiency in understanding and applying artificial intelligence tools, technologies, and ethical considerations."\n
Analytical Skills (S): "Assesses ability to evaluate and interpret data effectively." \n
Collaboration Skills (S): "Measures ability to work effectively in teams and contribute to collective goals." \n
---
**Ethics (E)** \n
Ethical Reasoning (E): "Evaluates ability to recognize and analyze ethical issues."\n
Professional Ethics (E): "Assesses understanding and application of field-specific ethical standards."\n
Social Responsibility (E): "Measures awareness and commitment to broader societal impacts."\n
Sustainability Awareness (E): "Evaluates understanding of sustainable practices and their impact on environmental, social, and economic systems."\n
Cultural Sensitivity (E): "Assesses understanding and respect for diverse cultural perspectives and practices." \n
---
**Character (C)** \n
Perseverance (C): "Assesses ability to persist through challenges and setbacks."\n
Integrity (C): "Evaluates adherence to moral and ethical principles in academic and professional contexts."\n
Empathy and Perspective-Taking (C): "Measures ability to understand diverse viewpoints, including environmental, societal, and future generational concerns."\n
Respect (C): "Measures ability to show consideration and regard for others' opinions, rights, and feelings."\n
Responsibility (C): "Assesses commitment to fulfilling duties and being accountable for actions and decisions."\n
Open-Mindedness (C): "Evaluates ability to consider and embrace new ideas and different perspectives." \n
---
**Teamwork and Collaboration** \n
Contribution to Team Goals: "Measures students' ability to apply knowledge to help achieve team objectives."\n
Collaborative Problem Solving: "Assesses ability to work with others to solve complex problems."\n
Leadership and Initiative: "Evaluates capacity to guide and motivate team members."\n
---
**Reflection and Growth** \n
Self-Reflection: "Assesses ability to critically evaluate one's own performance and learning."\n
Continuous Learning: "Measures commitment to ongoing personal and professional development."\n
Adaptability: "Evaluates ability to adjust to new situations and incorporate feedback."\n
""")


# Initialize or update Groq client when API key is provided
if api_key:
    st.session_state.groq_client = Groq(api_key=api_key)

# Define preset criteria and performance levels
PRESET_CRITERIA = {
    # Knowledge (K)
    "Subject Matter Expertise (K)": "Assesses depth and breadth of knowledge in the specific subject area.",
    "Environmental Literacy (K)": "Assesses understanding of environmental issues, their causes, impacts, and approaches to sustainability.",
    "Theoretical Understanding (K)": "Evaluates comprehension of fundamental theories and concepts.",
    "Interdisciplinary Knowledge (K)": "Measures ability to connect ideas across different disciplines.",
    "Social Change Knowledge (K)": "Assesses understanding of social structures and historical transformations." ,  # เพิ่ม
    "Cultural Knowledge (K)": "Assesses knowledge of cultural influences and their implications on tourism.",  # เพิ่ม
    
    # Skills (S)
    "Critical Thinking (S)": "Assesses ability to analyze, evaluate, and synthesize information.",
    "Systematic Decision-Making (S)": "Assesses ability to use structured processes to make well-informed and impactful decisions.",
    "Problem-Solving (S)": "Evaluates capacity to identify, frame, and resolve complex problems.",
    "Design Thinking and Innovation (S)": "Assesses ability to apply design thinking methodologies to develop innovative and practical solutions.",
    "Communication Skills (S)": "Measures effectiveness in verbal, written, and visual communication.",
    "Technical Proficiency (S)": "Assesses mastery of relevant tools, technologies, or methodologies.",
    "Creativity (S)": "Assesses ability to generate original ideas and innovative solutions to challenges.",
    "Digital Literacy (S)": "Assesses ability to navigate, evaluate, and create information using digital technologies.",
    "AI Literacy (S)": "Measures proficiency in understanding and applying artificial intelligence tools, technologies, and ethical considerations.",
    "Analytical Skills (S)": "Assesses ability to evaluate and interpret data effectively.",  # เพิ่ม
    "Collaboration Skills (S)": "Measures ability to work effectively in teams and contribute to collective goals.",  # เพิ่ม
                
    # Ethics (E)
    "Ethical Reasoning (E)": "Evaluates ability to recognize and analyze ethical issues.",
    "Professional Ethics (E)": "Assesses understanding and application of field-specific ethical standards.",
    "Social Responsibility (E)": "Measures awareness and commitment to broader societal impacts.",
    "Sustainability Awareness (E)": "Evaluates understanding of sustainable practices and their impact on environmental, social, and economic systems.",
    "Cultural Sensitivity (E)": "Assesses understanding and respect for diverse cultural perspectives and practices.",  # เพิ่ม
    
    # Character (C)
    "Perseverance (C)": "Assesses ability to persist through challenges and setbacks.",
    "Integrity (C)": "Evaluates adherence to moral and ethical principles in academic and professional contexts.",
    "Empathy and Perspective-Taking (C)": "Measures ability to understand diverse viewpoints, including environmental, societal, and future generational concerns.",
    "Respect (C)": "Measures ability to show consideration and regard for others' opinions, rights, and feelings.",
    "Responsibility (C)": "Assesses commitment to fulfilling duties and being accountable for actions and decisions.",
    "Open-Mindedness (C)": "Evaluates ability to consider and embrace new ideas and different perspectives.",  # เพิ่ม
    
    # Teamwork and Collaboration
    "Contribution to Team Goals": "Measures students' ability to apply knowledge to help achieve team objectives.",
    "Collaborative Problem Solving": "Assesses ability to work with others to solve complex problems.",
    "Leadership and Initiative": "Evaluates capacity to guide and motivate team members.",
    
    # Reflection and Growth
    "Self-Reflection": "Assesses ability to critically evaluate one's own performance and learning.",
    "Continuous Learning": "Measures commitment to ongoing personal and professional development.",
    "Adaptability": "Evaluates ability to adjust to new situations and incorporate feedback."
}

PERFORMANCE_LEVELS = ["Exemplary", "Proficient", "Adequate", "Developing", "Needs Improvement"]


def generate_rubric_with_llm(learning_outcomes, criteria, performance_levels):
    if not st.session_state.groq_client:
        st.error("Please enter a valid Groq API key in the sidebar.")
        return None

    prompt = f"""
    Generate a detailed rubric based on the following:
    
    Learning Outcomes:
    {', '.join(learning_outcomes)}
    
    Criteria:
    {', '.join(criteria)}
    
    Performance Levels:
    {', '.join(performance_levels)}
    
    For each criterion, provide a brief description and detailed explanations for each performance level that reflects implicitly associated to Learning Outcomes in plained text.
    Format the output as a Markdown table with the following columns:
    | Criteria | {' | '.join(performance_levels)} |
    
    Each row should represent a criterion, with descriptions for each performance level.
    Ensure the table is properly formatted with | characters and a header row separator.
    Ensure the output table format is consistent as possible everytime.
    """
    
    try:
        chat_completion = st.session_state.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            #model="llama-3.1-8b-instant",  # Using llama-3.1 model
            model= model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        llm_output = chat_completion.choices[0].message.content
        return llm_output
    except Exception as e:
        st.error(f"Error in generating LLM output: {str(e)}")
        return None

def parse_markdown_table(markdown_table):
    # Split the table into lines
    lines = markdown_table.strip().split('\n')

    # Extract headers
    #headers = [header.strip() for header in re.findall(r'\|(.*?)\|', lines[0])]
    headers = [header.strip() for header in lines[0].strip().split('|')[1:-1]]
    headers = [h for h in headers if h] 

    # Extract data rows
    data = []
    for line in lines[2:]:  # Skip the header and separator rows
        row = [cell.strip() for cell in line.strip().split('|')[1:-1]]
        row = [cell for cell in row if cell]
        if row:
            while len(row) < len(headers):
                row.append('')
            data.append(row[:len(headers)])
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df

def main():
    st.title("LLM-Enhanced Rubric Generator for Learning Outcomes")
    st.text("by JTIAPBN.Ai - v.1.0")
    # User input section
    st.header("1. Define Learning Outcomes")
    num_outcomes = st.number_input("Number of learning outcomes", min_value=1, max_value=10, value=1)
    
    learning_outcomes = []
    for i in range(num_outcomes):
        outcome = st.text_input(f"Learning Outcome {i+1}")
        learning_outcomes.append(outcome)

    # Rubric criteria selection
    st.header("2. Select Rubric Criteria")
    selected_criteria = st.multiselect("Choose criteria for your rubric", list(PRESET_CRITERIA.keys()))

    # Performance levels
    st.header("3. Customize Performance Levels")
    use_preset_levels = st.checkbox("Use preset performance levels", value=True)
    if use_preset_levels:
        performance_levels = PERFORMANCE_LEVELS
    else:
        num_levels = st.number_input("Number of performance levels", min_value=2, max_value=7, value=5)
        performance_levels = [st.text_input(f"Performance Level {i+1}", value=PERFORMANCE_LEVELS[i] if i < len(PERFORMANCE_LEVELS) else "") for i in range(num_levels)]

 # Generate rubric
    if st.button("Generate Rubric"):
        if not st.session_state.groq_client:
            st.error("Please enter a valid Groq API key in the sidebar before generating the rubric.")
        elif not learning_outcomes or not selected_criteria or not performance_levels:
            st.error("Please fill in all required fields before generating the rubric.")
        else:
            with st.spinner("Generating rubric with LLM..."):
                generated_rubric = generate_rubric_with_llm(learning_outcomes, selected_criteria, performance_levels)

            if generated_rubric:
                st.header("Generated Rubric")
                st.markdown(generated_rubric)  # Display original Markdown table
                
                try:
                    df = parse_markdown_table(generated_rubric)
                    
                    if df.empty:
                        st.error("Failed to parse the generated rubric. Please try again.")
                    else:
                        # Display the parsed table
                        st.dataframe(df)
                        
                        # Create CSV string
                        csv_buffer = StringIO()
                        df.to_csv(csv_buffer, index=False)
                        csv_string = csv_buffer.getvalue()
                        
                        # Add download button for CSV
                        st.download_button(
                            label="Download Rubric as CSV",
                            data=csv_string,
                            file_name="rubric.csv",
                            mime="text/csv",
                        )
                    
                except Exception as e:
                    st.error(f"Error parsing or displaying rubric: {str(e)}")
                    st.error("Raw generated content:")
                    st.code(generated_rubric)

if __name__ == "__main__":
    main()
