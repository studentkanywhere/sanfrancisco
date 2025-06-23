# Pursuit

This project is a simple Flask web application that allows users to share their hobbies and interests. Users can enter their name and favorite hobby which will be displayed on the main page.

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
   git clone https://github.com/studentkanywhere/sanfrancisco
   cd flask-app
   ```

2. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Flask application, execute the following command in your terminal:

```
python app.py 
```

The application will be accessible at `http://<ipaddress>:5000/`.

## Usage

- Open your web browser and navigate to the application URL (Currently not deployed).
- Enter your name, favorite hobby, and email address in the provided fields.
- Click the "Submit" button to see your entry added to the list of users.

## License

This project is licensed under the MIT License.
