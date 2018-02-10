import json
import discord


# loading settings
with open('settings.json') as file:
    d = json.load(file)
    token = d['token']
    role_name = d['role_name']

client = discord.Client()


# startup sequence
@client.event
async def on_ready():
    print('--------')
    print('Bot name : %s' % client.user.name)
    print('ID       : %s' % client.user.id)
    print('role name: \'%s\'' % role_name)
    print('Active servers: %d' % len(client.servers))
    print('-------')
    # assign correct groups upon initialization
    for server in client.servers:
        listen_role = discord.utils.get(server.roles, name=role_name)

        for member in server.members:
            if str(member.game) == 'Spotify':
                await client.add_roles(member, listen_role)
            else:
                await client.remove_roles(member, listen_role)


# Group switching when member starts listening
@client.event
async def on_member_update(before, after):
     if str(before.game) != str(after.game):
        listen_role = discord.utils.get(after.server.roles, name=role_name)

        if str(after.game) == 'Spotify':
            await client.add_roles(after, listen_role)
            print('[%s]: %s is now listening' % (after.server.name, after.name))
        else:
            await client.remove_roles(after, listen_role)
            print('[%s]: %s stopped listening' % (after.server.name, after.name))


client.run(token)
