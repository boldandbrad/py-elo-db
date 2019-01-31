# Py-Elo-DB

py-elo is a python tool for calculating and storing elo values and statistics for two sided match-based games. All data is stored in a sqlite database structure that can be easily queried, though py-elo-db will do the heavy lifting for you.

## Dependencies
- peewee

## Installation
- clone repository
- create and activate a virtualenv
- run: 
```bash
pip3 install -r requirements.txt
```

## Usages
```bash
python3 main.py --help
```

## Examples
The quickest way to get going with py-elo-db is to add the outcome of a match. There is never a need to manually add new players/teams because py-elo-db will automatically store them for you if they don't already exist when you add a match.

A match can be added with `-m` or `--match`:
```bash
python3 main.py -m "Bulldogs 4 3 Grizzlies"
```
This will create and store new entries for Bulldogs and Grizzlies in the Player table, as well as a new record in the Match table with the score and other relevant data.

Optionally, you can add `SD` to denote the game went to sudden death overtime:
```bash
python3 main.py -m "Bulldogs 4 3 Grizzlies SD"
```


## License
[MIT](https://choosealicense.com/licenses/mit/)