# Flask Application for Social Hobbies

This project is a simple Flask web application that allows users to share their hobbies and interests. Users can enter their name, favorite hobby, and email address, which will be displayed on the page.

## Project Structure

```
flask-app
├── app.py                # Main entry point of the Flask application
├── static
│   ├── app.js            # JavaScript file for client-side functionality
│   └── style.css         # CSS file for styling the HTML page
├── templates
│   └── pythonofsf.html   # HTML file served to the client
├── requirements.txt      # List of dependencies for the project
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd flask-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Flask application, execute the following command in your terminal:

```
python app.py
```

The application will be accessible at `http://127.0.0.1:5000/`.

## Usage

- Open your web browser and navigate to the application URL.
- Enter your name, favorite hobby, and email address in the provided fields.
- Click the "Submit" button to see your entry added to the list of users.

## License

This project is licensed under the MIT License.