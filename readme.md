# Web-Based Integrated Surveillance System

## Introduction
Welcome to the Web-Based Integrated Surveillance System project! This project aims to develop a comprehensive security solution that integrates various surveillance components into a unified web-based platform. The system allows users to monitor and control cameras, motion sensors, alarm systems, and floodlights remotely via a user-friendly web interface.

## Features
- **Multiuser Authentication:** Users can register and log in with their credentials to access the surveillance system. Different access levels are implemented to ensure secure and personalized user experiences.
- **Dashboard:** The dashboard provides an overview of the surveillance system, including live camera feeds, alarm status, and recent activity logs.
- **Camera Management:** Users can view live camera feeds, adjust camera settings, and access recorded footage.
- **Motion Sensor Control:** Users can monitor motion sensor activity and configure alert settings.
- **Alarm System:** Users can activate/deactivate the alarm system and receive notifications for triggered alarms.
- **Floodlight Control:** Users can control the activation/deactivation of floodlights to enhance visibility in dark environments.
- **Remote Data Logging:** The system logs security events and activities for future analysis and reference.
- **SMS Reporting:** Emergency interventions are facilitated through SMS reporting, allowing users to receive instant alerts and notifications on their mobile devices.

## Installation
1. Clone the repository to your local machine:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd surveillance
   ```
3. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure the database settings in `settings.py`.
5. Apply database migrations:
   ```
   python manage.py migrate
   ```
6. Create a superuser account for admin access:
   ```
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage
- Access the web app in your browser by navigating to `http://localhost:8000`.
- Log in with your credentials or register as a new user.
- Explore the different features of the surveillance system, including camera management, motion sensor control, alarm system, floodlight control, and more.
- Customize user settings and preferences as needed.
- Monitor security events and activities through the dashboard and receive notifications for critical alerts.

## Contributors
- [Opeyemi olalekan](https://github.com/olamilekan5162)
- [Adeyemi micheal](https://github.com/adeyemimichael)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
