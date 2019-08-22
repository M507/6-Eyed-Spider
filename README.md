# 6-Eyed-Spider - Under development 
![logo](https://github.com/M507/6-Eyed-Spider/raw/master/Examples/spider-1.png)

### Abstract
This is a post-exploitation Red-Teaming tool. It gathers data going out and coming into the browser — data like POST requests, cookies, and chosen headers like (ANTI-CSRF headers), then sends all data to Strapi. Strapi and MongoDB store the data so that 6-Eyed-Spider-CLI can use the collected data to perform specific attacks. Attacks using the users' valid cookies to execute commands, create admin users, enable unwanted functionalities, manipulate data in systems like VMware, Pfsense, and PanOS. 

The tool consists of a couple of parts:
* Dockerized MongoDB and Strapi
  * MongoDB stores the collected data.
  * Strapi receives and manages the collected data.
* Google-Chrome Extention
  * Collects the browser's data from the blue team.
* 6-Eyed-Spider-CLI
  * Runs custom made plugins which make use of the collected data.

### Disclaimer
This Red-Team tool is used for educational purposes ONLY!

## Table of contents:
 * [Abstract](#abstract)
 * [Disclaimer](#disclaimer)
 * [How to](#how-to)
    * [Install 6-Eyed-Spider](#install-6-eyed-spider)
    * [Run the server manually](#run-the-server-manually)
 * [Configure the admin panel and the API address from](#configure-the-admin-panel-and-the-api-address-from)
    * [Then with administrator privileges](#then-with-administrator-privileges)
    * [Clients:](#clients)
 * [6-Eyed-Spider-CLI Plugins](#6-eyed-spider-cli-plugins)
 * [Dependencies](#dependencies)
 * [Todos](#todos)

### How to:
#### Install 6-Eyed-Spider:
```sh
[M507:~]$ bash Install.sh
```
#### Run the server manually:
```sh
[M507:~]$ # Start the database
[M507:~]$ docker-compose -f docker-compose-db.yml up --build -d
[M507:~]$ # Wait 20 seconds until its states changes to healthy 
[M507:~]$ watch docker-compose -f docker-compose-db.yml ps
[M507:~]$ # Insert db.dump into the database, using this command
[M507:~]$ docker exec -i strapi-docker_db_1 sh -c 'mongorestore --archive'< RedAdmin.dmup
[M507:~]$ # Start the Strapi
[M507:~]$ docker-compose -f docker-compose-main.yml up --build -d
```
Or run Run.sh, which executes the same commands above.
```sh
[M507:~]$ bash Run.sh
```
###  Configure the admin panel and the API address from:
```sh
[M507:~]$ cat ./strapi-app/config/environments/development/server.json
{
  "host": "localhost",
  "port": 1337,
  "proxy": {
   "enabled": false
  },
  "autoReload": {
    "enabled": true
  },
  "cron": {
    "enabled": false
  },
  "admin": {
    "autoOpen": false
  }
}
```

Info ☄️  Default Admin panel: http://localhost:1337/admin
Info ⚡️ Default Server: http://localhost:1337

#### Then with administrator privileges:
Default credentials: admin:RedAdmin
* Insert all the targeted domains into: http://127.0.0.1:1337/Domains
* Insert all the targeted headers into: http://127.0.0.1:1337/Headers
* http://127.0.0.1:1337/Posts receives data from the public without any privileges.
* /Posts receives: IP (String),ID (String), Site (String), and Data (Json), Type (String). Type: either "Cookie", "Header", or "Form".
An example:
```html
{
    "IP": "192.168.1.2",
    "ID": 31231,
    "Site": "https://aavtrain.com/index.asp",
    "Data": {
        "Submit": "Submit",
        "login": "true",
        "password": "MYPASSWORD",
        "user_name": "admin"
    },
    "Type": "Cookies"
}
```

#### Clients:
```sh
Microsoft Windows [Version 10.0.17763.503]
(c) 2030 Microsoft Corporation. All rights reserved.

C:\Users\Mohad> .\New-ChromeExtension.ps1 (Powershell Payload attached). 
```


### 6-Eyed-Spider-CLI Plugins:
6-Eyed-Spider-CLI runs customized plugins that make use of the valid collected data from the API. 
+ VMware
    + Add an administrator
    + Start SSH
+ Pfsense
    + Add an administrator
    + Execute a command

### Dependencies
+ Docker-compose

### Todos

- Firefox extension configures itself based on the data on /domains /headers.
- Firefox extension sends All POST requests, cookies to /Posts as described above.
- New-FirefoxExtension.ps1
