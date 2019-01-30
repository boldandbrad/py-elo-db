# Py-Elo-DB

py-elo is a python tool for calculating and storing elo values and statistics for two sided match-based games. All data is stored in a sqlite database structure that can be easily queried, though py-elo-db will do the heavy lifting for you.

## Dependencies
- peewee

## Installation
- clone repository
- requirements.txt is located
- activate your virtualenv
- run: 
```bash
pip3 install -r requirements.txt
```

## Usages
```bash
python3 main.py --help
```

## Examples

### Adding Match Data
The quickest way to get going with py-elo-db is to add a match. There's never a need to add new players/teams manually because py-elo-db will automatically store them for you if they don't already exist when you add a match. A mach can be added with `-m` or `--match`:
```bash
python3 main.py -m "Bulldogs 4 3 Grizzlies"
```
This will create and store new entries for Bulldogs and Grizzlies in the Player table, as well as a new record in the Match table with the score.

Optionally, you can add `OT` to denote the game went to overtime:
```bash
python3 main.py -m "Bulldogs 4 3 Grizzlies OT"
```


## License
[MIT](https://choosealicense.com/licenses/mit/)