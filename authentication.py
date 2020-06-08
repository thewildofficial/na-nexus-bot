import discord
import json

from discord.ext import commands

def AuthCheck(ctx):
    # get authorized roles
    cog_auth = ctx.bot.auth['permissions'][ctx.command.cog_name]
    authorized_roles = set(cog_auth[ctx.command.name] if ctx.command.name in cog_auth else cog_auth['__default__'])

    # if there are no roles, allow anyone
    if not authorized_roles: return True

    # get the author's roles
    author_roles = set([role.id for role in ctx.message.author.roles])

    # get whitelist values
    try:
        author_roles.update(ctx.bot.auth['whitelist'][str(ctx.message.author.id)])
    except KeyError:
        pass

    # return True if there is an intersection with the authorized roles
    return bool(authorized_roles.intersection(author_roles))

class Bot(commands.Bot):
    def __init__(self, command_prefix, auth_file=None, help_command=commands.bot._default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)
        self.auth_file = auth_file
        self.load_auth()

    def load_auth(self):
        self.auth = json.load(self.auth_file)
    
    def save_auth(self):
        self.auth_file.seek(0)
        self.auth_file.write(json.dump(auth))
        self.auth_file.flush()