# Setup

This project was built using Python 3.12.3.

Install Graphviz on your system.

**Ubuntu / Debian**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

Clone the repository.

```bash
git clone <repository-url>
```

Create and activate a virtual envrironment on the project directory.

```bash
cd <repository-directory>
python3 -m venv .venv
source .venv/bin/activate
```

Install Dependencies.

```bash
pip3 install -r requirements.txt
```

On the cloned reposotitory, create a sobfolder named "data". Drag the data files into it.

```bash
mkdir data
```

With the virtual environment activated, run the main script to get the plots and the model results.

```bash
python3 main.py
```