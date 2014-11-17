#sickbeard-newpct-rss
________

####_Obtener fichero RSS compatible con Sick Beard de la web newpct/ newpct1 dot com para descargar series y películas en Español_

Con este script obtenemos un fichero RSS que es compatible con Sick Beard a partir del que pone a nuestra disposición newpct/newpct1.

--


####Instrucciones
* descargar el fichero "newpct.py" al directorio que deseemos
* abrir el fichero con un editor de texto y modificar: 
	- con tu usuario y contraseña (ahora mismo funciona sin tener que loguearse)
	```self.__browser.form['userName'] = 'uSuArIo'```  
    ```self.__browser.form['userPass'] = 'CoNtRaSeÑa'```  
	- la siguiente línea ```filename = '/ruta-donde-quieres-descargar-los-torrents/torrents/' + nombre + '.torrent'``` poner la ruta donde queremos que deje los ficheros torrent que se va a descargar
	- la siguiente línea también: ```fichero = open('/ruta-donde-quieres-dejar-el-fichero/newpct.php', 'w')```  con la ruta donde quieres que guarde el fichero RSS para que pueda acceder Sick Beard
	- y por último esto: ```fichero.write('\t<link>http://192.168.XXX.XXX/rss/tmp/' + titulo + '.torrent</link>\n')``` cambiar por la ip de vuestro servidor y la ruta donde están guardados los ficheros torrent
* dar permisos de ejecución: 
```sudo chmod +x newpct.py```
* ahora tenemos 2 opciones:
	+ lanzarlo manualmente: ```./ruta_descarga_fichero/newpct.py``` 

	+ incluirlo en nuestro [crontab](http://es.wikipedia.org/wiki/Cron_(Unix)) y ejecutarlo cada 3 horas por ejemplo añadiendo la siguiente línea a nuestro fichero "/etc/crontab"
	``` *	*/3	*	*	*	usuario	./ruta_descarga_fichero/newpct.py```
* añadimos el proveedor de torrent a Sick Beard:

  ![alt text](http://oi61.tinypic.com/10ndloh.jpg "añadir proveedor torrent")


--
#### Agradecimientos
>>> Thanks  	__dragor__
