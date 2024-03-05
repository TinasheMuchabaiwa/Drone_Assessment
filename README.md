# Drone Management System Assessment

## Introduction
This project is a Drone Management System developed as part of an assessment for 4-Sure Technologies. It provides functionality to register drones, register medications, load drones with medications, and perform various other operations related to drones and medications.

## Requirements
- Python (version 3.10+)
- Django (version 4.2.9)
- Django REST Framework (version 3.14.0)
- DRF YASG (version 1.21.7) - for Swagger documentation
- Pillow (version 10.2.0) - for image handling
- Docker (optional)

## Installation
1. Clone the repository:

    ```
    git clone git@github.com:TinasheMuchabaiwa/Drone_Assessment.git
    ```

2. Navigate to the project directory:

    ```
    cd Drone_Assessment
    ```

3. Create and activate a virtual environment (optional):

    ```
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate      # For Windows
    ```

4. Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

5. Run database migrations:

    ```
    python manage.py migrate
    ```

6. Start the development server:

    ```
    python manage.py runserver
    ```

7. Access the API documentation at `http://127.0.0.1:8000`.

### Using Docker (Optional)
Alternatively, you can use Docker to run the application:

1. Build the Docker image:

    ```
    docker build -t drone-management-system .
    ```

2. Run the Docker container:

    ```
    docker run -p 8000:8000 drone-management-system
    ```

3. Access the API documentation at `http://127.0.0.1:8000`.

## Usage
- Use the Swagger UI to interact with the API endpoints and perform operations such as registering drones, registering medications, loading drones with medications, etc.

## Testing
- Automated tests are available to ensure the correctness of the implemented functionality.
- To run the tests, use the following command:

    ```
    python manage.py test
    ```

## Authors
- [TINASHE MUCHABAIWA](https://github.com/TinasheMuchabaiwa)

## License
This project is licensed under the [MIT License](LICENSE).