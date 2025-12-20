# Data Processing
This is a web interface to perform various kinds of analysis on data.

## File types accepted
1. CSV

more to be supported

## How to run
Currently you can run this locally using Python or Docker.

```git clone https://github.com/actuallyarnav/data-processing.git```

```cd data-processing```
### Python
#### requirements: python3, pip
```pip install --no-cache-dir -r requirements.txt```

```python3 app.py```


### Docker
#### requirements: docker (of course)

```docker build -t data-proc .```

```docker run -p 8080:8080 data-proc```

Open ```http://127.0.0.1:8080/``` in a web browser
## Currently working
1. File uploads via HTML form
2. File Storage via Flask
3. Process data using basic techniques
3. Display the results (numerical, visual, etc.)

## To Do
1. Upload various kinda of files
2. Use more complex and informative techniques
