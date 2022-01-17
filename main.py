import discord
import color
import toml
import os
import json

import guild

bot = discord.Bot()

with open("conf.toml", mode="r") as file:
    conf = toml.loads(file.read())
    GUILD_IDS = conf["bot"]["guild_ids"]
    TOKEN = conf["bot"]["token"]

@bot.slash_command(guild_ids=GUILD_IDS)
async def create(ctx, name: str):
    with open("last_id.txt", mode="r") as f:
        id = int(f.read()) + 1
    with open("last_id.txt", mode="w") as f:
        f.write(str(id))
    _guild = guild.GuildTemplate(name, ctx.author.id, id)
    _guild.add_member(str(ctx.author.id)).create().store()
    await ctx.respond(f"成功創建 id={id}")

@bot.slash_command(guild_ids=GUILD_IDS)
async def my(ctx):
    def read_file(name):
        with open(f"data/{name}", mode="r") as f:
            return json.loads(f.read())

    l = list(filter(
        lambda i: i["author_id"] == ctx.author.id,
        list(map(
            read_file,
            os.listdir("data"),
        )),
    ))
    embed = discord.Embed(title="你的公會", description="你所有的公會")
    for i in l:
        name = i["name"]
        id = i["id"]
        embed.add_field(name=f"{name}", value=f"{id}", inline=False)
    await ctx.respond(
        embed=embed
    )

@bot.slash_command(guild_ids=GUILD_IDS)
async def invite(ctx, id: int, member: discord.Member):
    class View(discord.ui.View):
        @discord.ui.button(label='加入', style=discord.ButtonStyle.primary)
        async def button_callback(self, button, interaction):
            if member.id != interaction.user.id:
                return
            _guild.add_member(str(interaction.user.id)).store()
            button.disabled = True
            await interaction.response.send_message(f"你已加入{_guild.name}公會", ephemeral=True)

    _guild = guild.Guild.read(id)
    if _guild.author_id != ctx.author.id:
        raise Exception("Author is not same")
    await ctx.send(f"{member.mention} 你被邀請進{_guild.name}公會", view=View())

@bot.slash_command(guild_ids=GUILD_IDS)
async def check(ctx, id: int):
    _guild = guild.Guild.read(id)
    embed = discord.Embed(title=_guild.name, description="公會資料")
    embed.add_field(name="id", value=f"{_guild.id}")
    embed.add_field(name="成員數量", value=f"{len(_guild.members)}")
    line = "-" * 7
    embed.add_field(name="成員", value=f"**{line}**", inline=False)
    for i in _guild.members:
        embed.add_field(name=f"{(await bot.fetch_user(i)).display_name}", value=f"**{line}**", inline=False)
    await ctx.respond(embed=embed)
@bot.event
async def on_ready():
    print(f"{color.fg.GREEN}>> BOT READY <<{color.style.RESET_ALL}")

bot.run(TOKEN)
