### 🔑 API Key Setup

This project requires a Cohere API key to generate eBook content. Follow these steps to set it up:

1.  **Get Your Cohere API Key:**
    * Sign up or log in to the Cohere dashboard: [https://cohere.com/](https://cohere.com/)
    * Navigate to the "API Keys" section and generate a new Trial Key.

2.  **Create `config.py`:**
    In the root directory of this project, create a new file named `config.py`.

3.  **Add Your Key:**
    Edit the `config.py` file and add your API key like this, replacing `YOUR_COHERE_API_KEY_HERE` with the key you obtained:

    ```python
    # config.py
    COHERE_API_KEY = 'YOUR_COHERE_API_KEY_HERE'
    ```
    **Important:** `config.py` is ignored by Git to protect your credentials and should not be committed to your repository.
