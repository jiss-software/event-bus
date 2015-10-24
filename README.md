Event Bus Service
-----------------

Install:

    virtualenv env
    source env/bin/activate
    python setup.py install

Run:

    source env/bin/activate
    python server.py &


Data Structure
==============

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
