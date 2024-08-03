# Getting Started

Follow these steps to get the application up and running:

1. **Clone the Repository**
   ```bash
   git clone git@github.com:Vernadskii/feedback.git
   cd feedback
   ```
2. **Configure Environment Variables**  
Ensure you have a .env file in the root of your project directory.  
Rename env.example to .env to use it.


3. **Build and Start the Containers**
To build and start all the services defined in docker-compose.yml file, run:
    ```bash
    docker-compose up --build
    ```
   
4. **Access the Application**
Once the containers are up and running, you can access application.
- Backend: http://localhost:8080
- Frontend: http://localhost:5173
- Database localhost:5433