import os
from my_logger import logged
import xml.etree.ElementTree as ET


class FileNotFound(OSError):
    pass
class FileCorrupted(Exception):
    pass
"""
Сustom exception
"""

class WorkWithFile:
    """
    Class to manage XML file operations including reading, writing, and appending.
    """

    def __init__(self, file_name):
        """
        Initialize the WorkWithFile instance.
        Checks if the file exists and prompts the user to start the file manager.
        """
        if not os.path.exists(file_name):
            raise FileNotFound(f"File '{file_name}' not found!")
        else:
            self.file_name = file_name
        print('Do you want to continue working with the file? Yes/No')
        inpt = input().lower()
        if inpt == 'yes':
            self.file_manager()
        elif inpt == 'no':
            pass
        else:
            print('You entered something incorrect.')

    def file_manager(self):
        """
        Main loop for handling user commands to read, write, or append to the file.
        """
        command = ''
        while True:
            print('Write what exactly you want to do with the file: read/write/append or exit')
            command = input().lower()
            if command == 'exit':
                print('Work completed.')
                break
            try:
                if command == 'read':
                    print('Reading file...')
                    print(self.file_read())
                elif command == 'write':
                    self.file_write()
                elif command == 'append':
                    self.file_append()
                else:
                    print('You entered something incorrect. Try again')
            except FileCorrupted:
                pass

    @logged(FileCorrupted, mode="console")
    def file_read(self):
        """
        Reads the content of the XML file.
        """
        try:
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            return "\n".join([elem.text for elem in root.findall('line') if elem.text])
        except Exception as e:
            raise FileCorrupted(f"Failed to read XML file. Details: {e}")

    @logged(FileCorrupted, mode="file")
    def file_write(self):
        """
        Overwrites the XML file with new content provided by the user.
        Prompts the user for input and saves it into a new XML structure.
        """
        print('Warning! This is a file overwrite, all content will be lost. Continue? Yes/No')
        inpt = input().lower()
        if inpt == 'yes':
            print('Enter text (for a new line write \\n ):')
            data = input().replace(r'\n', '\n')
            try:
                root = ET.Element("data")
                lines = data.split('\n')
                for line in lines:
                    ET.SubElement(root, "line").text = line
                tree = ET.ElementTree(root)
                tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
            except Exception as e:
                raise FileCorrupted(f"Failed to write to XML file. Details: {e}")
        elif inpt == 'no':
            pass
        else:
            print('You entered something incorrect. Your answer is counted as No')

    @logged(FileCorrupted, mode="file")
    def file_append(self):
        """
        Appends new content to the existing XML file.
        Allows the user to choose between appending to the current line or starting a new one.
        """
        print('Do you want to continue writing from the current line or move to the next? This/Next')
        control = 0
        start = ""
        while control != 1:
            inpt = input().lower()
            if inpt == 'this':
                start = ""
                control = 1
            elif inpt == 'next':
                start = "\n"
                control = 1
            else:
                print('You entered something incorrect. Try again')
        print('Enter text (for a new line write \\n ):')
        data = input().replace(r'\n', '\n')
        try:
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            full_text = start + data
            lines = full_text.strip().split('\n')

            for line in lines:
                if line:
                    ET.SubElement(root, "line").text = line
            tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            raise FileCorrupted(f"Failed to append to XML file. Details: {e}")


if __name__ == "__main__":
    try:
        app = WorkWithFile(r"C:\Users\matvi\PycharmProjects\PythonProject1\Data\text.xml")
    except FileNotFound as error:
        print(f"Critical start error: {error}")
    except FileCorrupted as error:
        print(f"File error: {error}")