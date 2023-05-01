import uuid
from faker import Faker
import random
import docx
from docx import Document
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
    doc = Document(doc_path)

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
        table = doc.add_table(rows=rows+1, cols=cols)

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
        hdr_cells[0].text = 'Txn Date'
        hdr_cells[1].text = 'Description'
        hdr_cells[2].text = 'Ref No./Cheque No.'
        hdr_cells[3].text = 'Debit'
        hdr_cells[4].text = 'Credit'
        hdr_cells[5].text = 'Balance'

        # Populate table with transaction data
        fake = Faker()
        balance = 4000
        total_debit = 0
        total_credit = 0
        for i in range(1, rows):
            row_cells = table.rows[i].cells
            txn_date = fake.date_between(start_date='-1y', end_date='today').strftime('%d %b %Y')
            row_cells[0].text = txn_date
            row_cells[1].text = fake.sentence(nb_words=5, variable_nb_words=True)
            row_cells[2].text = str(uuid.UUID(fake.uuid4()).hex)[:8]
            is_debit = random.choice([True, False])
            if is_debit:
                debit = random.randint(100, 5000)
                credit = 0
            else:
                debit = 0
                credit = random.randint(100, 5000)
            balance = balance + credit - debit
            if debit > 0:
                row_cells[3].text = f"{debit:,}"
            else:
                row_cells[3].text = ''
            if credit > 0:
                row_cells[4].text = f"{credit:,}"
            else:
                row_cells[4].text = ''
            if balance >= 0:
                row_cells[5].text = f"{balance:,}"
            else:
                row_cells[5].text = ''

            total_debit += debit
            total_credit += credit

        # Add final row with total debit, total credit, and final balance
        row_cells = table.add_row().cells
        row_cells[1].text = "TOTAL"
        row_cells[3].text = f"{total_debit:,}"
        row_cells[4].text = f"{total_credit:,}"
        if balance >= 0:
            row_cells[5].text = f"{balance:,}"
        else:
            row_cells[5].text = ''


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
        docx_output_path = os.path.join(output_dir, f"generated_doc_{input_yaml_data['file_name']}_{input_yaml_data['action']}_{index+1}.docx")
        pdf_output_path = os.path.join(output_dir, f"generated_doc_{input_yaml_data['file_name']}_{input_yaml_data['action']}_{index+1}.pdf")

        try:
            # Save the document as a docx file
            doc.save(docx_output_path)
            # Add table to the document
            add_table_to_doc(docx_output_path,'Transaction Table', 10, 6) # Example values for 10 rows and 6 columns

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
    

