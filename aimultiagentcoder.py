import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
import logging

logging.basicConfig(level=logging.DEBUG)

st.title("AI-Powered Multi-Agent Collaboration Framework 🤖")
st.caption("Build an AI team where different agents handle coding, debugging, research, and documentation.")

# Sidebar for API key input and link
st.sidebar.markdown("[Get your GEMINI API Key](https://ai.google.dev/) 📌")
Google_api_key = st.sidebar.text_input("Enter GEMINI API Key", type="password")

# User input for task request
task_request = st.text_area("Enter your task request:")

if st.button("Execute Task"):
    if not Google_api_key:
        st.warning("Please enter the required API key.")
    else:
        with st.spinner("Processing your request..."):
            try:
                # Initialize GEMINI model
                model = Gemini(id="gemini-1.5-flash", api_key=Google_api_key)

                # Developer Agent
                developer_agent = Agent(
                    name="Python Developer",
                    role="Writes Python code based on user requirements",
                    model=model,
                    instructions=["Generate clean, well-documented Python code for the given task."],
                    markdown=True,
                )

                # Tester Agent
                tester_agent = Agent(
                    name="Python Tester",
                    role="Tests and debugs Python code",
                    model=model,
                    instructions=["Analyze the provided code, write test cases, and identify potential bugs."],
                    markdown=True,
                )

                # Research Agent
                research_agent = Agent(
                    name="Researcher",
                    role="Finds relevant information and resources",
                    model=model,
                    instructions=["Research best practices, provide documentation references, and summarize key findings."],
                    markdown=True,
                )

                # Documentation Agent
                documentation_agent = Agent(
                    name="Technical Writer",
                    role="Creates detailed documentation for the generated code",
                    model=model,
                    instructions=["Write clear and structured documentation, including usage examples and explanations."],
                    markdown=True,
                )

                # Multi-agent workflow
                agent_team = Agent(
                    team=[developer_agent, tester_agent, research_agent, documentation_agent],
                    instructions=[
                        "First, the Python Developer writes the required code.",
                        "Then, the Python Tester reviews the code, writes test cases, and identifies bugs.",
                        "The Researcher finds relevant resources and suggests improvements.",
                        "Finally, the Technical Writer prepares comprehensive documentation.",
                        "Deliver a final report containing the optimized code, test results, research insights, and documentation."
                    ],
                    markdown=True,
                )

                # Step 1: Generate code
                dev_response = developer_agent.run(f"Write Python code for: {task_request}")
                generated_code = dev_response.content
                
                # Step 2: Test the code
                test_response = tester_agent.run(f"Test the following Python code:\n{generated_code}")
                test_results = test_response.content
                
                # Step 3: Conduct research
                research_response = research_agent.run(f"Research best practices for:\n{generated_code}")
                research_findings = research_response.content
                
                # Step 4: Create documentation
                doc_response = documentation_agent.run(f"Document the following Python code:\n{generated_code}\n\nTest Results:\n{test_results}\n\nResearch Findings:\n{research_findings}")
                documentation = doc_response.content

                st.subheader("Final Optimized Code")
                st.code(generated_code, language='python')
                
                st.subheader("Test Results")
                st.text(test_results)
                
                st.subheader("Research Insights")
                st.text(research_findings)
                
                st.subheader("Documentation")
                st.text(documentation)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Enter a task request and API key, then click 'Execute Task' to start.")
