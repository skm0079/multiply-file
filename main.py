import pandas as pd
from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
import yaml
import os


def convert_docx_to_pdf(input_file_path, output_file_path):
    """
    Converts a docx file to pdf.

    Args:
        input_file_path (str): Path to the input docx file.
        output_file_path (str): Path to the output pdf file.

    Raises:
        ValueError: If the input file does not exist.
        RuntimeError: If the conversion fails or the output file is not created.

    Returns:
        None
    """
    # Check if input file exists
    if not os.path.isfile(input_file_path):
        raise ValueError("Input file does not exist.")

    try:
        # Convert docx to pdf
        convert(input_file_path, output_file_path)
    except Exception as e:
        raise RuntimeError("Failed to convert docx to pdf.") from e

    # Check if output file exists
    if not os.path.isfile(output_file_path):
        raise RuntimeError("Failed to create pdf output file.")


def generate_document_and_pdf(template_path, data, output_dir):
    """
    Generates a document and a pdf for each row in the given data.

    Args:
        template_path (str): Path to the document template.
        data (pd.DataFrame): Pandas DataFrame containing the data for the documents.
        output_dir (str): Path to the output directory.

    Raises:
        ValueError: If the input template docx file does not exist.
        RuntimeError: If the document or pdf generation fails or the output files are not created.

    Returns:
        None
    """
    # Check if template file exists
    if not os.path.isfile(template_path):
        raise ValueError("Template docx file does not exist.")

    for index, row in data.iterrows():
        # Define context for the document
        context = {
            'account_holder_name': row['account_holder_name'],
            'address': row['address'],
            'ifsc_code': row['ifsc_code'],
            'micr_code': row['micr_code'],
            'branch_name': row['branch_name'],
            'account_type': row['account_type'],
            'account_number': row['account_number'],
            'opening_balance': row['opening_balance'],
            'closing_balance': row['closing_balance'],
            'debit': row['debit'],
            'credit': row['credit'],
            'total_balance': row['total_balance'],
            'today_date': datetime.today().strftime("%d %b, %Y")
        }

        # Load the document template and render it with the context
        doc = DocxTemplate(template_path)
        doc.render(context)

        # Define output file paths
        docx_output_path = os.path.join(output_dir, f"generated_doc_{input_yaml_data['file_name']}_{index}.docx")
        pdf_output_path = os.path.join(output_dir, f"generated_doc_{input_yaml_data['file_name']}_{index}.pdf")

        try:
            # Save the document as a docx file
            doc.save(docx_output_path)

            # Convert the docx file to pdf
            convert_docx_to_pdf(docx_output_path, pdf_output_path)
        except Exception as e:
            raise RuntimeError("Failed to generate document and pdf.") from e


if __name__ == '__main__':
    # Define input and output directories
    input_dir = os.getcwd()
    output_doc_dir = 'output_docs'
    output_pdf_dir = 'output_pdfs'

    # Load the config input
    with open('config/input.yaml', 'r') as file:
        input_yaml_data = yaml.safe_load(file)
    
    # Define input file paths
    template_path = os.path.join(input_dir, 'docx_templates', f"{input_yaml_data['file_name']}.docx")
    data_path = os.path.join(input_dir, 'excel_sheets', f"{input_yaml_data['file_name']}_accounts.csv")

    # Read data from CSV file
    data = pd.read_csv(data_path)

    # Generate documents and pdfs
    generate_document_and_pdf(template_path, data, output_doc_dir)

    # Convert all generated docx files to pdf
    for file_name in os.listdir(output_doc_dir):
        if file_name.endswith('.docx'):
            file_path = os.path.join(output_doc_dir, file_name)
            convert_docx_to_pdf(file_path, os.path.join(output_pdf_dir, file_name.replace('.docx', '.pdf')))

