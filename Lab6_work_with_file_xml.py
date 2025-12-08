import os
from my_logger import logged
import xml.etree.ElementTree as ET


class FileNotFound(Exception):
    pass
class FileCorrupted(Exception):
    pass


class WorkWithFile:
    def __init__(self, file_name):
        if not os.path.exists(file_name):
            raise FileNotFound(f"Файл '{file_name}' не знайдено!")
        else:
            self.file_name = file_name
        print('Бажаєте продовжити роботу з файлом? Yes/No')
        inpt = input().lower()
        if inpt == 'yes':
            self.file_manager()
        elif inpt == 'no':
            pass
        else:
            print('Ви ввели щось не коректне.')

    def file_manager(self):
        command = ''
        while True:
            print('Напишіть, що саме ви хочете зробити з файлом: read/write/append або exit')
            command = input().lower()
            if command == 'exit':
                print('Робота завершена.')
                break
            try:
                if command == 'read':
                    print('Читаємо файл...')
                    print(self.file_read())
                elif command == 'write':
                    self.file_write()
                elif command == 'append':
                    self.file_append()
                else:
                    print('Ви ввели щось не коректне. Спробуйте ще раз')
            except FileCorrupted:
                pass

    @logged(FileCorrupted, mode="console")
    def file_read(self):
        try:
            tree = ET.parse(self.file_name)
            root = tree.getroot()
            return "\n".join([elem.text for elem in root.findall('line') if elem.text])
        except Exception as e:
            raise FileCorrupted(f"Не вдалося прочитати XML файл. Деталі: {e}")

    @logged(FileCorrupted, mode="file")
    def file_write(self):
        print('Увага! Це перезапис файлу, весь вміст буде втрачено. Продовжити? Yes/No')
        inpt = input().lower()
        if inpt == 'yes':
            print('Введіть текст (для нового рядка пишіть \\n ):')
            data = input().replace(r'\n', '\n')
            try:
                root = ET.Element("data")
                lines = data.split('\n')
                for line in lines:
                    ET.SubElement(root, "line").text = line
                tree = ET.ElementTree(root)
                tree.write(self.file_name, encoding="utf-8", xml_declaration=True)
            except Exception as e:
                raise FileCorrupted(f"Не вдалося записати в XML файл. Деталі: {e}")
        elif inpt == 'no':
            pass
        else:
            print('Ви ввели щось не коректне. Ваша відповідь зарахована як No')

    @logged(FileCorrupted, mode="file")
    def file_append(self):
        print('Бажаєте продовжити запис з поточного рядка чи перейти на наступний? This/Next')
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
                print('Ви ввели щось не коректне. Спробуйте ще раз')
        print('Введіть текст (для нового рядка пишіть \\n ):')
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
            raise FileCorrupted(f"Не вдалося дописати в XML файл. Деталі: {e}")


if __name__ == "__main__":
    try:
        app = WorkWithFile(r"C:\Users\matvi\PycharmProjects\PythonProject1\Data\text.xml")
    except FileNotFound as error:
        print(f"Критична помилка старту: {error}")
    except FileCorrupted as error:
        print(f"Помилка файлу: {error}")