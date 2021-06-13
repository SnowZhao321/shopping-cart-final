# Shopping-Cart-Project

## Installation

Clone or download from [GitHub source](https://github.com/SnowZhao321/shopping-cart-final), then navigate into the project repository:

```sh
cd shopping-cart-final
```

please install python version 3.8 in a conda environment, and create and activate a new project-specific Anaconda virtual environment:
```
conda create -n shopping-cart python=3.8 

conda activate shopping-cart
```

Install required python modules
```
pip install -r requirement.txt
```


## Usage

Run the program:

```py
python shopping_cart.py
```
Follow the program instruction to input item identifier 1-20 or DONE when finish. When DONE is input, a receipt with item details, total price and tax will be printed. 

## Configuring Environment Variables
edit the ".env" file in the root directory of this repo, and place tex rate of your current state like the following inside:
```TAXRATE=0.0875```
