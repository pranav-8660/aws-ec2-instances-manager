# EC2 Instance Manager

## Overview
This project is an EC2 Instance Manager that helps manage AWS EC2 instances efficiently.

## Setup Process
Instead of cloning the repository, you can refer to the repository and manually set up the project structure as follows:

### Backend Setup
1. Create a `backend` directory.
2. Inside the `backend` directory, create a `main.py` file, copy the contents of main.py from this repo.
3. Create an `infrastructure` directory inside `backend`.
4. Add a `main.tf` file inside `backend/infrastructure` and copy the contents of main.tf from this repo.

### Frontend Setup
1. Create a `frontend` directory.
2. Inside `frontend`, create a React app using:
   ```sh
   npm create react-app frontend-app
   ```
3. Replace the `App.js` file with the one from the repository.
4. Add a `EC2Manager.jsx` file from the repository.

## Notes
- Ensure that AWS credentials are configured properly for backend operations, to do this install aws-cli and configure the access key and the secret key manually.
- Terraform must be installed to use the `main.tf` file.Also run `terraform init`,`terraform plan`,`terraform apply` in order to run `main.tf`.
- The frontend should be started using `npm start` after setting up dependencies.
- To start the backend, we need python libraries `fastapi, uvicorn`, so install them using `pip install fastapi, uvicorn`. To run the backend use `uvicorn main:app --reload`.

For detailed implementation, refer to the repository.
