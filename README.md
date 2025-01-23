
<a href="https://huggingface.co/spaces/Ashoka74/WEF_Hackathon_Group2/tree/main">
<img alt="Spaces" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue">
</a>




# WEF Hackathon - Natural Language to SQL/XML Converter

A powerful web application that converts natural language queries into SQL and XML queries, specifically designed for SAP database structures. Built with Gradio and OpenAI's GPT-4, this tool helps users generate complex SQL and XML queries without needing to know the exact syntax.

## Features

- 🔄 Convert natural language to SQL and XML queries
- 📊 Upload and preview Excel files
- 💡 Pre-built example queries
- 🎯 Specialized for SAP database structures
- 📝 Detailed logging system
- 🚀 User-friendly Gradio interface

## Prerequisites

- Python 3.8+
- OpenAI API key
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd WEF_Hackathon
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
system_prompt=your_system_prompt
context_prompt=your_context_prompt
examples={
    'example_1': 'Your first example query',
    'example_2': 'Your second example query',
    ...
}
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to the local URL provided by Gradio (typically `http://localhost:7860`)

3. Upload your Excel file containing the data structure

4. Enter your query in natural language or select from the example queries

5. Click "Process Query" to generate SQL and XML queries

## Example Queries

The application comes with several pre-built example queries for common SAP database operations:

1. Vendor data joining with company code data
2. Email data retrieval using address references
3. Purchasing organization data queries
4. Bank details matching
5. Open vendor items listing
6. Change document tracking

## File Structure

```
WEF_Hackathon/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
└── app.log            # Application logs
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `system_prompt`: System prompt for the GPT model
- `context_prompt`: Context examples for the model
- `examples`: Dictionary of example queries

## Logging

The application maintains detailed logs in `app.log`, tracking:
- Query processing
- File operations
- API responses
- Error messages

## Error Handling

The application includes robust error handling for:
- File upload issues
- API communication errors
- Query parsing problems
- Invalid response formats

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Gradio team for the web interface framework
- SAP for database structure references
