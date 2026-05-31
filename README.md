# Mobile Library Application

This repository contains the source code of the **Mobile Library Application**, developed as a Graduation Thesis project in the Department of Computer Engineering at Çukurova University.

## Project Overview

The Mobile Library Application was developed to help users manage their personal reading activities through a single mobile platform. The application allows users to search for books, organize personal libraries, track reading progress, and maintain reading journals.

## Main Features

* User registration and login
* Book search using Google Books API
* Personal library management
* Reading status organization (Plan to Read, Reading, Completed)
* Reading progress tracking
* Reading journal system
* Personal notes and quotations
* User profile management

## Technologies Used

### Mobile Application

* Kotlin
* Jetpack Compose
* Android Studio

### Backend

* Python
* FastAPI
* SQLite
* SQLAlchemy

## Repository Contents

### Backend Source Code

The backend implementation is provided through the following files:

* `main.py` – REST API endpoints and application logic
* `models.py` – Database models
* `database.py` – Database configuration and database connection

### Android Application Source Code

The Android application source code is included in:

* `MobileLibraryApp.zip`

Most of the Android application logic, screen implementations, state management, and API integration are implemented within the Kotlin source files. A significant portion of the application functionality is located in `MainActivity.kt`, which coordinates the main user interface and application workflow.

## Code Review Guide

For reviewing the backend implementation, please examine:

* `main.py`
* `models.py`
* `database.py`

For reviewing the Android application, please extract `MobileLibraryApp.zip` and examine:

* `MainActivity.kt`
* User Authentication (Login & Register)
* Explore Screen and Google Books API Integration
* Library Management System
* Reading Progress Tracking
* Reading Journal System
* Profile Screen
* Jetpack Compose User Interface Components

## Running the Application

### Backend Setup

Navigate to the backend directory:


cd backend


Activate the virtual environment:


.\venv\Scripts\Activate.ps1


Allow script execution for the current session:


Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass


Start the FastAPI server:


uvicorn main:app --host 0.0.0.0 --port 8000


### Mobile Application Setup

1. Connect an Android device via USB.
2. Enable USB Debugging on the device.
3. Open the Android project in Android Studio.
4. Run the application on the connected device.

The mobile application communicates with the FastAPI backend running on the local network.

## Important Notes

* For security reasons, the Google Books API key has been removed before publishing this repository.
* Local configuration files, generated build files, database files, and API keys are not included.
* A valid Google Books API key is required to use the Google Books search functionality.
* The Android source code is provided as a ZIP archive to simplify repository submission.

## Author

Damla Gülen

Department of Computer Engineering

Çukurova University

2026
