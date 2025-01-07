# Ecommerce API  

A RESTful e-commerce API built with Python and FastAPI.

## Prerequisites  
Make sure you have the following installed:  
- [Python 3.9+](https://www.python.org/downloads/)  
- [Git](https://git-scm.com/)  

## Installation  
Follow these steps to set up the project on your local machine:  

### 1. Clone the repository  
Clone this repository to your local machine:  
```bash  
git clone https://github.com/sofiaarasme/ecommerce-api.git  
cd ecommerce-api
```

### 2. Create the virtual environment
```bash  
# Create the virtual environment  
python -m venv venv  

# Activate the virtual environment  
# On Windows:  
.\venv\Scripts\activate  

# On macOS/Linux:  
source venv/bin/activate  
```

### 2. Run the project
```bash  
# Terminal command to run app:  
uvicorn main:app --reload
```