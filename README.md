[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/MhTU6TbO)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=15411227&assignment_repo_type=AssignmentRepo)

# Final Rroject - Robo Advisor Submission Guide

Welcome to the Final Project for your NLP Applications course at UCSD's Rady Business School. This document provides detailed instructions on how to submit your group assignments through GitHub Classroom.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Accepting the Assignment](#accepting-the-assignment)
3. [Setting Up Your Repository](#setting-up-your-repository)
4. [Using the Assignment Template](#using-the-assignment-template)
5. [Secret Management](#secret-management)
6.[Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following:

1. A GitHub account.
2. Git installed on your local machine.
3. Docker installed on your local machine. Follow the [Docker installation instructions](https://docs.docker.com/get-docker/) for your operating system.
4. Windows Subsystem for Linux (WSL) for Windows users or a Unix-based system (macOS) for macOS users.
5. Basic understanding of Git and Docker commands.

## Accepting the Assignment

1. You will receive an invitation link to the GitHub Classroom for this assignment.
2. Click on the link, and you will be directed to GitHub Classroom.
3. If prompted, authorize GitHub Classroom to access your GitHub account.
4. Accept the assignment. This will create a private repository for your submission.

## Setting Up Your Repository

1. After accepting the assignment, navigate to your newly created repository.
2. Clone the repository to your local machine using the following command:

    ```sh
    git clone <repository_url>
    ```

    Replace `<repository_url>` with the URL of your repository.

3. Navigate to the cloned repository directory:

    ```sh
    cd <repository_name>
    ```

## Using the Assignment Template

1. Once you accept the classroom invitation and cloned your own repo, you should see the repo is already set up from the assignment template.
2. This template helps you set up the environment you need for your assignment.  The repository is set up with Docker and Poetry. It already includes classical NLP packages such as `nltk`, `textblob`, `vader`, and data science packages like `pandas`, `numpy`, `seaborn`, and `jupyterlab`.

### Starting Jupyter Lab
The template already set up a docker container and Makefile that allows you to easily spin up a docker container for your assignment.  You can start the Jupyter lab after you navigate to the cloned repository:

```sh
make nb
```

### Adding Packages with Poetry

If you need to add additional packages, you can do so using Poetry. To add a package, use the following command inside the Docker container:

```sh
docker exec mgta415_dmc_develop poetry add <package_name>
```
Replace <package_name> with the name of the package you want to add.

Once the package is added, please run the following command to make sure the dependencies will persist.

```sh
docker exec mgta415_dmc_develop poetry lock
```

## Secret Management

1. Create a `.env` file in the root directory of your project using the env_template file.
2. Add your API key and secret to the `.env` file in the following format:

    ```plaintext
    ALPACA_API_KEY=your_api_key_here
    ALPACA_SECRET_KEY=your_secret_key_here
    ```

3. Ensure your Docker container loads these environment variables. The provided Docker setup in the template repository should handle this automatically. If not, modify your `docker-compose.yml` to include:

    ```yaml
    services:
      your_service_name:
        env_file:
          - .env
    ```

4. Access these environment variables in your code using a package like `python-dotenv` or directly through `os.environ` in Python:

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()

    ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
    ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
    ```

5. Never commit your `.env` file to version control. Add `.env` to your `.gitignore` file to ensure it is excluded:

    ```plaintext
    # .gitignore
    .env
    ```


## Troubleshooting

- If you encounter issues with Docker, ensure Docker is properly installed and running on your machine. Refer to the [Docker installation instructions](https://docs.docker.com/get-docker/) for help.
- For Git-related issues, refer to the [Git documentation](https://git-scm.com/doc).
- If you have any other questions or face issues not covered in this guide, please reach out to the course instructor.
