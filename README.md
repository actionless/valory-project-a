# Dev-template

A template for development with the open-autonomy framework. Find the documentation [here](https://docs.autonolas.network).

## System requirements

- Python `>=3.8`
- [Tendermint](https://docs.tendermint.com/v0.34/introduction/install.html) `==0.34.19`
- [IPFS node](https://docs.ipfs.io/install/command-line/#official-distributions) `==0.6.0`
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Poetry](https://python-poetry.org/)
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Alternatively, you can fetch this docker image with the relevant requirements satisfied:

> **_NOTE:_**  Tendermint and IPFS dependencies are missing from the image at the moment.

```bash
docker pull valory/open-autonomy-user:latest
docker container run -it valory/open-autonomy-user:latest
```

## This repository contains:

- A directory, `packages`, which acts as the local registry

- Pre-filled in third-party core packages

- Basic example of a simple skill, a chained skill, an agent and a service

- .env sample file with Python path updated to include packages directory

## How to use

1. Create a virtual environment with all development dependencies:

    ```bash
    poetry shell
    poetry install
    autonomy packages sync --update-packages
    ```

2. Prepare an `ethereum_private_key.txt` (for agents) file and `keys.json` (for services) files containing wallet address and/or the private key for each of the agents. You can generate a new key by running `autonomy generate-key ethereum`. This is how those files hsould look like:

    ethereum_private_key.txt (check that there are no newlines at the end)

    ```
    0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a
    ```

    keys.json
    ```
    [
        {
            "address": "0x15d34AAf54267DB7D7c367839AAf71A00a2C6A65",
            "private_key": "0x47e179ec197488593b187f80a00eb0da91f1b9d0b13f8733639f19c30a34926a"
        }
    ]
    ```

3. Modify `packages/author/agents/demo_agent/aea-config.yaml` so `all_participants` contains your agent's public address.


5. Make a copy of the env file:

    ```cp sample.env .env```

5. Fill in the required environment variables in .env. You'll need a Ethereum RPC. `ALL_PARTICIPANTS` needs to contain your agent's public address.


6. Test the agent

    ```bash
    bash run_agent.py
    ```

    and in other terminal run Tendermint:

    ```bash
    make tm
    ```

7. Test the service

    ```bash
    bash run_service.py
    ```

8. Get developing...

## Useful commands:

Check out the `Makefile` for useful commands, e.g. `make formatters`, `make generators`, `make code-checks`, as well
as `make common-checks-1`. To run tests use the `autonomy test` command. Run `autonomy test --help` for help about its usage.


## Python Software Engineer - Project A

### Instructions

Your task, should you choose to accept it, is to implement an autonomous agent.
Autonomous agents have a number of defining characteristics:
- Communicate with the environment via asynchronous messages
- Display reactiveness (handling messages) and proactiveness (generating new
messages based on internal state or local time)
- Can be thought of as representing a human, organisation, or thing in a specific
domain and tasks

Your autonomous agent should support these operations and characteristics:
- Continuously consume messages (of different types) from an InBox
- Emit messages to an OutBox
- Allow for registration of message handlers to handle a given message type with its
specific handler (reactive: if this message then that is done)
- Allow for registration of behaviours (proactive: if this internal state or local time is
reached then this message is created)

Once the generic autonomous agent exists, create a concrete instance which:
- Has one handler that filters messages for the keyword “hello” and prints the whole
message to stdout
- Has one behaviour that generates random 2-word messages from an alphabet of
10 words (“hello”, “sun”, “world”, “space”, “moon”, “crypto”, “sky”, “ocean”, “universe”,
“human”) every 2 seconds

Run two instances of your concrete agents where the InBox of agent 1 is the OutBox of
agent 2 and vice versa.

Write one unit and one integration (both agents) test.

When you’re finished, submit a PR in a Github repository of your choosing and assign GH
handles dvilelaf - angrybayblade - dagacha as reviewers.

### Notes

- Imagine you’re submitting a PR to a production project you’re working on
- The design is light on details intentionally – we encourage you to make
clarifications and request changes
- Actual designs in the course of normal work at Valory would be much more fleshed
out
- We recommend using only pure Python3 and its standard libraries
- Include some notes in the PR to walk us through any choices you needed to make
or any feedback you have on the design
- Ideally you would spend no more than 3 hours implementing
