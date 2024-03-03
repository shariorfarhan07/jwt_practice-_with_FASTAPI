## Setting Up a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies. Follow these steps to set up a virtual environment:

```bash
# Create a virtual environment named 'env'
python3 -m venv env
#Or
python -m venv env
# Activate the virtual environment
source env/bin/activate  # On macOS/Linux
# Or
.\env\Scripts\activate   # On Windows
```

## Installing Dependencies

Once the virtual environment is activated, you can install project dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## when all the dependencies are installed run 
```bash
uvicorn controller:app --reload
```
then go to localhost:8000/docs for the swagger page
