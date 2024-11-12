# Overview

a.map{|x| [(Date.parse(x)).strftime("%Y-%m-%d"), (Date.parse(x) + 1.days).strftime("%Y-%m-%d"), (Date.parse(x) + 2.days).strftime("%Y-%m-%d")]}.flatten.uniq

## Install
```shellscript
source .venv/bin/activate
pip install .
```

## Run
```shellscript

<!-- MACOS -->
source .venv/bin/activate
streamlit run main.py --logger.level=debug


<!-- UBUNTU -->
source .venv/bin/activate
python3 -m streamlit run main.py --logger.level=debug
```
