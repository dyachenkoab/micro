# micro  
## Микросервис для электронного магазина  
*Модель/cущности*:  
* Товар - отвечает за товар на складе, например - телефон такой-то марки от такого-то производителя.  

*Поля*:
* идентификатор (ID)  
* название  
* описание  
* параметры: массив пар ключ/значение  

Сущности хранятся в MongoDB на localhost:27017 (можно запускать командой docker run -d -p 27017:27017 mongo)  

*REST API методы*:  
* Создать новый товар  
* Получить список названий товаров, с возможностью фильтрации по:
    * названию
    * выбранному параметру и его значению
* Получить детали товара по ID
  
Методы принимают JSON на входе и отдают JSON на выходе.  

*Необходимые шаги для инсталляции и запуска:*  
`git clone https://github.com/dyachenkoab/micro.git`  
`cd micro`  
`python3 -m venv env`  
`source env/bin/activate`  
`pip install -r requirements.txt`  
`./app.py`  

**Сurl команды с нужными параметрами для прохождения тестового сценария**:  

*Создать товар*:  
* curl -X POST localhost:5000/add_one -H 'Content-Type: application/json' -d '{ "_id": "1", "name": "Nokia", "description": "simple phone", "parameters":{"part_number":2938, "color": "green"}}'
* curl -X POST localhost:5000/add_one -H 'Content-Type: application/json' -d '{ "_id": "2", "name": "Alcatel", "description": "simple phone", "parameters":{"part_number":7364, "color": "green"}}'
* curl -X POST localhost:5000/add_one -H 'Content-Type: application/json' -d '{ "_id": "3", "name": "Nokia", "description": "simple phone", "parameters":{"part_number":9282, "color": "orange"}}'

*Найти по параметру*:  
* curl -X POST localhost:5000/filter -H 'Content-Type: application/json' -d '{"part_number": 2938}'  
* curl -X POST localhost:5000/filter -H 'Content-Type: application/json' -d '{"color": "green"}'  
* curl -X POST localhost:5000/filter -H 'Content-Type: application/json' -d '{"name": "Nokia", "color": "orange"}'  

*Получить детали по id*:
* curl -X POST localhost:5000/id -H 'Content-Type: application/json' -d '{"_id": "3"}'
