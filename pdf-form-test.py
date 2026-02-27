import re
from PyPDF3 import PdfFileReader
from PyPDF3.generic import ByteStringObject

def print_values():
    pdf_files = ['LaTeX_form_eforms/eforms-test_filledAdobe.pdf',
                 # eforms scheint tatsächlich nur mit Adobe zu funktionieren
                 # Fehler beim Auslesen anderer Viewer:
                 # Multiple definitions in dictionary at byte 0x3779 for key /AcroForm
                 #'LaTeX_form_eforms/eforms-test_filledFirefox.pdf',
                 #'LaTeX_form_eforms/eforms-test_filledOkular.pdf',
                 #'LaTeX_form_eforms/eforms-test_filledQpdf.pdf',

                 'LaTeX_form_hyperref/hyperref-test_filledAdobe.pdf',
                 'LaTeX_form_hyperref/hyperref-test_filledFirefox.pdf',
                 'LaTeX_form_hyperref/hyperref-test_filledOkular.pdf',
                 'LaTeX_form_hyperref/hyperref-test_filledQpdf.pdf',

                 'LaTeX_form_l3pdffield/l3pdffield-test_filledAdobe.pdf',
                 'LaTeX_form_l3pdffield/l3pdffield-test_filledFirefox.pdf',
                 'LaTeX_form_l3pdffield/l3pdffield-test_filledOkular.pdf',
                 'LaTeX_form_l3pdffield/l3pdffield-test_filledQpdf.pdf',
                 ]
    
    for file in pdf_files:
        result_lines = []
        print('File: ' + file)
        pdf_file = open(file, 'rb')
        pdf_reader = PdfFileReader(pdf_file)
        dictionary = pdf_reader.getFields()
        result_lines.append('File: ' + file + '\n\n')
        result_lines.append(param_formatter(dictionary,'info-name'))
        result_lines.append(param_formatter(dictionary,'info-number'))
        result_lines.append(param_formatter(dictionary,'info-course'))
        result_lines.append(param_formatter(dictionary,'Apples-number'))
        result_lines.append(param_formatter(dictionary,'CinemaTickets-number'))
        result_lines.append(param_formatter(dictionary,'TextAreaTest-answer'))
        result_lines.append(param_formatter(dictionary,'SliderTest-test'))
        result_lines.append(param_formatter(dictionary,'CheckboxTest-option1'))
        result_lines.append(param_formatter(dictionary,'CheckboxTest-option2'))
        result_lines.append(param_formatter(dictionary,'CheckboxTest-option3'))

        # Je nach Package und Viewer ist der Backslash
        # mal vorhanden und mal nicht, daher Abfrage von beidem
        result_lines.append(param_formatter(dictionary,'DropTest-count_'))
        result_lines.append(param_formatter(dictionary,'DropTest-count\\_'))
        
        result_lines.append(param_formatter(dictionary,'RadioButtonTest-test'))
        result_lines.append(param_formatter(dictionary,'RadioTest4-test'))
        result_lines.append(param_formatter(dictionary,'RadioTest3-test'))
        result_lines.append('\n')

        file_name = re.search(r'^.*?/(.*).pdf', file)
        if file_name:
            result_file = f'results/result-{file_name.group(1)}.txt'
            with open(result_file, "w") as result:
                result.writelines(result_lines)
                result.close()

def param_formatter(dict, param):
    param_dict = dict.get(param)
    if param_dict is None:
        return f'{param}: Not available\n'
    else:
        param_value = param_dict.get('/V')
        if param_value is None:
            return f'{param}: No value\n'
        elif isinstance(param_value, ByteStringObject):
            return f'{param}: {param_value.decode("utf-8")}\n'
        else:
            return f'{param}: {param_value}\n'

if __name__ == "__main__":
    print_values()