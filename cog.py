# bot.py
from operator import is_not
import discord
import random
import game
import typing
#1
from discord.ext import commands
from game import character, checkCharacter


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command(name = 'hello',help = 'say hello to bot')
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.display_name}~'.format(member))
        else:
            await ctx.send('Hello {0.display_name}... This feels familiar.'.format(member))
        self._last_member = member

class rollDice(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
    
    @commands.group(name = 'roll',help = 'roll the dice')
    async def roll(self, ctx, input_dice = 'd20'):
        number_of_dice = []
        number_of_sides = []
        modifier = 0
        if input_dice.find('+') != -1:
            string_split = input_dice.split('+')
            length = len(string_split)
            for i in range(length):
                if string_split[i].lower().find('d') != -1:
                    dice_split = string_split[i].split('d')
                    if dice_split[0] == '':
                        number_of_dice.append('1')
                    else:
                        number_of_dice.append(dice_split[0])
                    number_of_sides.append(dice_split[1])
                else:
                    modifier += int(string_split[i])
        elif input_dice.find('+') == -1:
            dice_split = input_dice.lower().split('d')
            if dice_split[0] == '':
                number_of_dice.append('1')
            else:
                number_of_dice.append(dice_split[0])
            number_of_sides.append(dice_split[1])

        result = 0
        response = ''
        for k in range(len(number_of_dice)):
            for _ in range (int(number_of_dice[k])):
                dice_result = random.choice(range(1,int(number_of_sides[k])+1))
                result += dice_result
                response = response + f'{dice_result}, '
        
        result += modifier
        response = response + f' total is {result}'
        await ctx.send('Dice rolled:')
        await ctx.send(response)


class character(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.char_name = None
    
    @commands.command(name = 'create', help = 'Create a new character: please also input character name')
    async def createChar(self, ctx, arg: typing.Optional[str] = None, member: discord.Member = None):
        member = member or ctx.author
        if arg is None:
            await ctx.send('Please enter character name: !create (name)')
            return
        else:
            if checkCharacter(arg):
                await ctx.send('Character name already exist, please try again')
                return
            else:   
                self.char_name = arg
                new_char = game.character(name = self.char_name, creator = member.id)
                await ctx.send(f'You have created character: {self.char_name}, this character will have all stat set to 10')
                await ctx.send(f'To set the character stat, please enter: !set (stat: str, dex,..) (character name) (value)')
                await ctx.send('To view a charactersheet, please enter: !view (character name)')
                await ctx.send('If you want to delete, please enter: !kill (character name)')
    
    @commands.command(name = 'kill', help ='Delete a character from this world')
    async def killChar(self, ctx, char_name: typing.Optional[str] = None):
        if char_name is None:
            await ctx.send('Please enter a exist character name: !kill (name)')
            return
        else:
            self.char_name = str(char_name)
            player = game.loadCharater(self.char_name)
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.delete()
                await ctx.send(f'Character {self.char_name} is removed from this world')
            else:
                await ctx.send("Only the mighty creator or the owner can kill this character!!!")
    
    @commands.command(name = 'view', help = 'View a charactersheet')
    async def viewChar(self, ctx, char_name: typing.Optional[str] = None):
        if char_name is None:
            await ctx.send('Please enter a charactername: !view (name)')
            return
        else:
            self.char_name = str(char_name)
            player = game.loadCharater(self.char_name)
            if player is not None:
                await ctx.send(f'{char_name} has the folowing stat:')
                await ctx.send(f'Strength: {player.str}')
                await ctx.send(f'Dexerity: {player.dex}')
                await ctx.send(f'Constitution: {player.con}')
                await ctx.send(f'Wisdom: {player.wis}')
                await ctx.send(f'Intelligent: {player.intel}')
                await ctx.send(f'Charisma: {player.cha}')
                return
            else:
                await ctx.send(f'{char_name} is not found, please try again')

    @commands.group(name = 'sets', invoke_without_command = True,help = 'Set the stat of character')
    async def setStat(self, ctx):
        await ctx.send('Function to set stat, Please specify stat and character name: !set (stat: str, dex,..) (charactername) (value)')
    
    #--------------Strength---------------------
    @setStat.command(name = 'str', aliases = ['strength', 'Strength'], help = 'Set character strength')
    async def setStrength(self, ctx, char_name: typing.Optional[str] = None, value: int = 10):
        self.char_name = str(char_name)
        player = game.loadCharater(self.char_name)
        if player is not None:
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.setStat('str', value)
                await ctx.send(f'{char_name} now has Strength of {player.str}')
            else:
                await ctx.send("Only the mighty creator or the owner can set this character stat!!!")
        else:
            await ctx.send(f'Character {char_name} is not found, please try again')
    
    #--------------Dex----------------------
    @setStat.command(name = 'dex', aliases = ['dexerity', 'Dexerity'], help = 'Set character dexerity')
    async def setDex(self, ctx, char_name: typing.Optional[str] = None, value: int = 10):
        self.char_name = str(char_name)
        player = game.loadCharater(self.char_name)
        if player is not None:
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.setStat('dex', value)
                await ctx.send(f'{char_name} now has Dexerity of {player.dex}')
            else:
                await ctx.send("Only the mighty creator or the owner can set this character stat!!!")
        else:
            await ctx.send(f'Character {char_name} is not found, please try again')
    
    #--------------int----------------------
    @setStat.command(name = 'int', aliases = ['intelligent', 'Intelligent'], help = 'Set character intelligent')
    async def setIntel(self, ctx, char_name: typing.Optional[str] = None, value: int = 10):
        self.char_name = str(char_name)
        player = game.loadCharater(self.char_name)
        if player is not None:
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.setStat('intel', value)
                await ctx.send(f'{char_name} now has Intelligent of {player.intel}')
            else:
                await ctx.send("Only the mighty creator or the owner can set this character stat!!!")
        else:
            await ctx.send(f'Character {char_name} is not found, please try again')
    
    #--------------con----------------------
    @setStat.command(name = 'con', aliases = ['Constitution', 'constitution', 'cons'], help = 'Set character constitution')
    async def setCon(self, ctx, char_name: typing.Optional[str] = None, value: int = 10):
        self.char_name = str(char_name)
        player = game.loadCharater(self.char_name)
        if player is not None:
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.setStat('con', value)
                await ctx.send(f'{char_name} now has Constitution of {player.con}')
            else:
                await ctx.send("Only the mighty creator or the owner can set this character stat!!!")
        else:
            await ctx.send(f'Character {char_name} is not found, please try again')

    #--------------wis----------------------
    @setStat.command(name = 'wis', aliases = ['wisdom', 'Wisdom'],help = 'Set character constitution')
    async def setWis(self, ctx, char_name: typing.Optional[str] = None, value: int = 10):
        self.char_name = str(char_name)
        player = game.loadCharater(self.char_name)
        if player is not None:
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.setStat('wis', value)
                await ctx.send(f'{char_name} now has Wisdom of {player.wis}')
            else:
                await ctx.send("Only the mighty creator or the owner can set this character stat!!!")
        else:
            await ctx.send(f'Character {char_name} is not found, please try again')
    
    #--------------cha----------------------
    @setStat.command(name = 'cha', aliases = ['charisma', 'Charisma'], help = 'Set character constitution')
    async def setCha(self, ctx, char_name: typing.Optional[str] = None, value: int = 10):
        self.char_name = str(char_name)
        player = game.loadCharater(self.char_name)
        if player is not None:
            if 'admin' in ctx.author.roles or ctx.author.id == player.creator:
                player.setStat('cha', value)
                await ctx.send(f'{char_name} now has Charisma of {player.cha}')
            else:
                await ctx.send("Only the mighty creator or the owner can set this character stat!!!")
        else:
            await ctx.send(f'Character {char_name} is not found, please try again')
    
    
        
    

        


            

