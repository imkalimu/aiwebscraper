# Import necessary classes from LangChain for LLM interaction and prompt template creation
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Define a prompt template for extracting specific information from text
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the OllamaLLM model with "llama3" or any LLM
model = OllamaLLM(model="llama3")

def parse_with_ollama(dom_chunks, parse_description):
    # Create a prompt using the defined template
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create a chain that connects the prompt with the model for processing
    chain = prompt | model

    # Initialize a list to hold the parsed results from each chunk
    parsed_results = []

    # Loop through each chunk of DOM content, using enumerate for index tracking
    for i, chunk in enumerate(dom_chunks, start=1):
        # Invoke the chain with the current chunk and the parse description
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        
        # Print the status of the parsing operation
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        
        # Append the response to the parsed_results list
        parsed_results.append(response)

    # Join the parsed results into a single string separated by newlines and return
    return "\n".join(parsed_results)
