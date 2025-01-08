# How to contribute to zenopay python sdk

We welcome contributions to the Zenopay Python SDK. To contribute to this project, follow the steps below:

## Issues

If you find a bug in the code or have a feature request, please open an issue on the repository. Just click on the Issues tab and click on the New Issue button. Select the type of issue you are creating, write a title and description, and click Submit new issue.

Ensure the bug was not already reported by searching on GitHub under Issues.

## Changes

1. Fork the repository

In the top-right corner of this page, click Fork. This will create a copy of this repository in your account.

1. Clone the repository

    ```bash
    git clone https://
    ```

1. Create a virtual environment

    The project works with python >=3.8

    Use virtual environment as it allows you to work on a project without affecting the system's Python installation.

    ```bash
    python3 -m venv .venv
    ```

    Activate the virtual environment

    ```bash
    source .venv/bin/activate
    ```

1. Install the dependencies

    ```bash
    pip install -r requirements.txt
    ```

1. Set up pre-commit hooks

    ```bash
    pre-commit install
    ```

1. Make changes

    Make your changes to the codebase.

1. Run tests [Not yet implemented]

    This is to be implemented.

1. Commit your changes

    ```bash
    git commit -am 'Add new feature'
    ```

1. Push your changes

    ```bash
    git push
    ```

1. Create a pull request

    Go to your forked repository and click on the Pull Requests tab. Click on the New Pull Request button. Select the branch you made your changes on and click Create Pull Request.

1. Wait for review

    Wait for the maintainers to review your pull request. If there are any issues, you can make changes and push them to the same branch.

Hope this helps you contribute to the Zenopay Python SDK.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENCE) file for details.
