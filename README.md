# To-Do List PWA

A simple, efficient, and mobile-friendly To-Do List App built with Python (Flask) and deployed as a Progressive Web App (PWA).

**Live Demo:** [https://todo-list-5kto.onrender.com](#)

## Features

- Add, edit, and delete tasks
- Mark tasks as completed
- Works as a Progressive Web App (PWA)
- Can be installed on Android & iOS
- Offline support using service workers

## Installation (For Local Use)

1. Clone the repository:

   ```bash
   git clone https://github.com/dnagelpro/todo-list.git
   cd todo-list
   ```

2. Create a virtual environment & install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```

3. Run the Flask app:

   ```bash
   python app.py
   ```

4. Open in browser:

   ```
   http://127.0.0.1:5000
   ```

## Deployment

This project is deployed using Render.

**Live URL:** [https://todo-list-5kto.onrender.com](#)

## PWA (Progressive Web App)

This app is a PWA, meaning it can be installed on mobile devices:

1. Open in Chrome (Android) or Safari (iPhone).
2. Tap "Add to Home Screen".
3. Launch the app like a native mobile app.

## License

This project is licensed under the MIT License – feel free to use and modify it!

## Future Improvements

- Convert to a mobile app using React Native or Flutter
- Add user authentication for personal task management
- Improve UI design
