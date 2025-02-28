<a id="readme-top"></a>

<div align="center">
  <a href="https://github.com/nu-quran-community/nu-quran-django">
    <img src="https://avatars.githubusercontent.com/u/186422981" alt="Logo" height="150" style="border-radius: 10px">
  </a>
  <h2 align="center">NU Quran API</h2>
  <p align="center">
    Backend API powering NU Quran community platform 🌙
    <p align="center">
      <a href="https://techforpalestine.org/learn-more"><img alt="StandWithPalestine" src="https://raw.githubusercontent.com/Safouene1/support-palestine-banner/master/StandWithPalestine.svg"></a>
      <img alt="GitHub License" src="https://img.shields.io/github/license/nu-quran-community/nu-quran-django">
      <img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/nu-quran-community/nu-quran-django/release.yml">
      <img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/nu-quran-community/nu-quran-django">
      <img alt="GitHub issues" src="https://img.shields.io/github/issues/nu-quran-community/nu-quran-django">
      <img alt="Python Version from PEP 621 TOML" src="https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fquickwrench%2Fquickwrench-api%2Fmain%2Fpyproject.toml">
    </p>
    <a href="#getting-started">Getting Started</a>
    ·
    <a href="https://github.com/nu-quran-community/nu-quran-django/issues">Report Bug</a>
    ·
    <a href="https://github.com/nu-quran-community/nu-quran-django/issues">Request Feature</a>

  </p>
</div>

## About The Project ✨

Backend API that powers the NU Quran Community platform, providing a structured and efficient way to manage donations, track student achievements, and facilitate community engagement. It serves as the core infrastructure for handling authentication, user data, contribution records, and achievement tracking.

### Key Features:

- 🏆 **Achievement Tracking** – Maintain student progress records, awarding points and achievements based on predefined criteria.
- 🔐 **Authentication & Authorization** – Ensure secure access with role-based permissions for administrators, students, and moderators.
- ⚡ **RESTful API** – Designed for seamless integration with frontend applications, allowing efficient data retrieval and updates.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<a id="getting-started"></a>

## Getting Started 🚀

Follow these steps to set up the project locally.

### Prerequisites 📦

- Python 3.12+

```sh
sudo apt install python3
```

- Docker (optional for containerized deployment)

```sh
sudo apt install docker.io
```

### Installation ⚙️

1. Clone the repo

```sh
git clone https://github.com/nu-quran-community/nu-quran-django.git
```

2. Navigate to the project directory

```sh
cd nu-quran-django
```

3. Set up a virtual environment and activate it

```sh
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies

```sh
pip install -r deps/requirements.prod.txt
```

5. Apply database migrations, load initial data, and prepare roles

```sh
python src/manage.py migrate
python src/manage.py loaddata category
python src/manage.py setuproles
```

6. Create a superuser for creating the first user

```sh
python src/manage.py createsuperuser
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage 🔧

Here is how to use the project:

1. Start the development server

```sh
python src/manage.py runserver
```

2. Visit `http://127.0.0.1:8000` in your browser.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing 👥

Contributions are welcome! To get started:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feat/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing-feature'`)
4. Push the branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License 📜

Distributed under the GPL v3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
