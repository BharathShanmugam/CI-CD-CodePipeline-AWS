# FastAPI Deployment with AWS CodePipeline and CodeDeploy

This repository contains a sample FastAPI application configured for automated deployment to an AWS EC2 instance using AWS CodePipeline and CodeDeploy.

---

## **Project Structure**

```
myapp/
├── app/
│   ├── __init__.py         # Initialization file
│   ├── service.py          # Business logic and services
│   ├── api.py              # API routes
│   ├── model.py            # Database models
│   ├── schema.py           # Pydantic schemas
│   ├── db.py               # Database connection and session
│   └── main.py             # Application entry point
├── requirements.txt        # Project dependencies
├── appspec.yml             # AWS CodeDeploy configuration
├── scripts/
│   ├── install_dependencies.sh  # Script to install dependencies
│   └── restart_server.sh        # Script to restart the FastAPI application
├── tests/
│   ├── __init__.py         # Test initialization file
│   └── test_main.py        # Unit tests for the application
├── .gitignore              # Files to exclude from version control
└── README.md               # Project documentation
```

---

## **Features**

- **FastAPI Framework**: Lightweight Python web framework for building APIs.
- **Automated CI/CD**: Updates deployed automatically on code changes in GitHub.
- **AWS Integration**:
  - **CodePipeline**: Automates the deployment process.
  - **CodeDeploy**: Handles the deployment to an EC2 instance.

---

## **Setup**

### **1. Prerequisites**

- **For Local Development**:
  - Python 3.8 or later installed.
  - `pip` installed for dependency management.
- **For AWS Deployment**:
  - An AWS account.
  - An EC2 instance running Amazon Linux 2.
  - CodePipeline and CodeDeploy configured.
  - S3 bucket to store deployment artifacts.
  - CodeDeploy Agent installed on EC2.

---

## **Local Development**

### **Run Locally**

1. Clone the repository:
   ```bash
   git clone https://github.com/BharathShanmugam/CI-CD-CodePipeline-AWS.git
   cd CI-CD-CodePipeline-AWS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
4. Open the browser at [http://localhost:8000](http://localhost:8000).

---

## **Deployment on EC2 Server**

### **Steps for Automated Deployment**

1. **Push Changes to GitHub**:
   - Any changes in the repository (e.g., `requirements.txt` or source code) are detected by **AWS CodePipeline**.
2. **CodePipeline Workflow**:
   - Pulls the latest code from GitHub.
   - Deploys the code to the EC2 instance using **AWS CodeDeploy**.
   - Installs dependencies from `requirements.txt` and restarts the FastAPI application.

### **Access the Deployed Application**

- Once deployed, the application runs on the EC2 instance.
- Access it via the public IP or domain of the EC2 server:
  ```
  http://<ec2-public-ip>:8000
  ```
  Replace `<ec2-public-ip>` with the actual public IP of your EC2 instance.

---

## **Deployment Configuration**

### **CodeDeploy Setup**

#### **`appspec.yml`**

Defines the deployment process for AWS CodeDeploy:

```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/myapp
hooks:
  AfterInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root
  ApplicationStart:
    - location: scripts/restart_server.sh
      timeout: 60
      runas: root
```

### **Scripts**

#### **`scripts/install_dependencies.sh`**

```bash
#!/bin/bash
echo "Installing dependencies..."
cd /var/www/myapp
pip install -r requirements.txt
```

#### **`scripts/restart_server.sh`**

```bash
#!/bin/bash
echo "Restarting FastAPI server..."
pkill -f "uvicorn"
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &
```

---

## **AWS Setup**

### **CodePipeline**

1. Create a new pipeline in AWS CodePipeline.
2. **Source Stage**: Connect the pipeline to your GitHub repository.
3. **Deploy Stage**: Add CodeDeploy to deploy the application to an EC2 instance.

### **CodeDeploy**

1. Create a CodeDeploy application.
2. Create a deployment group:
   - Attach an IAM role with `AmazonEC2RoleforAWSCodeDeploy`.
   - Add an EC2 instance tag (e.g., `Environment=Production`).
3. Install the CodeDeploy agent on the EC2 instance:
   ```bash
   sudo yum update -y
   sudo yum install ruby -y
   sudo yum install wget -y
   cd /home/ec2-user
   wget https://aws-codedeploy-ap-southeast-1.s3.amazonaws.com/latest/install
   chmod +x ./install
   sudo ./install auto
   sudo service codedeploy-agent start
   ```

---

## **Testing**

### **Run Tests**

Unit tests are located in the `tests` folder:

```bash
pytest tests/
```

---

## **Troubleshooting**

1. **Deployment Fails**:

   - Check logs in the AWS CodeDeploy Console.
   - SSH into the EC2 instance and verify logs in `/var/log/aws/codedeploy-agent/`.

2. **Application Not Running**:
   - Verify the application is running:
     ```bash
     ps aux | grep uvicorn
     ```
   - Restart manually if necessary:
     ```bash
     nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &
     ```

---

## **Contributors**

- **Bharath Shanmugam**: Initial setup and development.

---

## **Support**

For any issues, please open a GitHub issue in this repository.
