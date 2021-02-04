import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
import json

#translate client
translator = Translator()

class translate(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def serv_prefix(self, g_id):
        prefixes_i_supose = json.loads(open('prefix.json').read())

        return str(prefixes_i_supose[str(g_id)])

    @commands.command()
    async def translate(self,ctx, scr1, dest1 = None):
        if scr1 == "help" and dest1 == None:
            await ctx.send(f"suported language ID \n{googletrans.LANGCODES}")
        else:
            await ctx.send('type something that you want to translate')

            msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)

            result = translator.translate(msg.content, src=scr1,dest=dest1)

            await ctx.send(result.text)

    @translate.error
    async def translate_error(self, ctx, error):
        i = await self.serv_prefix(g_id=ctx.guild.id)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'`{i}translate (from language id) (to language id)`\nto see langguage id type `.translate help`')
        elif isinstance(error, commands.CommandError):
            await ctx.send('unknow language id')
            
def setup(client):
    client.add_cog(translate(client))

