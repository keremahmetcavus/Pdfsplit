import PyPDF4

import os

import glob
def split_pdf(input_file, output_prefix, output_folder):
    # Open pdf file 
    with open(input_file, 'rb') as file:
        #Read pdf file
        pdf_reader = PyPDF4.PdfFileReader(file)
        #Create empty writer
        pdf_writer = PyPDF4.PdfFileWriter()
        #Loop Through all pages
        for page_number in range(pdf_reader.getNumPages()):
            # Get the current page number
            page = pdf_reader.getPage(page_number)
            
            # Get the page rotation angle 
            rotation = page.get('/Rotate', 0)
            
            # Calculate the width and height of the page
            width = page.mediaBox.getWidth()
            height = page.mediaBox.getHeight()
            
            # Calculate the width of each piece
            piece_height = height / 3
            
            #Loop into 3 equal page
            for i in range(2,-1,-1):
                #Create empty piece with required width and height
                piece = PyPDF4.pdf.PageObject.createBlankPage(None, width, piece_height)
                
                #Cut and import into piece with piece height
                piece.mergeRotatedScaledTranslatedPage(page, rotation, 1, 0, -i * piece_height)
                
                # Add the piece to the PDF writer
                pdf_writer.addPage(piece)
            
        # Save the pieces to separate PDF files
        output_file = f'{output_prefix}.pdf'
        output_path = os.path.join(output_folder, output_file)
        with open(output_path, 'wb') as output:
            pdf_writer.write(output)
            print(f'Saved {output_file}')

#Get Current py path
path_current = os.path.dirname(__file__)
#Get Output path which cropped files will export
path_output = f'{path_current}/output'
#Get Input path which files going to get from
path_input = f'{path_current}/input'
                
#Get All files in input which are pdf
pdf_files = glob.glob(os.path.join(path_input, '*.pdf'))
#Loop through all file in input folder
for pdf_file in pdf_files:
    #Get file path 
    file_name = os.path.basename(pdf_file)
    file_path = f'{path_input}\{file_name}'
    
    #Create output name
    output_prefix = f'{os.path.splitext(file_name)[0]}_output'
    
    #Split pdf function
    split_pdf(file_path,output_prefix,path_output)