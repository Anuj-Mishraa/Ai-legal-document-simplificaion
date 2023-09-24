import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os
from langchain.document_loaders import PyPDFLoader
import docx
import tempfile

def generate_response(uploaded_file,query_text):
    # Split documents into chunks
    template = """you are given text from a document
    given text:
    {text}
    now anser my question
{query_text}"""
    prompt = PromptTemplate(input_variables=['text',"query_text"],template=template)
    prompt = prompt.format(text=uploaded_file,query_text=query_text)
    # get a chat completion from the formatted messages
    chat = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
    response = chat(prompt)
    return response
# Define function to get document content from uploaded file
def get_document_content(uploaded_file):
    if uploaded_file is not None:
        # Create a temporary directory to save the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())

            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            chapter = ""
            for page in pages:
                chapter += str(page)
        return chapter
    return None

# Define function to simplify legal document using AI
def AI_call(legal_doc):
    template='''
    You are a helpfull assistant in  simplifying the provided legal documents in a user understandable language
    Simplify the text of provided EMPLOYMENT AGREEMENT legal document in a simplify and common understandable languagee in a legal format.
    Note: The response should be complete. and should cover the following points.
    1. Complete details of user and parties envolved.
    2. BY AND BETWEEN
    3. Employment: 
    4. Position Title: 
    5. Compensation
    6. Vacation: 
    7. Vacation: 
    8. Performance Reviews
    9. Obligations of the Employee
    10.	Intellectual Property Assignment
    11.	Confidentiality
    12.	Remedies
    13.	Termination
    14. Laws
    15.	Successors: 
    16.	Entire Agreement: 
    17. provided Context:
    18.	Severability: 
    IN WITNESS WHEREOF 

    The Given document is :-
    {text}'''
    prompt = PromptTemplate(input_variables=['text'],template=template)
    prompt = prompt.format(text=legal_doc)
    # get a chat completion from the formatted messages
    chat = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
    response = chat(prompt)
    return response
def main():
    st.title("Legal Document Simplification App")
    tab1, tab2, tab3 = st.tabs(["Home", "Samples Of Legal Documents", "Simplify Your Document"])
    with tab1:
        st.markdown(
            """
# Legal Document Simplification

## Project Overview

**Project Title**: Legal Document Simplification

**Description**: We are developing an AI-based web application using Python, specifically utilizing the Langchian framework. This innovative platform aims to simplify complex legal documents and make them accessible to a wide range of users. The project is divided into several key features:

1. **Document Simplification**: Our AI-driven approach simplifies legal language in both Hindi and English. We generate simplified versions of provided documents using advanced language processing technologies such as Langchain and OpenAI.

2. **Customization**: Our platform includes an editor that allows users to modify the content of generated simplified documents or create fresh ones. We've even built a separate ReactJS application to provide powerful editing functionalities that seamlessly integrate with the initial app.

3. **Verification of Modifications through Legal Laws**: We've implemented a Python program, or AI-based system, that verifies the content of AI-generated documents or customized documents against relevant legal laws and regulations. If any mistakes are detected, an alert is generated to ensure compliance and accuracy.

4. **Expert Talk and Review**: After digital verification, our platform enables expert review of documents through a user-friendly interface. Users can engage with legal experts through chat messages or video messages, creating a robust feedback loop.

5. **Document Specific Bot**: We've developed an AI-based interface that allows users to interact with provided documents directly. This feature leverages Langchain and OpenAI technologies to provide an engaging and informative experience.

6. **System Bot**: Our platform features an AI-based interface that guides users in using the app effectively and addresses any issues they may encounter, enhancing the overall user experience.

## Technical Feasibility

### AI Algorithms and NLP:
- Feasibility: AI and NLP technologies have advanced significantly, making it feasible to simplify legal language.
- Considerations: Access to legal datasets and AI model expertise is crucial.

### Multilingual Support:
- Feasibility: Feasible with robust translation and language processing capabilities.
- Considerations: Accuracy in translations and regional variations are important factors.

### Voice Assistance:
- Feasibility: Feasible using speech recognition technology.
- Considerations: Accuracy in responses and understanding legal queries is critical.

### User Interface and Experience:
- Feasibility: Feasible with modern web and mobile app development technologies.
- Considerations: User testing for ease of use and accessibility is essential.

### Data Security and Privacy:
- Feasibility: Implementing data security measures is technically feasible.
- Considerations: Compliance with data protection regulations is mandatory.

### Scalability:
- Feasibility: Achievable with cloud-based infrastructure and proper architectural design.
- Considerations: Cloud-based infrastructure and performance monitoring are key.

### Legal Compliance:
- Feasibility: Ensuring legal compliance is technically feasible.
- Considerations: Collaboration with legal experts for updates is essential.

### Customer Support and Feedback:
- Feasibility: Implementing customer support and feedback mechanisms is technically straightforward.
- Considerations: Timely response to user inquiries is critical.

### Integration with Legal Databases:
- Feasibility: Integrating with existing legal databases is feasible through APIs and data extraction techniques.
- Considerations: APIs, data accuracy, and compatibility with the platform are important."""
        )
    with tab3:
        key = st.text_input("Enter OpenAi API KEY: ")
        if key:
            os.environ["OPENAI_API_KEY"] = key
            st.write("Upload a legal document, and we will simplify it for you.")
            # Sidebar container for the query bot chat interface
            st.sidebar.title("Query Bot Chat Interface")
            query = st.sidebar.text_input("Ask a question about the document:")
            # Add a "Submit Query" button
            submit_query = st.sidebar.button("Submit Query")
            uploaded_file = st.file_uploader("Upload ", type=["pdf", "docx"])
            process_button = st.button("Process Document Further")
            if uploaded_file is not None:
                content = get_document_content(uploaded_file)
                if submit_query:
                    if query:
                        st.sidebar.write(generate_response(content[:5440],query))
                if process_button:
                    if content:
                        # Process the document if the button is clicked
                        
                        sim_doc = AI_call(content)
                        # Display the further processed document
                        st.subheader("Further Processed Document")
                        st.write(sim_doc)
                        
                    
                        # Create a temporary directory to save the simplified document
                        with tempfile.TemporaryDirectory() as temp_dir:
                            temp_file_path = os.path.join(temp_dir, "generated_document.docx")
                            
                            # Create a new document and add the simplified content
                            doc = docx.Document()
                            doc.add_paragraph(sim_doc)
                            
                            # Save the document to the temporary file
                            doc.save(temp_file_path)
                            
                            # Provide a link to download the file manually
                            with open(temp_file_path, "rb") as file:
                                doc_bytes = file.read()
                                st.download_button(
                                    label="Download Simplified Document (docx)",
                                    data=doc_bytes,
                                    key="download_sim_doc",
                                    file_name="generated_document.docx",
                                )
        else:
            st.warning('Please Enter OpenAI API key', icon="⚠️")
    
if __name__ == "__main__":
    main()
