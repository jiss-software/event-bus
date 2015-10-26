Event Bus Service
=================

Install:

    virtualenv env
    source env/bin/activate
    python setup.py install

Run:

    source env/bin/activate
    python server.py &

Default port 33002.

Requests
--------

    GET /events/<CONTEXT>/<CHANNEL>

Получить все элементы.

    GET /events/<CONTEXT>/<CHANNEL>?start=<timestamp>

Список событий начиная с выбраного момента.

    GET /events/<CONTEXT>/<CHANNEL>?peek=<cursor>

Получить следующий элемент после идентификатора курсора.  

    POST /events/<CONTEXT>/<CHANNEL>

`X-EVENT-ISSUER=<ISSUER>` - объязательный заголовок

Опубликовать событие. В теле высылается исключительно PAYLOAD данные в виде словаря.

Data Structure
--------------

    {
    	"issuer": "JERPi",
    	"context": "mkp", 
    	"channel": "INVOICE", 
    	"timestamp": 1444900471,
    
    	"payload": {
    		... any data ...
    	}
    }

* issuer -  система которая произвела публикацию события
* context - если система поддерживает разделение по контекстам или сайтам то идентификатор данного контекста.
* channel - канал публикации, другими словами тип события
* timestamp - время регистрации события, на шине (назначаеться автоматически)
* payload - набор данных для хранения в базе 

Test calls from command line
----------------------------

Register new event

    curl --data '{"x": 1, "y": "test"}' -X POST -H 'X-JISS-ISSUER: TEST' 127.0.0.1:33002/events/context/CHANNEL
    
Read events

    curl -X POST 127.0.0.1:33002/events/context/CHANNEL
    curl -X POST 127.0.0.1:33002/events/context/CHANNEL?start=123
    curl -X POST 127.0.0.1:33002/events/context/CHANNEL?peek=2

Замечания
---------

Механизм реакций будет основан на внешних компонентах. 

Планируется использовать по меньшей мере одного общего компонента используемого для всех. В его задачи будет входить отслеживать события и сверять их со своей базой данных для рассылки писем. 

Иные компоненты могут следить за событиями периодически спрашивая сервер выборкой с использованием peek при этом в распределённой среде необходимо записывать указатель на текущее события.

Впрочем на данный момент подробное описание метода параллельной работы двух экземпляров одного компонента по обработки событий, не описывается, так как в текущей  архитектуре он избыточен (мы допускаем оповещение пользователя с опозданием.) 
