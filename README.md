<div align="center">

# 🐍 Deploying a ResNet ONNX Model on AWS Lambda
[![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-Python_3.9-blue?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/lambda/)
[![ONNX](https://img.shields.io/badge/ONNX-1.17.0-005CED?logo=onnx&logoColor=white)](https://onnx.ai/)
[![Mangum](https://img.shields.io/badge/Mangum-0.17.0-blueviolet)](https://mangum.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.98.0-teal?logo=fastapi)](https://fastapi.tiangolo.com/)

A step-by-step guide to deploying a ResNet50 model, converted to ONNX, using FastAPI and Mangum on AWS Lambda. This project demonstrates how to create a serverless image classification service running on AWS Lambda, complete with API Gateway integration.

</div>

## 📌 Introduction
This repository provides all the necessary code and instructions to deploy a pre-trained ResNet50 model as a serverless API on AWS Lambda. By leveraging FastAPI for the web framework and Mangum for AWS Lambda compatibility, we create a scalable and efficient image classification service.

<br>

## 📦 Main Technologies

- __ResNet50__: A powerful convolutional neural network for image classification tasks.
- __ONNX (Open Neural Network Exchange)__: A format for representing deep learning models to enable interoperability.
- __FastAPI__: A modern, fast web framework for building APIs with Python 3.6+.
- __Mangum__: An adapter for using ASGI applications with AWS Lambda & API Gateway.
- __Docker__: Containerization platform to package the application and its dependencies.
- __AWS Lambda__: Serverless compute service that runs code in response to events.
- __API Gateway__: A fully managed service for creating, publishing, maintaining, monitoring, and securing APIs.
<br>

## 📁 Project Structure
```
├── checkpoints
├── data
│   └── imagenet_classes.txt
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── scripts
│   ├── export_onnx.py
│   └── requirements.txt
├── server.py
└── tests
    └── onnx_test.py
```
- __checkpoints__: Contains the exported ONNX model.
- __data__: Holds necessary data files like class labels.
- __scripts__: Contains scripts for model export and other utilities.
- __tests__: Includes testing scripts to verify the ONNX model.
- __server.py__: The FastAPI server script with Mangum integration.
- __Dockerfile__: Instructions to containerize the application.
- __requirements.txt__: Python dependencies for the application.

<br>

## 🚀 Quickstart
Follow these steps to set up and deploy the application:

### Prerequisites
- __AWS Account__: [Sign up for AWS](https://signin.aws.amazon.com/signup?request_type=register) if you don't have one.
- __AWS CLI__: Install and configure the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- __Docker__: Install [Docker Desktop](https://docs.docker.com/engine/install/).
- __Python 3.9__: Ensure Python is installed on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com/sh-aidev/lambda-classifier-deployment.git
cd lambda-classifier-deployment
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Export the ResNet50 Model to ONNX
First, install the required libraries for model export:
```bash
pip install -r scripts/requirements.txt
```
Then, run the export script to convert the ResNet50 model to ONNX format:

```bash
python scripts/export_onnx.py
```
This will download the ResNet50 model and export it to ONNX format, saving it in the `checkpoints` directory.

### 4. Build and Test the Docker Image Locally
Build the Docker image:
```bash
docker build -t resnet50-fastapi .
```
Run the Docker container:
```bash
docker run --rm -it -p 8000:8000 resnet50-fastapi
```
Test the API locally:
```bash
curl --location --request GET 'https://<ip addr>:<port>/2015-03-31/functions/function/invocations' \
--header 'Content-Type: application/json' \
--data '{
    "resource": "/",
    "path": "/", 
    "httpMethod": "GET", 
    "requestContext": {}
}'
```

### 5. Push Docker Image to AWS ECR

Authenticate Docker to your AWS ECR registry:
```bash
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com
```
Create an ECR repository.

Tag and push the image:
```bash
docker build -t lambda-classifier .
docker tag lambda-classifier:latest <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/lambda-classifier:latest
docker push <your-aws-account-id>.dkr.ecr.<your-region>.amazonaws.com/lambda-classifier:latest
```

### 6. Create AWS Lambda Function
- Navigate to AWS Lambda in the AWS Console.
- Click __Create function__.
- Select __Container image__.
- Choose the image from ECR.
- Set __Function name__ to `lambda-classifier`.
- Increase __Timeout__ to 2 minutes and __Memory__ to 768 MB under __Configuration__ > __General configuration__.
### 7. Set Up API Gateway
- In your Lambda function, click on __Add trigger__.
- Select __API Gateway__.
- Choose __Create an API__.
- Set __API Type__ to __REST API__.
- Click __Add__.

Configure the API Gateway:

- Navigate to API Gateway service.
- Create a new __Resource__ called `/infer`.
- Enable __CORS__.
- Create a __POST__ method under `/infer`.
- Set the integration type to __Lambda Function__ and select your __Lambda function__.
- Deploy the API to a stage (e.g., `prod`).

### 9. Test the Setup with a POST Request
Use Postman to send a POST request for the above created API Gateway endpoint with an image file as input.

Expected response:
```json
{
  "predicted": "tabby, tabby cat"
}
```
## 📝 Notes
- Ensure that the AWS Lambda function has the necessary execution role permissions.
- Adjust the memory and timeout settings based on your model's performance.
- For security, consider implementing authentication mechanisms for your API.

## 📚 References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Mangum](https://github.com/Kludex/mangum.git)
- [ONNX Runtime](https://onnxruntime.ai/docs/)
- [AWS Lambda Container Images](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/deploy-lambda-functions-with-container-images.html)
- [Docker](https://docs.docker.com/get-started/)
