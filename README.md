# **2022 U.S. Hospital Services Areas(HSAs)**: Web Application with Multi-Page Navigation

**[HSAs](https://leoncensh-baho.hf.space) is a Healthcare AI data Analyst agent**. Uses gradio to prototype in Python. The agent analyzes U.S. prescription data from the Center of Medicare and Medicaid(CMS) to replicate papers from academic journals and articles from Kaiser Health News on U.S. prescription drug prices.

Web application with five primary subpages: **Home, Login, Blog, About, and Pricing**. The application allows to sign in using their Google account or traditional email and password credentials.

### Objectives
- To allow users to sign in using their Google account or standard login credentials.
- To inform visitors about the application through a blog, about section, and pricing page.
- To ensure the application is responsive, scalable, and secure.

### Pages Description and Requirements
#### Home Page
  - Clean, simple design with a prominent call to action(CTA).
  - A navigation bar allowing access to other subpages: Login, Blog, About, Pricing.
  - Footer with links to Terms of Service, Privacy Policy, and Contact Information.
  - As a visitor, I want to understand the purpose of the website immediately upon landing.

#### Login Page
  - **Google Sign-In Button**: Positioned at the top for easy access, allowing users to sign in using their Google account.
  - **Email/Password Form**: Traditional sign-in form with input fields for "Email or Username" and "Password".
    - Password visibility toggle (eye icon) to show/hide password input.
  - **Log In Button**: Standard button with clear "Log In" text.
  - **Forgot Password Link**: Allows users to reset their password if forgotten.
  - **Sign Up Link**: A link to the account creation page for new users.
  - **SSO Login Option**: A “Login with SSO” link for users with enterprise accounts using Single Sign-On.
  - As a user, I want to log in securely using my Google account.
  - As a user, I want to log in using my email/username and password combination.
  - As a user, I want to reset my password if I have forgotten it.

#### Blog Page
  - Blog posts displayed in reverse chronological order.
  - Pagination or infinite scroll to navigate through older posts.
  - A search bar to filter posts by keywords or topics.
  - As a visitor, I want to search blog posts based on specific keywords.

#### About Page
  - Content sections for the company mission, history, and team member profiles.
  - Images or media to complement the company’s story.
  - As a visitor, I want to see profiles of the team members.

#### Pricing Page
  - Clear breakdown of different pricing tiers (e.g., Basic, Pro, Enterprise).
  - Feature comparison chart for each pricing tier.
  - Call-to-action buttons for sign-up or contacting sales for custom pricing.
  - As a visitor, I want to compare pricing plans to choose the one that best suits my needs.

### Functional Requirements
- **Navigation**: A top navigation bar will be consistent across all pages, allowing users to move between Home, Login, Blog, About, and Pricing.
- **Responsive Design**: The site must be fully responsive and accessible across different device types (desktops, tablets, mobile).
- **Authentication**:
  - **Google OAuth 2.0**: Integration with Google OAuth for login.
  - **Traditional Login**: Secure login with email/username and password.
  - **SSO**: Single Sign-On integration for enterprise users.
  
#### Login Page Features And API Integrations
- **Password Management**: Integration of "Forgot Password" functionality using an email recovery link.
- **Password Visibility**: Toggle option for hiding/showing password.
- **Error Handling**: Display appropriate error messages for incorrect credentials or connection issues.
- **Security**: All forms must be secure (e.g., SSL, secure password storage with encryption).
- **User Authentication**: Integrate with Google OAuth 2.0 API.
- **Blog API**: Fetch blog post content from a backend API or Content Management System (CMS).
- **Pricing Data**: Dynamically retrieve and display pricing data, potentially from a CMS or database.

### Non-Functional Requirements
- The site must load within 2 seconds on average.
- The login authentication process should take less than 1 second.

### Wireframes and Visual Design
- Navigation bar placement.
- Call-to-action buttons.
- Content sections for each page.
- Login page design with Google Sign-In.
