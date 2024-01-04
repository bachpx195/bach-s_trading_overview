# Overview

a.map{|x| [(Date.parse(x)).strftime("%Y-%m-%d"), (Date.parse(x) + 1.days).strftime("%Y-%m-%d"), (Date.parse(x) + 2.days).strftime("%Y-%m-%d")]}.flatten.uniq

## Install
```shellscript
pip install .
```

## Run
```shellscript
streamlit run main.py --logger.level=debug
```
