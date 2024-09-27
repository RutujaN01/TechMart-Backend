## TechMart Backend
### Installation
- Clone the repository by running the following in a terminal:  
  - `git clone https://github.com/RutujaN01/TechMart-Backend.git`
  - `cd TechMart-Backend`
- Create and activate a virtual environment:  
  - `python -m venv venv`
  - `source venv/bin/activate  # On Windows use 'venv\Scripts\activate'`
- Install the required packages:  
  - `pip install -r requirements.txt`
### Getting Started
- Apply migrations:  
  - `python manage.py migrate`
- Run the development server:  
  - `python manage.py runserver 8081`
- Access the application at http://127.0.0.1:8081/  
### Contribution Guidelines
- Clone the repository and create your branch from main.
- Write clear, concise commit messages.
- Test your changes thoroughly.
- Submit a pull request with a detailed description of your changes.
#### Pull Request Format
##### Title: 
- A brief description of the changes.
##### Description: 
- Detailed information about what was changed and why.
  - Closes #issue_number (if applicable)
  - Changes: List of changes made
  - Tests: List of tests that were added/modified/deleted
