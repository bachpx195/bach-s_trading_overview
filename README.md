# Overview

a.map{|x| [(Date.parse(x)).strftime("%Y-%m-%d"), (Date.parse(x) + 1.days).strftime("%Y-%m-%d"), (Date.parse(x) + 2.days).strftime("%Y-%m-%d")]}.flatten.uniq

## Install
```shellscript
source .venv/bin/activate
pip install .
```

## Run
```shellscript
source .venv/bin/activate
streamlit run main.py --logger.level=debug
```
