from nextcord.ext import commands
import nextcord 
import os
from requests import post, Session , get
import datetime
import math
from re import match 
from discord.ext import commands
from servar import server_on

# GOOD NIGHT⚡️

TOKEN = "MTI5NzkxNTc1MTk1MjU1MjAyNw.G6ROKw.8RY8wrYDFmQh4inmg2OPB1muZWcHqKjKdlKpqo"       
phone = "0964457663" 
guildid = 1292059911680950342           

bot = commands.Bot(help_command=None)



@bot.event
async def on_ready():
    print(f"BOT ONLINE : {bot.user}")
    await bot.change_presence(activity=nextcord.Game(name="พร้อมใช้งาน🟢"))


class Topup(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("เติมเงินผ่านระบบซองอั่งเปา")  
        self.topup = nextcord.ui.TextInput(
            label="เติมเงินด้วยอังเปา (ห้ามมีตัว # อยู่ในลิงค์)",
            placeholder="กรอกลิงค์ซองอั่งเปาของคุณ",
            required=True
        )
        self.add_item(self.topup)
    async def callback(self, interaction: nextcord.Interaction):

        if (not match (r"https:\/\/gift\.truemoney\.com\/campaign\/\?v=+[a-zA-Z0-9]{18}", self.topup.value)):
           await interaction.send(f"เหมือนคุณจะกวนตีนบอท", ephemeral = True) 
           return
        voucher_code = self.topup.value.split("?v=")[1]
        response = requests.post(f"https://gift.truemoney.com/campaign/vouchers/{voucher_code}/redeem",json={"mobile": phone, "voucher_hash": voucher_code},headers={"Accept": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36","Content-Type": "application/json","Origin": "https://gift.truemoney.com","Accept-Language": "en-US,en;q=0.9","Connection": "keep-alive",})
        redeemdata = response.json()
        if response.status_code == 200 and redeemdata["status"]["code"] == "SUCCESS" :
            amount = float(redeemdata["data"]["my_ticket"]["amount_baht"])


            done = nextcord.Embed(title="**ระบบโดเนทเงิน**", description=f'> **✅ โดเนทสำเร็จ | จำนวน `{amount}` บาท**' ,color=nextcord.green())



            await interaction.send(embed=done,ephemeral=True)

        if response.status_code ==  400 or response.status_code == 404:
            await interaction.send(f"ซองอั่งเปานี้ถูกใช้ไปแล้ว หรือ ลิงค์อั่งเปาให้ถูกต้อง ", ephemeral = True)



class Main(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @nextcord.ui.button(label="กดเพื่อโดเนท", emoji="<:V_:1274765259504226458>", style=nextcord.ButtonStyle.secondary, custom_id="do")
    async def do(self, button: nextcord.Button, interaction: nextcord.Interaction):
        await interaction.response.send_modal(Topup())


@bot.slash_command(guild_ids=[guildid],description="creater give Admin")
async def setup(interaction: nextcord.Interaction):
    embed1 = nextcord.Embed(title="> **DONATE ให้แก่Admin**",description=f"> **กดปุ่มด้านล่างเพื่อโดเนท**\n> หากมีปัญหาติดต่อ @GOOD NIGHT",color=nextcord.Color.blue())
    embed1.set_image(url="https://cdn.discordapp.com/attachments/1286664283442385000/1297924479997055006/237_20241021210439.png?ex=6717b1de&is=6716605e&hm=4d05399ce09e68ea23e91ab32dda9cbb88d60cad8ed29e5e838c3d5f1e35f4fa&") #เปลี่ยนลิ้งรูปได้!!
    embed1.set_footer(text="kum56")

    await interaction.send(embed=embed1, view=Main())

server_on()

bot.run(TOKEN)