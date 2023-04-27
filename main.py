import uuid
from faker import Faker
import random
import docx
from datetime import datetime
from docxtpl import DocxTemplate
from docx.shared import Cm
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx2pdf import convert
import pandas as pd
import yaml
import pprint
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


def add_table_to_doc(doc_path, placeholder_text, rows, cols):
    # Open the docx file
    doc = docx.Document(doc_path)

    # Before creating the table
    print(f"Number of tables before: {len(doc.tables)}")

    # Find the placeholder
    placeholder = None
    for paragraph in doc.paragraphs:
        if placeholder_text in paragraph.text:
            placeholder = paragraph
            break

    # If placeholder is found, replace it with the table
    if placeholder:
        # Remove the placeholder paragraph
        p = placeholder._element
        p.getparent().remove(p)
        p._p = p._element = None

        # Insert an empty paragraph before the table
        placeholder.insert_paragraph_before('Tomcat')

        # Create the table
        table = doc.add_table(rows=rows, cols=cols)

        # Print the text of the paragraph before the table
        print(table._element.getprevious().text)

        # After creating the table
        print(f"Number of tables after: {len(doc.tables)}")

        # Set table alignment to center
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Set column widths
        col_widths = [Cm(2), Cm(3), Cm(4), Cm(2), Cm(2), Cm(3)]
        for i, width in enumerate(col_widths):
            table.columns[i].width = width

        # Set table header row
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Date'
        hdr_cells[1].text = 'Referal code'
        hdr_cells[2].text = 'Mode of transaction'
        hdr_cells[3].text = 'Debit'
        hdr_cells[4].text = 'Credit'
        hdr_cells[5].text = 'Total balance'

        # Populate table with random data
        fake = Faker()
        for i in range(1, rows):
            row_cells = table.rows[i].cells
            row_cells[0].text = fake.date_this_month().strftime('%d-%m-%Y')
            row_cells[1].text = str(uuid.UUID(fake.uuid4()).hex)[:8]
            row_cells[2].text = random.choice(['Online', 'Offline'])
            row_cells[3].text = str(random.randint(1, 10000))
            row_cells[4].text = str(random.randint(1, 10000))
            row_cells[5].text = str(random.randint(1, 100000))

        # Add spacing after the table
        doc.add_paragraph(' ')

        # Save the modified docx file
        doc.save(doc_path)

        print(f"Table successfully added to {doc_path}!")
    else:
        print(f"Placeholder '{placeholder_text}' not found in {doc_path}!")

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
            'today_date': datetime.today().strftime("%d %b, %Y"),
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
            # Add table to the document
            add_table_to_doc(docx_output_path,'abcxyz', 10, 6) # Example values for 10 rows and 6 columns

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
    

