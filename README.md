## JBG050 Data Challenge 2 | Group 12

### 💡 Project Description
This repository contains the Python source code and the `.ipynb` notebooks containing the analysis of team 12 for the course JBG050.

Given a large set of Police datasets, the project was aiming towards enhancing the level of trust and confidence of London's citizens in the Metropolitan Police.

### 💻 Code Structure
Most of the code is available in Jupyter notebooks and therefore, the user is required to have a Jupyter client installed. 
Please follow the guidance of [this](https://jupyter.org/install) link in order to install Jupyter.

### 👨🏽‍💻 Installation and Setup
We encourage the user to use a virtual environment to run this project locally. This is to isolate the environment in which the codebase and it's dependencies run from the original host environment.

To achieve this you can choose to either use [Python venv](https://docs.python.org/3/library/venv.html) or a [Conda](https://www.anaconda.com/download/) environment.

The source-code is compatible with Python version 3.12.0.

1. Install [Python pip](https://pypi.org/project/pip/) to manage dependencies.
2. Run `pip install -r requirements.txt` in your terminal environment (from the project root) to install the associated dependencies.
3. Place the data correctly.
   
   To ensure that the stakeholder data is not shared with public or non-authorized parties, we do not include the datasets associated with analysis in this repository.
   The user must place the data in the corresponding sub-folders located in the data directory.
4. Run the pre-processing. 
   1. Run merge-sas.py to merge all the Stop-and-Search datasets.
         Simply run `python merge-sas.py` form your terminal environment.
   2. Within each notebook, perform the pre-processing required prior to running the other cells.
5. Fetch the additional datasets by running `src/data_utils/download_metro_police_data.py`.

### 📊 Running the analysis
There are multiple models trained and evaluated for this project. Most of which are explained thoroughly in the technical report. To reproduce the results, the notebooks have been named in a clear way to explain what each file
is responsible for. You can simply locate the file for which you're interested in knowing the results and then running the notebook cells.
