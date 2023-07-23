# NEGCO2

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About NEGCO2</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The Environment Sustainability project aims to create a web application that promotes and educates users about environmental sustainability. The project will provide information, resources, and tools to encourage individuals to adopt sustainable practices and make environmentally friendly choices in their daily lives. It will also facilitate collaboration and community engagement in environmental initiatives.

### Built With

- ![Flask][Flask]
- ![Tailwind][Tailwind]

## Getting Started

### Installation

_Below is an example of how to install and set up NEGC02._

1. Get a free API and Site Key at [https://www.hcaptcha.com/](https://www.hcaptcha.com/)
2. Set up your Database
3. Clone the repo

   ```sh
   git clone https://github.com/poonbing/IT2555---Application-Security.git
   ```

4. Install NPM packages

   ```sh
   npm install
   ```

5. Set up python virtual environment

   ```sh
   python -m venv venv
   ```

   ```sh
   source venv/bin/activate  # For Unix/Linux
   venv \Scripts\activate  # For Windows
   ```

6. Enter your API in `config.py`
   ```python
   SQLALCHEMY_DATABASE_URI = "ENTER DATABASE URI"
   XCAPTCHA_SITE_KEY = "ENTER API SITE KEY"
   XCAPTCHA_SECRET_KEY = "ENTER API SECRET KEY"
   ```
7. Enter your Email Username and Password
   ```python
    MAIL_USERNAME = "ENTER USERNAME"
    MAIL_PASSWORD = "ENTER PASSWORD"
   ```

## Usage

1. Run `run.py`
2. Go to 127.0.0.1:5000


_For more examples, please refer to the [Documentation](https://example.com)_

## Contributing

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/poonbing/IT2555---Application-Security](https://github.com/poonbing/IT2555---Application-Security)

## Acknowledgments

[Flask]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Tailwind]: https://img.shields.io/badge/Tailwind%20CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
