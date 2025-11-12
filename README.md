# Mythic Access DnD API

A FastAPI-based backend for managing users, campaigns, dnd classes, dice sets and dice rolls — designed for tabletop and D&D-style applications.  
Built with PostgreSQL, JWT authentication, and rate limiting.

---


## Features

- Secure JWT authentication (`/auth`)
- User registration and management (`/users/`)
- Campaign and character class management (`/campaigns/`, `/classes/`)
- Dice roll and log tracking (`/dices/`, `/dicelogs/`)
- Create and roll dice sets (`/dicesets/`)
- PostgreSQL database
- Rate limiting with `slowapi`

---


## Environment Variables

Create a `.env` file in the project root with the following variables:

DATABASE_URL=your db url (e.g. postgresql://user:password@hostname:5432/dbname)
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=your algorithm
JWT_ACCESS_TOKEN_EXPIRE=your expiration time (e.g. 60)


On Render, set these under Environment → Environment Variables.

---


## Database Setup (Render PostgreSQL)

1.	On Render, create a PostgreSQL service.
2.	Copy the Internal Database URL.
3.	Paste it into your .env file as DATABASE_URL.
4.	Run migrations (if any) automatically on deploy.

---


## API Endpoints

- Authentication - 

POST - /auth/register - Register a new user

POST - /auth/token - Authenticate and receive JWT token


- Users -

GET - /users/me - Get current user profile

PATCH - /users/me/update - Update current user profile

DELETE - /users/me/delete - Delete current user account


- Campaigns -

GET - /campaigns - List all campaigns

GET - /campaigns/{id} - Get campaign by ID

POST - /campaigns - Create a new campaign

PATCH - /campaigns/{id} - Update campaign

DELETE - /campaigns/{id} - Delete campaign


- DnD Classes/Characters -

GET - /classes - List all character classes

GET - /classes/{id} - Get class by ID

POST - /classes - Create a new class

PATCH - /classes/{id} - Update class

DELETE - /classes/{id} - Delete class


- Dices -

GET - /dices - List all dices

GET - /dices/{id} - Get dice by ID

POST - /dices/{id}/roll - Roll a dice 


- Dice Sets -

GET - /dicesets - List all dice sets

GET - /dicesets/{id} - Get dice set by ID

POST - /dicesets - Create a dice set

PATCH - /dicesets/{id} - Update dice set

DELETE - /dicesets/{id} - Delete dice set

POST - /dicesets/{id}/roll - Roll a dice set


- Dice Logs -

GET - /dicelogs - List all dice logs from user ID 

GET - /dicelogs/{id} - Get a specific dice log from user ID


- Health Check - 

GET - /healthz - Basic health check endpoint for Render



## Rate Limiting

each endpoint is protected by rate limiting with slowapi → Each endpoint is protected by rate limiting via slowapi.



MIT License © 2025 Mythic Access DnD Project

