import discord
from discord.ext import commands
import random
import time
import os

class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.current_game = ""
        self.games_data = ("security", "worker facilities", "entrance", "gears", "wiring", "switchboard left", "switchboard right")
        self.time = 0
        self.gears_data = 0
        self.wires_data = (("A", "E"), ("B", "C"))
        self.wires_status = list()
        self.riddle_data = ("What has many teeth, but cannot bite?", ("comb", "Comb", "brush", "Brush"))
        self.song_data = ("./assets/stayingalive.mp3", ("staying", "Staying", "Stayin","stayin"))
        self.panning_data = 0
        self.panning_status = 0
        self.pitch_left = 0
        self.pitch_right = 0
        self.game_status = False

    @commands.command()
    async def join(self, ctx):
        self.game_status = True
        self.time = 10
        self.current_game = "entrance"
        self.gears_data = random.randint(1, 4)
        self.panning_data = random.randint(1, 7)
        self.panning_status = random.randint(1, 7)
        self.pitch_left = random.randint(1, 7)
        self.pitch_right = random.randint(1, 7)
        self.wires_status = list()
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send("Command to runner checking in. Confirming audio and visual. Right, everything looks good. You were already briefed but I’ll go over it again. Basically 2 weeks ago, the settlement stopped receiving auxiliary power from this nuclear plant. Our batteries and generators are running low, the team camped there hasn’t checked in for a few days. They said waste collection was becoming an issue. We need you to head in and make sure everything is alright. Fingers crossed, but in the event that there was a build up of radioactive waste, you are gonna want to limit your time in the building. Just head inside, check with the team, and do what you can to get this place running.")
        await ctx.send(file=discord.File('./assets/entrance.png'))
        await ctx.send("Commands: /goto {room}")
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/join.wav"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        print(f"Joined {ctx.author.name}'s voice channel.")

    @commands.command()
    async def leave(self, ctx):
        self.game_status = False
        await ctx.voice_client.disconnect()
        print("Left voice channel.")

    @commands.command()
    async def goto(self, ctx, *games):

        game_name = (' '.join(games)).lower()

        if game_name not in self.games_data:
            return

        mapping = {"entrance": {"entrance": 0, "gears": 2, "wiring": 3, "security": 1, "worker facilities": 2, "switchboard left": 2, "switchboard right": 3},
                   "gears": {"entrance": 2, "gears": 0, "wiring": 3, "security": 1, "worker facilities": 2, "switchboard left": 2, "switchboard right": 3},
                   "wiring": {"entrance": 3, "gears": 3, "wiring": 0, "security": 2, "worker facilities": 3, "switchboard left": 2, "switchboard right": 1},
                   "security": {"entrance": 1, "gears": 1, "wiring": 2, "security": 0, "worker facilities": 1, "switchboard left": 1, "switchboard right": 2},
                   "worker facilities": {"entrance": 2, "gears": 2, "wiring": 3, "security": 1, "worker facilities": 0, "switchboard left": 1, "switchboard right": 3},
                   "switchboard left": {"entrance": 3, "gears": 3, "wiring": 2, "security": 2, "worker facilities": 1, "switchboard left": 0, "switchboard right": 2},
                   "switchboard right": {"entrance": 3, "gears": 3, "wiring": 1, "security": 2, "worker facilities": 3, "switchboard left": 2, "switchboard right": 0} }

        prev_game = self.current_game
        self.current_game = game_name

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        await self.reduce_time(ctx, mapping[prev_game][self.current_game])
        if self.game_status == False: return

        if self.current_game == "entrance":
            await ctx.send(file=discord.File('./assets/entrance.png'))
            await ctx.send('This is the entrance.')
        elif self.current_game == "gears":
            await ctx.send(file=discord.File('./assets/gears.png'))
            await ctx.send('This is the gear room, but something sounds off in here. Like, more so than usual. Looks like you have access to four of the major gear networks labeled 1, 2, 3, and 4. Maybe if you /crank the gears you can figure out which one to /repair. Careful though, making too many changes might draw... unwanted attention.')
            await ctx.send("Commands: /crank {int}, /repair {int}")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/gears.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        elif self.current_game == "wiring":
            await ctx.send(file=discord.File('./assets/wiring.png'))
            await ctx.send("God… it's a mess in here. Is that, is that blood all over the walls? You know what, don't answer that. It looks like the monster cut a bunch of /wires as it tore through this place, maybe if you can reconnect two pairs of terminals (A, B, C, D, E), we can get the circuits running again.")
            await ctx.send("Commands: /wires {char} {char}")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/wires.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        elif self.current_game == "security":
            await ctx.send(file=discord.File('./assets/security.png'))
            await ctx.send("This is the security hub, looks like you are gonna have to unlock this place before you can go anywhere else. There's probably a way to shut down the SOS sequence. Look there, on that screen, it looks like a /riddle.")
            await ctx.send("Commands: /riddle {string}")
            await ctx.send(self.riddle_data[0])
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/security.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        elif self.current_game == "worker facilities":
            await ctx.send(file=discord.File('./assets/worker.png'))
            await ctx.send("I think this is the kitchen. Most of the food in here is probably rotten though… hey what's that sound?")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/song1.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(1)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.song_data[0]))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(1)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/song2.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send("It's a radio! Incredible, it hasn't died yet. God I love this /song, but I can’t remember the name. Do you know it? You can try to /replay it if you need to.")
            await ctx.send("Commands: /song {string}, /replay")
        elif self.current_game == "switchboard left":
            await ctx.send(file=discord.File('./assets/switch_left.png'))
            await ctx.send("I think this is one of the switchboard rooms. At least, it was… most of the stuff here is torn apart. Luckily, The primary components are hidden behind those panels on the wall. Try to listen for which panel is putting out there error sound and fix it.")
            await ctx.send("Commands: /walk {left/right} {int}, /open")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/panning.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(1)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.get_pan_file()))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        elif self.current_game == "switchboard right":
            await ctx.send(file=discord.File('./assets/switch_right.png'))
            await ctx.send("Alright, Switchboard Right, we are looking for a sliding control panel. There it is, the required input is sending out a signal in the form of that sound, try to make the second sound match the pitch of the first one and that should be it!")
            await ctx.send("Commands: /slide {left/right} {up/down} {int}, /pitch {left/right}, /match")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/pitch.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    async def reduce_time(self, ctx, tyme):
        self.time -= tyme
        if self.time <= 0:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/rip.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(1)
            await ctx.send(file=discord.File('./assets/died.png'))
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/hq.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(1)
            await self.leave(ctx)
            return
        elif self.time <= 4 and self.time >= 3:
            while ctx.voice_client.is_playing():
                time.sleep(.5)
            filename = random.choice(('close1.wav', 'close2.wav'))
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/monster/" + filename))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(.5)
        elif self.time <= 8 and self.time >= 7:
            while ctx.voice_client.is_playing():
                time.sleep(.5)
            filename = random.choice(('far1.wav', 'far2.wav', 'far3.wav', 'far4.wav'))
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/monster/" + filename))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(.5)
        await ctx.send(f"You have {self.time} hours left.")

    @commands.command()
    async def crank(self, ctx, gear_number):
        if self.current_game != "gears":
            await ctx.send("Wrong command! You are not in the Gears Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        filename = "./assets/gear_faster.mp3"
        if int(gear_number) == self.gears_data:
            filename = "./assets/gear_fast.mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def repair(self, ctx, gear_number):
        if self.current_game != "gears":
            await ctx.send("Wrong command! You are not in the Gears Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if int(gear_number) == self.gears_data:
            await ctx.send("Thats it! Finally, we should move on. I don’t want you in here any longer than you have to be.")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/gears_right.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            return
        else:
            await ctx.send("No, I don't think that was it, and we had to spend so much time too. Let's hope whatever is in here hasn’t been tracking your scent. Try again.")
            await self.reduce_time(ctx, 0.5)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/gears_wrong.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def wires(self, ctx, terminal_one, terminal_two):
        if self.current_game != "wiring":
            await ctx.send("Wrong command! You are not in the Wires Room.")
            return

        terminal_one = terminal_one.upper()
        terminal_two = terminal_two.upper()

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        active_wires = set()
        for pair in self.wires_data:
            active_wires.add(pair[0])
            active_wires.add(pair[1])

        filename = ""

        if (terminal_one, terminal_two) in self.wires_data or (terminal_two, terminal_one) in self.wires_data:
            filename = "./assets/wires_ss.mp3"
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            while ctx.voice_client.is_playing():
                time.sleep(1)
            if len(self.wires_status) == 0:
                self.wires_status.append((terminal_one, terminal_two))
                await ctx.send("Great job! You need to find one more wire pair.")
            elif len(self.wires_status) == 1:
                self.wires_status.append((terminal_one, terminal_two))
                await ctx.send("Nice! A model electrician you are, hopefully next will be something less, shocking. Get it? Just trying to lighten the mood. Try not to get gore on your shoes on the way out.")
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/wires_right.wav"))
                ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        elif terminal_one in active_wires and terminal_two in active_wires:
            filename = "./assets/wires_ssf.mp3"
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            await self.reduce_time(ctx, 0.1)
        elif terminal_one in active_wires or terminal_two in active_wires:
            filename = "./assets/wires_sf.mp3"
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            await self.reduce_time(ctx, 0.1)
        else:
            filename = "./assets/wires_ff.mp3"
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            await self.reduce_time(ctx, 0.1)

    @commands.command()
    async def riddle(self, ctx, answer):
        if self.current_game != "security":
            await ctx.send("Wrong command! You are not in the Security Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if answer in self.riddle_data[1]:
            await ctx.send("Great, that's the first step down. Now we should move on to the rest of the factory.")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/security_right.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            return
        else:
            await ctx.send("No, that's not it. Come on, I think I'm seeing some movement in the camera feeds behind you.")
            await self.reduce_time(ctx, 0.5)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/security_wrong.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def song(self, ctx, answer):
        if self.current_game != "worker facilities":
            await ctx.send("Wrong command! You are not in the Worker Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if answer in self.song_data[1]:
            await ctx.send("Yeah, that's right! Hey pick up the radio for me. I think I can use it for something.")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/song_right.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            await ctx.send("Radio Acquired!")
            return
        else:
            await ctx.send("No, I don’t think that’s it. We should probably keep moving.")
            await self.reduce_time(ctx, 0.5)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/song_wrong.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def replay(self, ctx):
        if self.current_game != "worker facilities":
            await ctx.send("Wrong command! You are not in the Worker Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(self.song_data[0]))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def walk(self, ctx, direction, distance):
        if self.current_game != "switchboard left":
            await ctx.send("Wrong command! You are not in the Left Switchboard Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if direction == "right":
            if self.panning_status + int(distance) >= 7:
                self.panning_status = 7
            else: self.panning_status += int(distance)
        elif direction == "left":
            if self.panning_status - int(distance) <= 1:
                self.panning_status = 1
            else: self.panning_status -= int(distance)
        else:
            await ctx.send("Fix your command!")
            return

        filename = self.get_pan_file()
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def open(self, ctx):
        if self.current_game != "switchboard left":
            await ctx.send("Wrong command! You are not in the Left Switchboard Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if self.panning_status == self.panning_data:
            await ctx.send("Looking good! Or rather… bad. Flip those three switches on the upper left and… TADA! Panel reset. Granted, it's a little quieter in this room so try not to tip anything over on the way out.")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/panning_right.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            return
        else:
            await ctx.send("Nope, no sound, not flashing lights, no nothing. Make sure you replace the panel in case our “friend” gets any ideas about what to destroy next.")
            await self.reduce_time(ctx, 0.5)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/panning_wrong.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    def get_pan_file(self):
        difference = self.panning_status - self.panning_data
        if difference > 5:
            difference = 5
        elif difference < -5: difference = -5
        filename = "./assets/ding"
        if difference < 0:
            filename = filename + str(-1 * difference) + "R.mp3"
        elif difference > 0:
            filename = filename + str(difference) + "L.mp3"
        else: filename += ".mp3"
        return filename

    @commands.command()
    async def slide(self, ctx, side, direction, distance):
        if self.current_game != "switchboard right":
            await ctx.send("Wrong command! You are not in the Right Switchboard Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if side == "left":
            if direction == "up":
                if self.pitch_left + int(distance) >= 7:
                    self.pitch_left = 7
                else: self.pitch_left += int(distance)
            elif direction == "down":
                if self.pitch_left - int(distance) <= 1:
                    self.pitch_left = 1
                else: self.pitch_left -= int(distance)
            else:
                await ctx.send("Fix your command!")
                return
        elif side == "right":
            if direction == "up":
                if self.pitch_right + int(distance) >= 7:
                    self.pitch_right = 7
                else: self.pitch_right += int(distance)
            elif direction == "down":
                if self.pitch_right - int(distance) <= 1:
                    self.pitch_right = 1
                else: self.pitch_right -= int(distance)
            else:
                await ctx.send("Fix your command!")
                return
        else:
            await ctx.send("Fix your command!")
            return

        filename = "./assets/pitch"
        if side == "left":
            filename += str(self.pitch_left)
        elif side == "right":
            filename += str(self.pitch_right)

        filename += ".mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def pitch(self, ctx, side):
        if self.current_game != "switchboard right":
            await ctx.send("Wrong command! You are not in the Right Switchboard Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        filename = "./assets/pitch"
        if side == "left":
            filename += str(self.pitch_left)
        elif side == "right":
            filename += str(self.pitch_right)
        else:
            await ctx.send("Fix your command!")
            return

        filename += ".mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def match(self, ctx):
        if self.current_game != "switchboard right":
            await ctx.send("Wrong command! You are not in the Right Switchboard Room.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        if self.pitch_left == self.pitch_right:
            await ctx.send("Perfect Pitch! We are on the right track to getting your sorry butt out of here. Keep Moving.")
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/pitch_right.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
            return
        else:
            await ctx.send("Your notes did say you were tone deaf… oh sorry, I shouldn't have said that. Try again, you got this!")
            await self.reduce_time(ctx, 0.5)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("./assets/dialogue/pitch_wrong.wav"))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def audio_test(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        filename = "./assets/growl_short_right.mp3"
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

def setup(client):
    client.add_cog(Voice(client))
