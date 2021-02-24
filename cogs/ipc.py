from discord.ext import commands, ipc


class IpcRoutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @ipc.server.route()
    async def send_(self, data):
        print(data.id)
        try:
            await (await self.bot.fetch_user(data.id)).send("로그인 성공")  # get the guild object using parsed guild_id
            return True  # return the member count to the client
        except:
            return False

    @ipc.server.route()
    async def guild_(self,data):
        print(data.us)
        li = []
        for i in self.bot.guilds:
            li.append(i.id)
        return li

def setup(bot):
    bot.add_cog(IpcRoutes(bot))
    print('ok')