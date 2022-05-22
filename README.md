Django Blog
======
This is a Blog app made with Django, has all features typical for blog app.
Project has whole web application and also API made by Django Rest Framework which cover all features.

Project created to increase coding skill in Django framework.

## Install

```sh
git clone https://github.com/PawelMichnowicz/Django-Blog-site.git
pip install -r requirement.txt
```

## Usage

```sh
py manage.py migrate
py manage.py runserver
```

## Features 
- User Authentication system :\
Registration, Login/Logout, Password change, Passowrd reset (by email)
- Posts :\
Create, Edit(by author), Delete(by author)
- Comments
- Number of views for posts and users
- Like button using Ajax
- Scroll Pagination using Ajax
- Activity log
- List of posts in choosen order 
- List of posts created by particular user 

## Appearance of application
Main page:
![A-main](https://user-images.githubusercontent.com/83020761/169698059-9964a8aa-ebcf-4abb-b438-25de61175bdb.gif)


List of posts:
![A-list](https://user-images.githubusercontent.com/83020761/169698241-87ccdb2b-9d20-4146-99d6-7b715cab643e.gif)


Detail post view:
![image](https://user-images.githubusercontent.com/83020761/169698332-fda4d9c9-5b4a-4d1a-90d4-9907fce195e1.png)
