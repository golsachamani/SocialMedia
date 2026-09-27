# 🔴 RedditClone — Community-Based Social Platform

A **Reddit-inspired** social media platform built with **Django**. Users can create communities (subreddits), join them, submit posts, vote on posts and comments, and take part in nested comment discussions.

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Data Models](#-data-models)
- [Installation & Setup](#-installation--setup)
- [Main Routes](#-main-routes)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 👤 Authentication & Users
- User registration and login (customized `UserCreationForm`)
- Profile editing (first name and last name)
- Password change with confirmation (Password Change / Done)
- Logout

### 🏘️ Communities
- Create, update, and delete communities
- Automatic unique **slug** generation for each community
- Join / leave communities
- Member role system: `Member` and `Moderator`
- A community can only be deleted by its creator, and only if it has no posts
- Displays the list of communities the current user owns or belongs to

### 📝 Posts & Comments
- Create, update, and delete posts within each community
- **Self-referencing** structure for comments: every comment is itself a `Post` with a `parent`, enabling unlimited nested discussions
- Comments rendered as a tree (`comment_recursive.html`)
- Smart redirection back to the root of a discussion after adding, editing, or deleting a comment (`get_grandparent_absolute_url`)

### ⬆️⬇️ Voting System
- Upvote / downvote on posts
- Toggle logic: clicking the same vote again removes it; clicking the opposite vote replaces it
- Post score computed as the sum of all votes

### 💾 Other Modeled Features
- **Save** — bookmark posts to view later
- **Report** — flag inappropriate posts with a reason and a resolution status

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend Framework | Django |
| Database (development) | SQLite3 |
| Templating | Django Template Language (DTL) |
| Authentication | Django Auth (default `User` model) |

---

## 📂 Project Structure

```
├── accounts/                  # Authentication & user profile app
│   ├── forms.py                # Registration and profile editing forms
│   ├── models.py
│   ├── templates/accounts/
│   ├── urls.py
│   └── views.py
│
├── config/                    # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── templates/base.html     # Shared base template
│
├── socialmedia/                # Core app: communities, posts, voting
│   ├── models.py               # Community, Post, Vote, Membership, Save, Report
│   ├── forms.py
│   ├── templates/
│   ├── urls.py
│   └── views.py
│
├── db.sqlite3
└── manage.py
```

---

## 🗃️ Data Models

### `Community`
Communities (equivalent to subreddits). Has a unique name, description, creator, and an auto-generated slug.

### `Membership`
Relationship between a user and a community, with a role (`member` / `moderator`).

### `Post`
Both posts **and comments** are built from this same model; the self-referencing `parent` field determines whether an item is a root post or a reply to another post/comment.

### `Vote`
A user's vote on a post (`+1` or `-1`), with a uniqueness constraint per user per post.

### `Save` and `Report`
Bookmarking and reporting of posts by users.

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create an admin user (optional)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

The project will be available at:
```
http://127.0.0.1:8000/
```

> ⚠️ If `requirements.txt` doesn't exist yet, generate it with `pip freeze > requirements.txt`.

---

## 🔗 Main Routes

### Accounts

| Route | Name | Description |
|---|---|---|
| `/register/` | `register` | Register a new user |
| `/login/` | `login` | Log in |
| `/logout/` | `logout` | Log out |
| `/profile/` | `profile` | Edit profile |
| `/password/` | `password_change` | Change password |
| `/password/done/` | `password_change_done` | Password change confirmation |

### Social Media

| Route | Name | Description |
|---|---|---|
| `/` | `home` | Home page (feed of the user's communities) |
| `/communities/` | `community_list` | List of all communities |
| `/r/add/` | `community_add` | Create a new community |
| `/r/<slug>/` | `community_detail` | Community detail page |
| `/r/<slug>/update/` | `community_update` | Update a community |
| `/r/<slug>/delete/` | `community_delete` | Delete a community |
| `/r/<slug>/join/` | `community_join` | Join a community |
| `/r/<slug>/leave/` | `community_leave` | Leave a community |
| `/r/<slug>/add/` | `post_add` | Create a new post |
| `/r/<slug>/<post_slug>/` | `post_detail` | Post detail and comments |
| `/r/<slug>/<post_slug>/update/` | `post_update` | Update a post |
| `/r/<slug>/<post_slug>/delete/` | `post_delete` | Delete a post |
| `/r/<slug>/<post_slug>/comments/add/` | `comment_add` | Add a new comment |
| `/r/<slug>/<post_slug>/vote/<up\|down>/` | `toggle_vote` | Vote on a post |

---

## 🗺️ Roadmap

- [ ] Global search (communities and posts)
- [ ] Image uploads for posts and profiles
- [ ] Moderation panel for handling reports
- [ ] Notifications for votes and new comments
- [ ] Saved posts page
- [ ] Pagination for the feed and comment lists
- [ ] Convert to a REST API (Django REST Framework)

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a new branch: `git checkout -b feature/feature-name`
3. Commit your changes: `git commit -m 'Add feature X'`
4. Push the branch: `git push origin feature/feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ and Django</p>
