# trellolo [![Build Status](https://www.travis-ci.com/jamrok/trellolo.svg?branch=master)](https://www.travis-ci.com/jamrok/trellolo) ![Codecov](https://img.shields.io/codecov/c/github/jamrok/trellolo.svg)

  Basic Trello CLI that allows for easy:
  - Board: showing, adding, deleting
  - List: showing
  - Card: showing, adding, deleting, adding/deleting comments, adding/deleting labels

## Contributors
  - Author: Jamrok

## Supporting Docs
  - [Trello API Reference]( https://developers.trello.com/reference/ )
  - [Steps for obtaining Trello API Key and Token]( https://developers.trello.com/docs/api-introduction )

## Assumptions
  - You have an Trello Account 🙂

## Precautions
  - There is no *dry-run* for delete operations 😅

## Rollback
  - Anything you accidentally delete will need to be recreated manually.

## Prerequisites
  - python >= 3
  - pip3
  - tox
  - git (optional)

## Compatibility
  - python 3.6 - Verified
  - python 3.7 - Verified

## Syntax
```bash
$ trellolo
Usage: trellolo [OPTIONS] COMMAND [ARGS]...

  CLI for interacting with the Trello API

Options:
  -k, --api-key TEXT  Your Trello API key
  -t, --token TEXT    Your Trello token
  -h, --help          Show this message and exit.

Commands:
  board   Interact with boards
  card    Interact with cards
  config  Save Trello API key to the trellolo config file.
  list    Interact with lists

```

---

## Installation

#### Setup TOX
```bash
pip3 install tox
```

#### Download the trellolo repo
```bash
git clone https://github.com/jamrok/trellolo.git
cd trellolo
```
#### Have tox setup the virtual environment
```bash
tox -e py3
source .tox/py3/bin/activate
```

---

## Using your [Trello API Key and Token]( https://developers.trello.com/docs/api-introduction )
There are three ways to utilize your credentials, choose any of the options below:
#### 1. Set environment variables
```bash
read -s -p "Paste Key: " TRELLO_KEY
read -s -p "Paste Token: " TRELLO_TOKEN
export TRELLO_KEY TRELLO_TOKEN
```
###### Note:
1. To test your credentials, run: `trellolo board show --all`
1. To view your credentials, run: `env | grep TRELLO_`
1. To remove your credentials, run: `unset TRELLO_KEY TRELLO_TOKEN`

#### 2. Supply command like options that include your credentials
```bash
read -s -p "Paste Key: " key1
read -s -p "Paste Token: " token1
```
###### Note:
1. To test your credentials, run: 
  `trellolo -k $key1 -t $token1 board show --all`
1. To view your credentials, run: `set | grep "key1\|token1"`
1. To remove your credentials, run: `unset key1 token1`

#### 3. Save your credentials to a file
```bash
trellolo config 
Enter API key:
Enter Token:
Saved API key to ~/.trellolo.cfg
```

###### Sample `~/.trellolo.cfg` contents:
```bash
{'key': 'BLAHBLAHBLAHBLAHBLAH', 'token': 'xyz123gibberishxyz123gibberishwxyz123gibberishxyz123gibberishxyz'}
```

#### ✨ 🍰 ✨ Trellolo is all setup! Enjoy ✨ 🍰 ✨

---

## Examples

#### How to show all cards on all lists on all boards
```bash
$ trellolo card show --all
Board ID: 5c6hfvhjkfuhikjl45tgnk27 | Name: Board with no lists
  🗋 No lists are on this board.

Board ID: 5cdsfghhjhg787iujh86454e | Name: Board with one list but no cards
  📄 List ID: 5c6b993fa3eabe2af426aa2a | Name: List with no cards
    🃠 No cards are on this list.

Board ID: 5cg46ujhnbfrteyujgnbgdte | Name: RANDOM
  📄 List ID: 5cgida4508hdu590hu85309a | Name: Stuff
    🃪 Card ID: 5c4jk35y3743k23hc74846e3 | Name: To Do
      🏷  Label(s): ['green', 'orange', 'sky', 'yellow', blue', 'purple', 'red']
        💭  Comment ID: 5c72fa330f4c0b8bd50a2799 | Name: Jamrok | Date: 2019-02-25T23:05:27.844Z | Text: Fixed!
        💭  Comment ID: 5c72fa305cf82e3a0e47ef9e | Name: Jamrok | Date: 2019-02-25T23:05:24.806Z | Text: What! No comments!???

```
---

#### Show all boards

```bash
$ trellolo board show --all
Board ID: 5c6hfvhjkfuhikjl45tgnk27   Board Name: Board with no lists
Board ID: 5cdsfghhjhg787iujh86454e   Board Name: Board with one list but no cards
Board ID: 5cg46ujhnbfrteyujgnbgdte   Board Name: RANDOM

```
---

#### How to add a board
```bash
$ trellolo board add
Usage: trellolo board add [OPTIONS]

  Create a new board.

Options:
  -n, --name TEXT
  -h, --help       Show this message and exit.
```

---

#### How to add a card
```bash
$ trellolo card add --help
Usage: trellolo card add [OPTIONS]

  Adds a card to a specified list on a given board.

Options:
  -t, --title TEXT                [required]
  -d, --description, --desc TEXT
  -l, --list_id TEXT              [required]
  -c, --labels [yellow|purple|blue|red|green|orange|black|sky|pink|lime|null]
  -h, --help                      Show this message and exit.
```

---

#### How to add a comment to a card 
```bash
$ trellolo card add_comment -h
Usage: trellolo card add_comment [OPTIONS]

  Add a comment to a card

Options:
  -i, --id TEXT       Card ID  [required]
  -c, --comment TEXT  Comment Text  [required]
  -h, --help          Show this message and exit.
```
