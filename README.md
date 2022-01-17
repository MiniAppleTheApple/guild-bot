# Guild BOT

## Features
- create a guild(not discord guild)
- invite member to the guild
- check the guild info
- check guild which user have created

## Usage

### Set up

create the `last_id.txt` and write
```
0
```
and create the `conf.toml` and write
```
[bot]
token = "TOKEN"
guild_ids = [GUILD_ID]
```

replace `TOKEN` as your token, and `GUILD_ID` as your guild

### Run
```
pipenv shell
```
and then
```
python3 main.py
```
or
```
python main.py
```
