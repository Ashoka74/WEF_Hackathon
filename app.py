import gradio as gr
import os
import pandas as pd
from openai import OpenAI
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def upload_file(xsl_file):
    if xsl_file is None:
        return "Please upload a file first"
    try:
        df = pd.read_excel(xsl_file.name)
        return df
    except Exception as e:
        return f"Error reading file: {str(e)}"
       
def process_query(xsl_file, query):
    # Process the file and generate responses
    logger.info("Starting query processing")
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    model = "gpt-4o"
    responses = {}

    # Convert DataFrame to JSON
    if xsl_file is not None:
        logger.info(f"Reading Excel file: {xsl_file.name}")
        try:
            df = pd.read_excel(xsl_file.name)
            json_data = df.to_json(orient='records')
            responses['data'] = json_data
            logger.info("Successfully converted Excel to JSON")
        except Exception as e:
            logger.error(f"Error converting Excel to JSON: {str(e)}")
            raise
    
    try:
        logger.info("Sending request to OpenAI API")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": os.getenv('system_prompt')},
                {"role": "user", "content": f"Examples: {os.getenv('context_prompt')}\n\n Data: {json_data}\n\n Query: {query} \n\n INSTRUCTIONS: You must absolutely return the sql between <SQL></SQL> and the XML between <XML></XML>. If the user query is incorrect, add the disclaimer between the SQL/XML tags as well. \n\n Output:"}
            ]
        )
            
        responses['query'] = query
        responses['response'] = response.choices[0].message.content
        logger.info(f"Raw response content: {response.choices[0].message.content}")
        
        # Add validation before splitting
        if '<SQL>' not in response.choices[0].message.content or '<XML>' not in response.choices[0].message.content:
            logger.error("Response missing SQL or XML tags")
            raise ValueError("Response format invalid - missing SQL or XML tags")
            
        try:
            responses['SQL'] = response.choices[0].message.content.split('<SQL>')[1].split('</SQL>')[0]
            logger.info("Successfully extracted SQL query")
        except IndexError as e:
            logger.error(f"Error extracting SQL query: {str(e)}")
            responses['SQL'] = "Error extracting SQL query"
            
        try:
            responses['XML'] = response.choices[0].message.content.split('<XML>')[1].split('</XML>')[0]
            logger.info("Successfully extracted XML query") 
        except IndexError as e:
            logger.error(f"Error extracting XML query: {str(e)}")
            responses['XML'] = "Error extracting XML query"
            
        logger.info("Successfully processed OpenAI response")

    except Exception as e:
        print(f"Error occurred: {e}")
        responses['error'] = str(e)

    try:
        df = pd.read_excel(xsl_file.name)
        return responses['SQL'], responses['XML'], responses
    except Exception as e:
        return f"Error reading file: {str(e)}", None, None

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# WEF Hackathon Demo")

    
    # Top section - XLS file upload
    with gr.Row():
        xsl_upload = gr.File(
            label="Upload XLS File",
            file_types=[".xls"]
        )
    
    # Display section for uploaded data
    data_display = gr.Dataframe(
        label="Uploaded Data Preview",
        interactive=False,
        wrap=True
    )
    
    # Bottom section - 3 columns
    with gr.Row():
        # First column - Natural language input
        with gr.Column():
            query_input = gr.Textbox(
                label="Natural Language Query",
                placeholder="Enter your query here...",
                lines=5
            )
        
        # Second column - SQL output
        with gr.Column():
            sql_output = gr.Textbox(
                label="LLM SQL Response",
                interactive=False
            )
        
        # Third column - XML output
        with gr.Column():
            xml_output = gr.Textbox(
                label="LLM XML Response",
                interactive=False
            )
    
    # Submit button
    submit_btn = gr.Button("Process Query")
    cached_examples = os.getenv('examples')
    examples = gr.Examples(
        examples=[
    '''Join LFA1 (general vendor data) with LFB1 (company code data) by matching LIFNR. Filter on a specific vendor (e.g., LIFNR = "100000"), then retrieve the vendor’s number, name, company code, payment block, and payment terms.''',
    '''Match LFA1’s address number (ADRNR) to ADR6’s address reference (ADDRNUMBER) to get e-mail data. For a given vendor (e.g., LIFNR = "100000"), select the vendor’s number, name, e-mail address, and validity dates.''',
    '''Join LFM1 and LFM2 on both vendor number (LIFNR) and purchasing organization (EKORG). Retrieve data like the vendor’s credit group and blocking status for a given vendor (LIFNR) and purchasing org (EKORG).'''
    '''Link LFBK (vendor’s bank details) to BNKA (bank master) by matching bank key and account (e.g., LFBK.BANKL = BNKA.BANKL and LFBK.BANKN = BNKA.BANKN). For a vendor (LIFNR = "100000"), return their bank account plus the bank’s name and country.''',
    '''Join BSIK (open vendor items) with LFA1 (vendor data) using LIFNR. Filter on a specific vendor and list open items (document number, amount) alongside the vendor’s name.''',
    '''Combine CDHDR/CDPOS (change documents) with LFA1 (vendors). Match CDHDR.OBJECTID = LFA1.LIFNR (and ensure CDHDR.OBJECTCLAS = "LFA1"), then join CDHDR.CHANGENR = CDPOS.CHANGENR to display what fields changed, along with old/new values, for a specific vendor.'''
        ],
        inputs=query_input
    )

    xsl_upload.change(fn=upload_file,
                      inputs=[xsl_upload],
                      outputs=data_display)
    
    # Handle submission
    submit_btn.click(
        fn=process_query,
        inputs=[xsl_upload, query_input],
        outputs=[sql_output, xml_output]
    )

if __name__ == "__main__":
    demo.launch() 