# Differentially private for binary dataset

This repository is for the project of **CS4257: Algorithmic Foundations of Privacy**

### Method:

The basic idea is to generate the synthetic data for differentially privacy based on the **marginal tables**

### Steps:

- Generate the marginal tables: run main.py

  The result will be saved in ```data/marginal_table_no_noise.pickle```

  ```python
  process = 'generate_marginal_table'
  num_attribute = 600 #number of attributes in the original dataset
  num_marginal_tables = 300 # how many marginal tables
  size_marginal_tables = 8 # how many attributes in one marginal tables
  epsilon = 3 # the differentially private parameter

  ```

- Generate the synthetic data: run main.py

  The data will be save in ```data/result.csv```

  ```python
  num_generate_data = 100 # how many data need to be generated
  num_attribute = 600 #number of attributes in the original dataset
  process = 'generate_data'
  ```

  ## Dataset:

  Please put the dataset in the data folder.
