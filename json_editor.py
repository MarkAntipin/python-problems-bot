import json


def add_question_text_and_code_markup_to_json(file, newfile):
    with open(file, encoding='utf-8') as f:
        file_content = f.read()
        templates = json.loads(file_content)  # json-файл в виде списка словарей
    for template in templates:  # итерируемся по списку словарей, берём словарь
        a = template.pop('text_markup')  # из словаря убираем ключ 'text_markup' и заводим его значение в переменную
        b = a.split(sep='*')  # делим его на элементы по знаку звёздочки; 1й элем - пустая строка, 2й - текст вопроса,
        # 3й элем - код вопроса
        if len(b) > 2:  # в обычном случае для данного файла после деления значения образуется список с 3 элементами
            template['question_text_markup'] = b[1]  # заносим текст вопроса в соответствующий ключ
            template['question_code_markup'] = b[2]  # заносим код вопроса в соответствующий ключ
        elif len(b) == 2:  # на случай, если вопрос без прилагающегося кода
            template['question_text_markup'] = b[1]  # заносим только текст вопроса в соответствующий ключ
        elif len(b) == 1:  # Эта заглушка нужна для вопроса 122, где звёздочек нет, и делить приходится по "?"
            # Если привести json к единообразному виду, то она, в общем-то, и не нужна.
            b = b[0].split(sep='?')
            template['question_text_markup'] = b[0] + '?'  # заносим текст вопроса, возвращаем "?", по которому делили
            template['question_code_markup'] = b[1]  # заносим код вопроса

    with open(newfile, 'w', encoding='utf-8') as f:
        json.dump(templates, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    file = input("Введите путь к редактируемому файлу: ")
    newfile = input("Введите путь к новому файлу и его название: ")
    add_question_text_and_code_markup_to_json(file, newfile)
