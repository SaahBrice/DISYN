

# 📚 Disyn Platform

Welcome to **Disyn** – a dynamic web platform designed to catalog and display various entities across Cameroon, including industries, restaurants, schools, shops, bakeries, hotels, and more! 🎉 This platform serves as a central resource for Cameroonians seeking detailed information about these entities, such as location, contact details, and other relevant information. It also serves as a platform where people can apply for jobs and internships openings, as well as company or entities visit. 

## 🚀 Project Overview

**Disyn** is built with a focus on accessibility and usability, ensuring that users can easily find and interact with the information they need. The platform is designed using a **mobile-first approach** to provide a seamless experience across all devices.

### Key Objectives:

- **Centralized Directory**: A comprehensive directory for industries, restaurants, schools, and other entities in Cameroon.
- **Easy Access**: Users can easily access detailed information about various entities.
- **Responsive Design**: A modern, responsive design that prioritizes mobile devices.
- **Streamlined Management**: A streamlined process for content management and application handling.

## 🛠️ Features

### Entity Posts

- **Consistent Structure**: Each entity (e.g., industry, restaurant, school) has a dedicated post with consistent structure across the platform.
- **Images**: Visual representation through logos, photos, etc.
- **Upvote Option**: Users can upvote entities without needing to sign in, with an optional field to provide feedback.
- **Location and Contact Information**: Detailed location, email, phone number, and optionally, the director's name.
- **Tags**: Categorize entities using tags like School, Shop, Restaurant, etc.
- **External Links**: Direct users to more detailed information via external links.

### User Management

- **Admin Control**: The platform has a single user type – the Admin, who has comprehensive control over content, applications, and user feedback.

### Design and UI/UX Considerations

- **Modern and Elegant Design**: A clean, visually appealing interface that prioritizes user experience.
- **Mobile-First and Responsive**: Optimized for mobile devices with seamless adaptation to different screen sizes.

### Technology Stack

- **Backend**: Powered by Django, and SQLite.
- **Frontend**: Styled with Tailwind CSS for a customizable and consistent design, enhanced with custom CSS.

### Additional Functionalities

- **Search and Filtering**: Users can search and filter entities by name, location, or category.
- **Application Management**: Entities can apply to be listed on the platform, with applications managed by the Admin.
- **Analytics**: Basic analytics for tracking user engagement.

## 🗓️ Project Timeline

### Phases and Milestones:

1. **Requirements Gathering and Planning** (1 weeks)
2. **Backend Development** (2 weeks)
3. **Frontend Development** (1 weeks)
4. **Testing and QA** (1 weeks)
5. **Deployment and Launch** (3 days)



## 🛠️ Development Guidelines

### Code Structure

- **Django Apps**: Organized into Django apps, each responsible for different parts of the platform.
- **CSS Organization**: Tailwind CSS as the primary styling tool, with modular and well-documented custom CSS.
- **Version Control**: Managed via Git, with regular commits and proper branching.


## 🛠️ How to Run the Project

### Prerequisites

Ensure you have the following installed on your local machine:

- **Python 3.10**: The backend of the application is built using Python.
- **Django**: The web framework used to build the platform.
- **Git**: For version control.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/saahbrice/disyn.git
   cd disyn
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Frontend Setup** 

   Tailwind CSS

   ```bash
   pip install tailwindcss
   ```

5. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**:

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**:

   ```bash
   python manage.py runserver
   ```

   The application should now be running at `http://127.0.0.1:8000/`.

8. **Access the Admin Panel**:

   Go to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created.

### Deployment

For deploying the project to a live server, you may follow these steps:

1. **Configure Production Settings**: Update your settings for production in `settings.py` (e.g., disable DEBUG, set ALLOWED_HOSTS, configure database, etc.).

2. **Collect Static Files**:

   ```bash
   python manage.py collectstatic
   ```

3. **Deploy to a Server**: Deploy using services like AWS, Heroku, or any server that supports Django.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## 📧 Contact

For any inquiries, please contact the project team at [saahbrice98@gmail.com).
