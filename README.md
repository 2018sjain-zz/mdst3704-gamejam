# mdst3704-gamejam

Horror Factory: Scavenge of Terror is a Discord bot developed in Python. Horror Factory allows players to navigate through a haunted factory containing a treacherous monster let loose. In the factory, there are many rooms in which players must repair essential items in order to successfully escape. Having your sound on (head/earphones) is a must when beginning your journey in the Horror Factory, and keeping track of your time limit is crucial as well.

## Installation

Use the following command to install this library.

```bash
git clone https://github.com/2018sjain/mdst3704-gamejam
```

## Usage

Run bot.py using python3.

```bash
python3 bot.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

Contribute by including new Commands in the cogs/voice.py file. An example command is included below.

```python
@commands.command()
async def example(self, ctx):
    await ctx.send("Ran example command.")
    print("Ran example command.")
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
