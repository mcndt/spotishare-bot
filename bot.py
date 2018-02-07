import json
import discord


# loading settings
token, role_name = None, None
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
    print('-------')

    # assign correct groups upon initialization
    for server in client.servers:
        listen_role = discord.utils.get(server.roles, name=role_name)

        for member in server.members:
            if str(member.game) == 'Spotify':
                await client.add_roles(member, listen_role)
            else:
                await client.remove_roles(member, listen_role)


# Group switching on listening
@client.event
async def on_member_update(before, after):
    game0, game1 = str(before.game), str(after.game)

    if game0 != game1:
        listen_role = discord.utils.get(after.server.roles, name=role_name)

        if str(after.game) == 'Spotify':
            await client.add_roles(after, listen_role)
        else:
            await client.remove_roles(after, listen_role)

        print('[%s]: {%s}: %s -> %s' % (after.server.name,
                                        after.name, game0, game1))


client.run(token)
