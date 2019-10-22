# Internal Approval System
Internal Approval System is a backend system where people from different level can approve a project. If people from all levels approve the project, a message is published. This is a minimalistic blockchain system with minimalistic smart contract.

## Getting Started
### Prerequisites
- Python 3.7
- Django 2.2
- [Django REST 3.10.3](https://pypi.org/project/djangorestframework/) (install from PIP should be okay)
- [PyCrypto 2.6.1](https://pypi.org/project/pycrypto/) (install from PIP should be okay)

## Running Tests
Just run `python3 manage.py test`

## Authors
- [Giovanni Dejan](github.com/iamdejan)

## FAQ
1) **Question**: Why not use Ethereum's Solidity?
**Answer**: I want to learn the core concept of Blockchain, so I don't use Solidity.
2) **Question**: How do you check if the approval is valid?
**Answer**: During the approval creation request (process where user can approve a project), I can check whether the sent data is valid / not, based on sent signature. During the blockchain validation, I can check if the block is valid (not tempered) and check again the given signature.

## TODO: In The Future
- Publish the message, so client can notice.
- Create the frontend system (in separate repo).
- Add documentation.