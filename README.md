# SmartFinance (Backend Only)
SmartFinance is a **personal finance management backend** system designed to help users track and analyze their financial activities. It allows users to register incomes and expenses, view aggregated summaries, and receive AI-powered insights based on their financial data and reference documents. This backend can be integrated with any frontend (web or mobile) to provide a full-featured personal finance application.

## Technologies

- Python 
- Django 
- Django REST Framework
- PostgreSQL
- JWT (Simple JWT)
- LangChain + OpenAI (RAG)
- Chroma Vector Store

## API Endpoints


| Resource        | Method | URL                        | Description                                   |
|-----------------|--------|----------------------------|-----------------------------------------------|
| **Authentication** | POST | `authentication/token/`             | Obtain JWT access and refresh tokens         |
|                  | POST   | `authentication/token/refresh/`     | Refresh JWT access token                      |
|                  | POST   | `authentication/token/verify/`      | Verify JWT token                              |
| **Users**        | POST   | `users/`                 | Create a new user                             |
|                  | GET    | `users/`                 | List all users                                |
|                  | GET    | `users/<int:pk>/`        | Retrieve a specific user                      |
|                  | PATCH  | `users/<int:pk>/`        | Update user information                       |
|                  | DELETE | `users/<int:pk>/`        | Delete a user                                 |
| **Incomes**      | GET    | `income/`               | List all incomes                              |
|                  | POST   | `income/`               | Create a new income                           |
|                  | GET    | `income/<int:pk>/`      | Retrieve a specific income                    |
|                  | PATCH  | `income/<int:pk>/`      | Update an income                              |
|                  | DELETE | `income/<int:pk>/`      | Delete an income                              |
|                  | GET    | `income/dashboard/`     | Get aggregated income dashboard               |
| **Expenses**     | GET    | `expense/`              | List all expenses                             |
|                  | POST   | `expense/`              | Create a new expense                          |
|                  | GET    | `expense/<int:pk>/`     | Retrieve a specific expense                   |
|                  | PATCH  | `expense/<int:pk>/`     | Update an expense                             |
|                  | DELETE | `expense/<int:pk>/`     | Delete an expense                             |
|                  | GET    | `expense/dashboard/`    | Get aggregated expense dashboard              |
| **AI Insights**  | POST   | `insights/`             | Generate financial insights based on user data and reference PDFs |

