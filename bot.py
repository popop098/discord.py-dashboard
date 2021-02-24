import discord
from discord.ext import commands, ipc


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="aswedfghjuygfvcdxs")  # create our IPC Server

        self.load_extension("cogs.ipc")  # load the IPC Route cog

    async def on_ready(self):
        """Called upon the READY event"""
        print("Bot is ready.")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        print(endpoint, "raised", error)


my_bot = MyBot(command_prefix="!")

@my_bot.command()
async def guild(ctx):
    li = []
    for i in my_bot.guilds:
        li.append(i.id)
    await ctx.send(li)
if __name__ == "__main__":
    my_bot.ipc.start()  # start the IPC Server
    my_bot.run("NzY2OTMyMzY1NDI2ODE5MDky.X4qjbA.Gwh8VEtkI3igoUsgTJ3HHWjrNhE")