import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import docx
import tempfile
import io
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

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
# def trans_late(text):
#     template = """Translate the following text into Hindi
#                 {text}"""
#     prompt = PromptTemplate(input_variables=['text'],template=template)
#     prompt = prompt.format(text=text)
#     # get a chat completion from the formatted messages
#     chat = OpenAI(temperature=0, model_name='gpt-3.5-turbo')
#     response = chat(prompt)
#     return response
# Main Streamlit app
def main():
    st.title("Legal Document Simplification App")
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
    
if __name__ == "__main__":
    main()
