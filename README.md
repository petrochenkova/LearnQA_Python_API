### Установка виртуального окружения и зависимостей ###
 * Установка виртуальной среды: python3 -m venv venv
 * Активация виртуальный среды: source venv/bin/activate
 * Обновить pip: pip3 install --upgrade pip
 * Утановка зависимостий из файла requirments.txt: pip3 install -r requirements.txt
 * Отключение виртуальной среды: deactivate

### Обновление файла requirements.txt
Если в момент работы с проектом вы добавляете новую библиотеку, необходимо обновить файл requirements.txt
* Команда для обновления файла: pip freeze > requirements.txt
