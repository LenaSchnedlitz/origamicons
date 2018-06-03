<p align="center">
  <img src="https://github.com/Mailea/origamicons/blob/master/origamicon/static/img/logo.png"/>
</p>


# Origamicons

(Almost) unique identicons, based on SHA-1 and inspired by folded paper.   

## Requirements
This program is written in **Python 3.6**.  
Requirements are listed in *requirements.txt* and can be installed with Pip:
```bash
cd origamicon
pip install -r requirements.txt
```

## Web App
The web app can be started by executing `app.py` inside the *origamicon* folder:
```
python app.py
```

### URL Parameter
Origamicons can be requested directly using URL parameters, e.g.
```
localhost:5000/mailea
```

## Command Line Tool
The avatar generator can also be used as a command line tool:
```
python generator.py
```

## Online
To see the web app in action, click [here](http://sha1-origamicon.herokuapp.com/).
