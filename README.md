# **2022 U.S. Hospital Services Areas(HSAs)**: Web Application with Multi-Page Navigation

[HSAs](https://lnshuti--hsas-datasette-ui.modal.run)

# Docs
[Docs](https://healthcare-services-areas-obga1oo27-lnshutis-projects.vercel.app)

**Version**: 1.0

### 1. Overview
Web application with five primary subpages: **Home, Login, Blog, About, and Pricing**. The application allows to sign in using their Google account or traditional email and password credentials. Additionally, users can view blogs, learning more about the company on the About page, and exploring pricing options.

### 2. Objectives
- To provide a simple, intuitive user interface for navigation between multiple pages.
- To allow users to sign in using their Google account or standard login credentials.
- To inform visitors about the application through a blog, about section, and pricing page.
- To ensure the application is responsive, scalable, and secure.

### 3. Pages Description and Requirements

#### 3.1. Home Page
- **Purpose**: Acts as the landing page for the website, offering users a snapshot of the site’s purpose and content.
- **Key Features**:
  - Clean, simple design with a prominent call to action.
  - A navigation bar allowing access to other subpages: Login, Blog, About, Pricing.
  - Footer with links to Terms of Service, Privacy Policy, and Contact Information.
  
- **User Stories**:
  - As a visitor, I want to understand the purpose of the website immediately upon landing.
  - As a visitor, I want clear navigation to explore other parts of the website.

#### 3.2. Login Page
- **Purpose**: Allows users to securely sign in with their credentials or through a third-party Google service.
- **Key Features**:
  - **Google Sign-In Button**: Positioned at the top for easy access, allowing users to sign in using their Google account.
  - **Email/Password Form**: Traditional sign-in form with input fields for "Email or Username" and "Password".
    - Password visibility toggle (eye icon) to show/hide password input.
  - **Log In Button**: Standard button with clear "Log In" text.
  - **Forgot Password Link**: Allows users to reset their password if forgotten.
  - **Sign Up Link**: A link to the account creation page for new users.
  - **SSO Login Option**: A “Login with SSO” link for users with enterprise accounts using Single Sign-On.
  
- **User Stories**:
  - As a user, I want to log in securely using my Google account.
  - As a user, I want to log in using my email/username and password combination.
  - As a user, I want to reset my password if I have forgotten it.

#### 3.3. Blog Page
- **Purpose**: Hosts articles, announcements, and other informative content related to the company or product.
- **Key Features**:
  - Blog posts displayed in reverse chronological order.
  - Pagination or infinite scroll to navigate through older posts.
  - A search bar to filter posts by keywords or topics.
  
- **User Stories**:
  - As a visitor, I want to browse blog articles to learn more about industry insights or product updates.
  - As a visitor, I want to search blog posts based on specific keywords.

#### 3.4. About Page
- **Purpose**: Provides information about the company, mission, team, and history.
- **Key Features**:
  - Content sections for the company mission, history, and team member profiles.
  - Images or media to complement the company’s story.
  
- **User Stories**:
  - As a visitor, I want to learn about the company’s mission and values.
  - As a visitor, I want to see profiles of the team members.

#### 3.5. Pricing Page
- **Purpose**: Displays pricing plans and details for users interested in purchasing services.
- **Key Features**:
  - Clear breakdown of different pricing tiers (e.g., Basic, Pro, Enterprise).
  - Feature comparison chart for each pricing tier.
  - Call-to-action buttons for sign-up or contacting sales for custom pricing.
  
- **User Stories**:
  - As a visitor, I want to compare pricing plans to choose the one that best suits my needs.
  - As a visitor, I want to contact sales for more information on custom pricing.

### 4. Functional Requirements

#### 4.1. General Features
- **Navigation**: A top navigation bar will be consistent across all pages, allowing users to move between Home, Login, Blog, About, and Pricing.
- **Responsive Design**: The site must be fully responsive and accessible across different device types (desktops, tablets, mobile).
- **Authentication**:
  - **Google OAuth 2.0**: Integration with Google OAuth for login.
  - **Traditional Login**: Secure login with email/username and password.
  - **SSO**: Single Sign-On integration for enterprise users.
  
#### 4.2. Login Page Features
- **Password Management**: Integration of "Forgot Password" functionality using an email recovery link.
- **Password Visibility**: Toggle option for hiding/showing password.
- **Error Handling**: Display appropriate error messages for incorrect credentials or connection issues.
- **Security**: All forms must be secure (e.g., SSL, secure password storage with encryption).

#### 4.3. API Integrations
- **User Authentication**: Integrate with Google OAuth 2.0 API.
- **Blog API**: Fetch blog post content from a backend API or Content Management System (CMS).
- **Pricing Data**: Dynamically retrieve and display pricing data, potentially from a CMS or database.

### 5. Non-Functional Requirements

#### 5.1. Performance
- The site must load within 2 seconds on average.
- The login authentication process should take less than 1 second for both Google OAuth and traditional logins.

#### 5.2. Security
- Use HTTPS and SSL for all communications.
- Implement CAPTCHA or similar anti-bot measures on the login page.
- Store user passwords securely (hash and salt using bcrypt or similar).

### 6. Wireframes and Visual Design

Provide wireframes for each page (Login, Home, Blog, About, Pricing) to visualize the layout and design expectations. These wireframes should include:
- Navigation bar placement.
- Call-to-action buttons.
- Content sections for each page.
- Login page design with Google Sign-In and traditional form.

