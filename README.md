# CV Bot

### **Description:**

This Telegram Bot helps users to create a CV (Curriculum Vitae) in a chat format. By intercating with the Bot, a user can type required information to each CV section (**Personal Information, About me, Work Experience, Education and Skills**) - and then review and edit this information if necessary. 
At the end, the bot provides an output **PDF file** with CV information. 

[![Button-5.png](https://i.postimg.cc/Zq57h51F/Button-5.png)](https://t.me/thebest_cv_bot)

[![Git-Hub-pic.jpg](https://i.postimg.cc/NM9Qz0NH/Git-Hub-pic.jpg)](https://postimg.cc/xJQrk9Vf)

### **Tools used:**

- Python (pyTelegramBotAPI, regex)
- PostgreSQL
- HTML/CSS
- Docker

## **Why this project?**

This project was assigned to me as a part of **Entrepreneurship course in my Master's program at the UE for Applied Sciences**. 

With my team including other groupmates, we needed to create any relevant business model. 
We decided to develop a **Telegram bot** for CV creation. **Why?**

- A lot of employees, especially young professionals, struggle with designing their CV and demonstrating their strenghts in a concise way. 
- Existing online resources for creating a resume generally lack UX/UI in mobile versions.
- There is a concern about data security issues on such resources.

Thus, the **CV Bot** aims to provide user-friendly, reliable step-by-step guide to creating user's CV. 

## **Project overview**

1. **Setting up and developing the Telegram bot**

The bot logic includes handlers and functions triggered by particular commands. User-frienly and convenient UX/UI is created for a more understandable interaction with the bot. User imput data is validated
through Python regular expressions and stored in a dictionary.

2. **Deploying a PostgreSQL database**

A PostgreSQL database is deployed to manage and store the structured user data collected in a Python dictionary. It includes personal information, educational background, work experiences, and skills. 

3. **PDF file design and structure using HTML/CSS**

Designing provides flexibility in modifying the layout and appearance of the information, making it easy to customize the CV to meet the individual's preferences. 

4. **Automating insertion and modification of HTML content**

The process of inserting, modifying and updating HTML content and elements within the CV is automated. This system ensures that each user's information is accurately reflected in the CV. By dynamically adapting the CV, a personalized and tailored document is provided for each user.

5. **Deploying the bot and its components on a server**

The Telegram bot and its associated components are deployed on a `fly.io` server. The bot now is accessible for users allowing them to interact with it and generate their customized CVs. 

## **Notes**

Ensure the correct setup of the PostgreSQL database, proper configuration of environment variables (`API_TOKEN`, `PAYMENT_TOKEN`, `DATABASE_URI`) in order to connect to Telegram Bot API and PostgreSQL database, and installation of dependencies as in `requirements.txt`. 





