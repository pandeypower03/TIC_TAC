



# Tic-Tac-Toe Game Backend with User Authentication and Match History

A robust backend API for a Tic-Tac-Toe game built with user management and game tracking capabilities. This system allows users to register, authenticate, play games against other users, and maintain their game history. The API implements secure user authentication using JWT tokens and provides comprehensive game management including move validation, win detection, and detailed match history tracking.






## API Reference

#### Register User

```http
 POST /api/register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. username for registration |
| `password`      | `string` | **Required**. password for registration |
| `email`      | `string` | **Required**. user email |



#### Login user

```http
  POST /api/token
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username` | `string` | **Required**. username |
| `password`      | `string` | **Required**. password  |

#### List Users
```http
  POST /api/token
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | `string` | **Required**. JWT token |

#### Get User Profile
```http
  GET /api/profile/me
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Authorization` | `string` | **Required**. JWT token |

#### Update Profile
```http
 PUT /api/profile/me
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token |
| `username` | `string` | **Optional**. New username |
| `email`      | `string` | **Optional**. New email|

#### Create Game
```http
 POST /api/games
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token |
| `player2_id` | `string` | **Required**. Opponent's ID |

#### Make Move
```http
 POST /api/games/${game_id}/make_move
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token |
| `position_x` | `number` | **Required**. Row coordinate (0-2) |
| `position_y` | `number` | **Required**. column coordinate (0-2) |

#### Get User Games
```http
 GET /api/games/my_games
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token |

#### Get Match History
```http
 GET /api/match-history
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. JWT token |
| `limit` | `number` | **Optional**. Number of records to return |
| `offset`      | `number` | **Optional**.Number of records to skip|
















## 🚀 About Me
As a passionate and detail-oriented backend developer, I specialize in designing, building, and optimizing scalable systems that power seamless user experiences. With hands-on experience in Python, Flask, Firebase, and database management, I focus on creating efficient, secure, and reliable backend solutions.

Whether it’s developing APIs, integrating third-party services, or ensuring robust data flow, I thrive on solving complex challenges and bringing innovative ideas to life. My work includes developing dashboards, implementing real-time analytics, and streamlining processes for improved performance and functionality.

I’m always excited to collaborate with dynamic teams, learn new technologies, and contribute to meaningful projects that make an impact. Let’s connect to discuss how we can create exceptional solutions together!


## Screenshots

When the players are playing TIC-TAC-TOE![Screenshot 2025-01-21 202352](https://github.com/user-attachments/assets/b247a64d-4b2f-4003-b316-9cc37aa4e812)


Win of a player![Screenshot 2025-01-21 202504](https://github.com/user-attachments/assets/35134a05-a129-4580-a493-96ece4d15894)


History of previous matches![Screenshot 2025-01-21 202526](https://github.com/user-attachments/assets/07ba1b1f-f36c-4a64-9644-64cd0a993772)





## Run Locally

To run this project locally

1.To start a project first make a new repository and then clone it through the command prompt [git clone project_name]

2.now open the tic-tak in vs code.

3.create a virtual environment 
```bash
[python -m venv venv]
```
4.now activating the virtual environment
```bash
[venv/scripts/activate]
```
5.now installing all the requirements for my porject  in the virtual environment
```bash
[pip install -r requirements.txt]
```
 my requirements.txt contains 

Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.0
python-dotenv==1.0.0

6.now make migrations 
```bash
[python manage.py makemigrations]
```
   Now migrate
```bash   
[python manage.py migrate]
```
7.Now create a superuser
```bash
[python manage.py createsuperuser]
```
Enter the required credentials-username,password,email-id

8.now open split powershell ,activate your environment , in first powershell run the server
```bash
[python manage.py runserver]
```
9. Make sure your server is running at port 8000 then in the second powershell run 
```bash
[python play_games.py]
```
10.now register player 1 and set password ,then register player 2 and set password ,both users will require a login using JWT then the game starts



## 🛠 Skills
Web Developer | Full Stack developer| BackEnd Specialist | HTML, CSS3 ,Bootstrap, JavaScript ,Python developer


## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/priyanka-pandey77/)



## Tech Stack

**Client:** React, React-axios, React-routing

**Server:** Django, Django-rest framework, JWT


## Demo

https://drive.google.com/file/d/1A7jk2P_5kfJ8ZGzsqMQn80JoaSrUJMWV/view?usp=sharing


