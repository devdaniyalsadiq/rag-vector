## Create env if not exists

```
python3 -m venv venv
```

## Activate env

```
source venv/bin/activate
```

## Install Packages

```
python3 -m pip install -r requirements.txt
```

## To run App

```
streamlit run app.py
```
# PRODUCTION 

Run the application in background using `nohup`

## Run application

```bash
nohup streamlit run app.py > output.log 2>&1 &
```

## Check Logs

```bash
cat output.log
```

## Check Instances running 
This will show all the running processes

```bash
ps -ef | grep streamlit
```

## Kill the process

```bash
kill -9 PID

For example
kill -9 1234
```
