import json
import discord


# loading settings
with open('settings.json') as file:
    d = json.load(file)
    token = d['token']
    role_name = d['role_name']

client = discord.Client()

# auxiliary method
def is_listening(member):
    for activity in member.activities:
        if type(activity) == discord.activity.Spotify:
            return True
    return False

# startup sequence
@client.event
async def on_ready():
    print('--------')
    print('Bot name : %s' % client.user.name)
    print('ID       : %s' % client.user.id)
    print('role name: \'%s\'' % role_name)
    print('Active servers: %d' % len(client.guilds))
    print('-------')
    # assign correct groups upon initialization
    for guild in client.guilds:
        listen_role = discord.utils.get(guild.roles, name=role_name)

        for member in guild.members:
            if is_listening(member):
                await member.add_roles(listen_role, reason="is listening")
            else:
                await member.remove_roles(listen_role, reason="is not listening")


# Group switching when member starts listening
@client.event
async def on_member_update(before, after):
    if before.activities != after.activities:

        is_listening_before = is_listening(before)
        is_listening_after  = is_listening(after)
        
        if not is_listening_before and is_listening_after:
            listen_role = discord.utils.get(after.guild.roles, name=role_name)
            await after.add_roles(listen_role, reason="started listening")
            print('[%s]: %s is now listening' % (after.guild.name, after.name))

        elif is_listening_before and not is_listening_after:
            listen_role = discord.utils.get(after.guild.roles, name=role_name)
            await after.remove_roles(listen_role, reason="stopped listening")
            print('[%s]: %s stopped listening' % (after.guild.name, after.name))
 
 
client.run(token)
