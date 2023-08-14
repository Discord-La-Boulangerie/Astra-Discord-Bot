#imports
import discord, os, datetime, random, requests, pprint, json, time, sys, brawlstats, fortnite_api, urllib
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
from typing import Optional
from discord.gateway import DiscordWebSocket, _log
from blagues_api import BlaguesAPI, BlagueType, Blague, CountJoke, main
from brawlstats import Ranking, Player, Members, Client, Club, Constants, Brawlers, BattleLog, NotFoundError, models, core
from enkanetwork import EnkaNetworkAPI, EnkaPlayerNotFound
from fortnite_api import StatsImageType, AccountType, BrBannerImage, BrPlayerStats, Playlist
#paramètres

#mobile status
async def identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                '$os': sys.platform,
                '$browser': 'Discord Android',
                '$device': 'Discord Android',
                '$referrer': '',
                '$referring_domain': ''
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }

    if self.shard_id is not None and self.shard_count is not None:
        payload['d']['shard'] = [self.shard_id, self.shard_count]

    state = self._connection
    if state._activity is not None or state._status is not None:
        payload['d']['presence'] = {
            'status': state._status,
            'game': state._activity,
            'since': 0,
            'afk': False
        }

    if state._intents is not None:
        payload['d']['intents'] = state._intents.value

    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(payload)
    _log.info('Shard ID %s has sent the IDENTIFY payload.', self.shard_id)
load_dotenv()
DISCORD_TOKEN = os.getenv("discord_token")
BS_TOKEN = os.getenv("bs_api_token")
enkaclient = EnkaNetworkAPI(lang="fr", cache=True)
# client def
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        await self.tree.sync(guild=guild_id1)
        await self.tree.sync()
intents = discord.Intents.all()
client = MyClient(intents=intents)
guild_id = 1104309851775049728
guild_id1 = discord.Object(id=guild_id)
botlink= "https://discordapp.com/users/1139870049528709120"
boticonurl= "https://cdn.discordapp.com/icons/1104309851775049728/cc577c08ac2c2c10024a3e446a0777cd.webp?size=96"
DiscordWebSocket.identify = identify

##commands
#ping
@client.tree.command(name = "ping", description = "[TEST] pong ! 🏓")
async def pingpong(interaction: discord.Interaction):
    emb=discord.Embed( description="Pong ! 🏓", color=discord.Color.blurple(),timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}") # type: ignore
    emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore            
    await interaction.response.send_message(embed=emb, ephemeral=True)

#staff app system
class staff(discord.ui.Modal, title="Candidature"):
    role = discord.ui.TextInput(label='rôle', style=discord.TextStyle.paragraph, max_length=200, placeholder="décrit nous quel rôle tu souhaite avoir", required = True)
    reason = discord.ui.TextInput(label='raison', style=discord.TextStyle.paragraph, max_length=2000, placeholder="hésitez pas avec les détails, vous avez de la place", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"ta candidature a bien été enregistrée {interaction.user.mention} !", ephemeral=True)
        channel=client.get_channel(1130945538406240399)
        emb=discord.Embed(title="Candidature", description=f"```{interaction.user.display_name} vient de postuler :\n\n rôle sujet au recrutement : {self.role}\n\n Raison : {self.reason}```", color = discord.Colour.blurple(), timestamp=datetime.datetime.now())
        emb.set_author(name="BreadBot", url=f"{botlink}", icon_url=f"{boticonurl}") # type: ignore
        emb.set_thumbnail(url=f"{interaction.user.avatar}")        
        emb.set_footer(text=f"{interaction.user.display_name}, sur {interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore            
#send embed to mod chat
        await channel.send(embed=emb) #type: ignore

@client.tree.command(name = "staff_app", description = "[MODERATION] postuler dans la modération, grâce à cette commande, c'est facile.")
async def staff_app(interaction: discord.Interaction):
    await interaction.response.send_modal(staff())

#sendrule
@client.tree.command(name = "sendrule", description = "[MODERATION]permet d'envoyer l'embed du règlement.") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.default_permissions(manage_guild=True)
async def sendrule(interaction: discord.Interaction):
    channel=client.get_channel(1130945537907114137)
    emb=discord.Embed(title="Règlement de la Boulangerie", description="# __I__. Respecter les règles de la plate-forme !\nAvant de respecter le règlement du serveur, nous vous invitons également à respecter les règles de discord :\n- [Conditions d'utilisation de Discord](https://discord.com/terms)\n- [Charte d’utilisation de la communauté Discord](https://discord.com/guidelines)\n# __II__. Langue sur le serveur :\nLe serveur et ses discussions sont uniquement en Français.\n# __III__. Soyez respectueux et ayez du bon sens !\nAyez une bonne impression au sein de la communauté ! Tous types de contenus violents, racistes et NSFW sont interdits sur ce serveur. Respectez vous peu importe vos affinités lorsque vous parlez avec le reste de la communauté. Nous ne pouvons pas tout énumérer mais n'essayez pas de contourner les règles d'une quelconque manière.\n# __IV__. Les Interdictions :\nLa publicité de n'importe quel projet sur le serveur comme dans les messages privés des autres membres est interdite. Le spam, le flood ou tout spam de mentions inutiles voir abusives vous sera sanctionné. Les comportements toxiques (troll, insultes, etc...) ainsi que les provocations n'ont rien à faire sur ce serveur. La divulgation d'informations sans consentement vous sera sanctionné.\n# __V__. Le Staff :\nL'équipe de modération vous remercierai d'avoir un pseudonyme sans caractère spéciaux ainsi qu'un profil correct et approprié. Ces règles ne sont pas négligeables et obligatoires. L'équipe de modération ainsi que l'administration aura toujours le dernier mot. En cas d'abus de l'un de nos modérateurs, merci de nous prévenir !", color = discord.Color.blue())
    emb.set_author(name="Wishrito", url="https://discordapp.com/users/911467405115535411", icon_url=f"{interaction.user.avatar}") # type: ignore
    emb.set_thumbnail(url="https://cdn.discordapp.com/icons/1115588576340606978/a_d2b27f21b84bc1b5c000b05d408a76ef.gif?size=96")        
    #send embed to rules chat
    await channel.send(embed=emb) #type: ignore
    await interaction.response.send_message("envoyé!", ephemeral=True)

#rps
@client.tree.command(name="rps", description="[FUN][BETA] Shi-Fu-Mi")
@app_commands.choices(choix=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors"),
    ])
async def rps(interaction: discord.Interaction, choix: app_commands.Choice[str]):
    if (choix.value == 'rock'):
        await interaction.response.send_message("paper! :scroll:", ephemeral=True) 
    elif (choix.value == 'paper'):
        await interaction.response.send_message("scissors! :scissors:", ephemeral=True)
    else:
        await interaction.response.send_message("rock! :rock:", ephemeral=True)

@client.tree.context_menu(name="Profil", guild=guild_id1)
@app_commands.rename(user="Membre")
async def profil(interaction: discord.Interaction, user: discord.Member):
# Remove unnecessary characters
    badges_class = str(user.public_flags.all()).replace("UserFlags.","").replace("[<","").replace(">]","").replace("hypesquad_bravery: 64","<:bravery:1137854128131932290>").replace("hypesquad_balance: 256","<:balance:1137854125120421918>").replace("hypesquad_brilliance: 128","<:brilliance:1137854120930332682>").replace("active_developer: 4194304","<:activedeveloper:1137860552257970276>").replace(">, <"," ")

    # Output
    emb = discord.Embed(title=f"Profil de {user.display_name}", description=f"Date de création du compte :\n> le {user.created_at.day}/{user.created_at.month}/{user.created_at.year} à {user.created_at.hour}h{user.created_at.minute}\nBadges :\n{badges_class}", color=user.color)
    emb.set_thumbnail(url=user.display_avatar)
    await interaction.response.send_message(embed=emb, ephemeral=True, view=SimpleView(url=user.avatar.url, user=user)) #type: ignore
class SimpleView(discord.ui.View):
    def __init__(self, user, url):
        super().__init__()
        
        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(discord.ui.Button(label=f'photo de profil de {user.display_name}', url=url))

#sanctions system
@client.tree.command(name ="ban", description = "[MODERATION][BETA] bannit un utilisateur spécifié") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à ban")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du ban")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason:Optional[str] = None):
    if not interaction.user.id == interaction.guild.owner_id : #type: ignore
        if interaction.user.top_role <= member.top_role: #type: ignore
            await interaction.response.send_message(f"tu n'as pas la permission de ban {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", ephemeral=True, color=discord.Color.red()) #type: ignore
        else:
            await member.ban(reason=reason)
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été ban pour la raison suivante :\n{reason}", ephemeral=True)
            channel = await client.fetch_channel(1130945537907114139)
            await channel.send(content=f"{member.mention} a été ban du serveur par {interaction.user.name}") #type: ignore
    else:
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été ban pour la raison suivante :\n{reason}", ephemeral=True)
        channel = await client.fetch_channel(1130945537907114139)
        await channel.send(content=f"{member.mention} a été ban du serveur par {interaction.user.name}") #type: ignore

#sanctions system
@client.tree.command(name ="mute", description = "[MODERATION] mute un utilisateur spécifié", guild=guild_id1) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à mute")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du mute")
@app_commands.rename(duration="temps")
@app_commands.describe(duration="Le temps que l'utilisateur doit être mute")
@app_commands.describe(file="le fichier contenant la preuve de la raison")
@app_commands.rename(file="fichier")
@app_commands.default_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, member: discord.Member, duration: str, reason:Optional[str], file: Optional[discord.Attachment] = None):
    if not interaction.user.id == interaction.guild.owner_id : #type: ignore
        if interaction.user.top_role.position <= member.top_role.position: #type: ignore
            emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de kick {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", color=discord.Color.red()) #type: ignore
            await interaction.response.send_message(embed=emb, ephemeral=True) #type: ignore
        else:
            await member.timeout(datetime.timedelta(seconds=float(duration)), reason=reason)
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute {duration} minutes pour la raison suivante : {reason}", ephemeral=True)
            channel = await client.fetch_channel(1131864743502696588)
            emb = discord.Embed(title="Sanction",description=f"{member.mention} a été mute par {interaction.user.mention}")
            emb.set_field_at(index=1, name="", value=file)
            await channel.send(embed=emb) #type: ignore

    else:
        await member.timeout(datetime.timedelta(seconds=float(duration)))
        await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été mute pour la raison suivante :\n{reason}", ephemeral=True)
        channel = await client.fetch_channel(1131864743502696588)
        emb = discord.Embed(title="Sanction",description=f"{member.mention} a été mute par {interaction.user.mention}")
        emb.set_image(url=file)
        await channel.send(embed=emb) #type: ignore

@client.tree.command(name="kick", description="[MODERATION] kick un utilisateur spécifié", guild=guild_id1)
@app_commands.rename(member="membre")
@app_commands.describe(member="l'utilisateur à kick")
@app_commands.rename(reason="raison")
@app_commands.describe(reason="la raison du kick")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: Optional[str], file: Optional[discord.Attachment] = None):
    if not interaction.user.id == interaction.guild.owner_id : #type: ignore
        if interaction.user.top_role <= member.top_role: #type: ignore
            emb = discord.Embed(title="[ERREUR] Sanction", description=f"tu n'as pas la permission de kick {member.display_name}, car le rôle {interaction.user.top_role} est supérieur ou égal au tien.", color=discord.Color.red()) #type: ignore
            await interaction.response.send_message(embed=emb, ephemeral=True) #type: ignore
        else:
            await member.kick(reason=reason)
            await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été kick pour la raison suivante :\n{reason}", ephemeral=True)
            channel = await client.fetch_channel(1130945537907114139)
            await channel.send(content=f"{member.mention} a été kick du serveur par {interaction.user.name}") #type: ignore
    else:
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.display_name} ({member.id}) a bien été kick pour la raison suivante :\n{reason}", ephemeral=True)
        channel = await client.fetch_channel(1130945537907114139)
        await channel.send(content=f"{member.mention} a été kick du serveur par {interaction.user.name}") #type: ignore

@client.tree.command(name="sync", description="[MODERATION] permet de synchroniser le tree")
@app_commands.default_permissions(manage_guild=True)
async def sync(interaction: discord.Interaction):
    await client.tree.sync(guild=guild_id1)
    await client.tree.sync()
    await interaction.response.send_message("le tree a été correctement synchronisé !", ephemeral=True)

@client.tree.command(name="verify", description="[BETA] permet de se vérifier sur le serveur", guild=guild_id1)
@app_commands.describe(file="une capture d'écran de votre profil Brawl Stars")
@app_commands.rename(file="fichier")
async def verify(interaction: discord.Interaction, file: discord.Attachment):
    if file.content_type == "image/png" or "image/jpeg" :
        e = interaction.user.id
        channel = client.get_channel(1139911542616367179)
        emb = discord.Embed(title="Demande de vérification", timestamp=datetime.datetime.now())
        emb.set_image(url=file)
        emb.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
        await interaction.response.send_message("ta demande a bien été envoyée. :thumbsup:",ephemeral=True)
        await channel.send(embed=emb, view=(verifyview(e, interaction)))
    else:
        await interaction.response.send_message("le fichier que tu as envoyé doit être une image, et ce n'est pas le cas. réessaie s'il te plait",ephemeral=True)
        
class verifyview(discord.ui.View):
    def __init__(self, e, interaction):
        self.interaction = interaction
        self.e = e
        super().__init__()
    @discord.ui.button(label="Valider", style=discord.ButtonStyle.green)
    async def on_click1(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = discord.utils.get(interaction.guild.roles, id=1104312217224085556) #type: ignore
        emb = discord.Embed(title="Félicitation", description=f"tu as été accepté sur {self.interaction.guild.name}!", timestamp=datetime.datetime.now(), color=discord.Color.green())
        emb.set_author(name=f"{self.interaction.guild.name}", url=self.interaction.guild.icon)
        await interaction.user.edit(roles=[role])
        await self.e.send(embed=emb)
    
    @discord.ui.button(label="Invalider", style=discord.ButtonStyle.red)
    async def on_click2(self, interaction: discord.Interaction, button: discord.ui.Button):
        emb = discord.Embed(title="Désolé...", description=f"tu as été refusé sur {self.interaction.guild.name}! :confused:", timestamp=datetime.datetime.now(), color=discord.Color.green())
        emb.set_author(name=f"{self.interaction.guild.name}", url=self.interaction.guild.icon)
        await self.e.kick(reason="n'est pas présent sur le club")

#report system

#def modal
class ReportModal(discord.ui.Modal, title="signalement"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(label="raison du report",min_length=1, placeholder=f"pourquoi veux-tu le signaler ?")
    
    async def on_submit(self, interaction: discord.Interaction):
        textinput = self.textinput
        chat = await client.fetch_channel(int(1130945538406240405))
        emb=discord.Embed(title="signalement", description=f"{interaction.user.display_name} vient de créer un signalement :\n\nMembre signalé : {self.msg.author.display_name}\n\nRaison : {textinput}\n\nPreuve : {self.msg.content}\n\n\n [aller au message]({self.msg.jump_url})", color = discord.Color.green(), timestamp=datetime.datetime.now())
        emb.set_author(name=f"{client.user}", url=f"{botlink}", icon_url=f"{boticonurl}")
        emb.set_thumbnail(url=f"{interaction.user.avatar}") # type: ignore
        emb.set_footer(text=f"{interaction.guild.name}", icon_url=interaction.guild.icon) # type: ignore
        #send embed to mod chat
        await chat.send(embed=emb) # type: ignore
        await interaction.response.send_message(content=f"ton signalement a bien été envoyé {interaction.user.display_name}", ephemeral=True)

@client.tree.context_menu(name="Report", guild=guild_id1)
async def report(interaction: discord.Interaction, message: discord.Message):
    msg = message
    await interaction.response.send_modal(ReportModal(msg))

class say(discord.ui.Modal, title="contenu du reply"):
    def __init__(self, msg):
        self.msg = msg
        super().__init__()
    textinput = discord.ui.TextInput(label="texte",min_length=1)

    async def on_submit(self, interaction: discord.Interaction):

        await self.msg.reply(self.textinput.value)
        await interaction.response.send_message(content="ton message a bien été envoyé", ephemeral=True)

@client.tree.context_menu(name="Say", guild=guild_id1)
@app_commands.default_permissions(manage_guild=True)
async def pins(interaction: discord.Interaction, message: discord.Message):
    msg = message
    await interaction.response.send_modal(say(msg))

#auto events
@client.event
async def on_member_remove(member: discord.Member):
    channel=client.get_channel(1130945537907114139)
    emb=discord.Embed(title="Au revoir!", description=f"Notre confrère pain {member.name} vient de brûler... Nous lui faisons nos plus sincères adieux. :saluting_face:", color = discord.Color.red(), timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}")
    emb.set_footer(text=f"{member.name}, sur {member.guild.name}", icon_url=member.guild.icon)       
    await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore

@client.event 
async def on_member_join(member: discord.Member):
    emb=discord.Embed(title="Nouveau Pain!", description=f"Un nouveau pain vient de sortir du four ! Bienvenue sur {member.guild.name} {member.display_name}! :french_bread:", color = discord.Color.green(), timestamp=datetime.datetime.now())
    emb.set_author(name="BreadBot", icon_url=f"{boticonurl}", url=f"{botlink}")
    emb.set_footer(text=f"{member.name}, sur {member.guild.name}", icon_url=member.guild.icon)            
    channel = client.get_channel(1130945537907114139)
    await channel.send(content=f"{member.mention}", embed=emb, silent=True) # type: ignore

#login check + bot login events
@client.event
async def on_ready():
    print("="*10 + " Build Infos " + "="*10)
    print(f"Connecté en tant que {client.user.display_name} ({client.user.id})") #type: ignore
    print(f"Discord info : {discord.version_info.releaselevel}")
    activity = discord.Activity(type = discord.ActivityType.watching, name=f"Astra Academy")
    await client.change_presence(activity=activity, status=discord.Status.online)
client.run(str(DISCORD_TOKEN))