from twitchio.ext import commands
from pkmn.config import TWITCH
from pkmn.voting import VoteManager
from pkmn.actions import ACTIONS
import asyncio

def start_bot(vote_manager: VoteManager):
    asyncio.set_event_loop(asyncio.new_event_loop())
    bot = commands.Bot(
        irc_token=TWITCH['IRCToken'],
        client_id=TWITCH['ClientId'],
        nick=TWITCH['Nick'],
        prefix=TWITCH['Prefix'],
        initial_channels=[TWITCH['Channel']]
    )

    @bot.event
    async def event_ready():
        'Called once when the bot goes online.'
        print(f"Twitch layer ready")
        ws = bot._ws
        await ws.send_privmsg(TWITCH['Channel'], f"/me is ready to receive votes")


    @bot.event
    async def event_message(ctx):
        'Runs every time a message is sent in chat.'

        # make sure the bot ignores itself and the streamer
        if ctx.author.name.lower() == TWITCH['Nick'].lower():
                return
        try:
            await bot.handle_commands(ctx)
        except:
            pass

    @bot.command(name='vote')
    async def vote_command(ctx, vote=''):
        if not vote_manager.is_poll_available():
            await ctx.send(f'{ctx.author.name}, there\'s no vote happening at the moment')
        else:
            if vote:
                vote_manager.cast_vote(ctx.author.name, vote)
            else:
                await ctx.send(f'{ctx.author.name} tell me what you\'re voting for!')

    @bot.command(name='points')
    async def points_command(ctx):
        points = vote_manager.get_points_for_user(ctx.author.name)
        ending = 's' if points != 1 else ''
        await ctx.send(f'{ctx.author.name}, you have {points} point{ending}')

    @bot.command(name='spend')
    async def spend_command(ctx, action='', argument=''):
        if action:
            if action not in ACTIONS:
                await ctx.send(f'{ctx.author.name}, that\'s not a thing you can do...')
            elif not vote_manager.spend_points(ctx.author.name, action, argument):
                await ctx.send(f'{ctx.author.name}, you don\'t have enough points!')
            else:
                await ctx.send(f'Thanks {ctx.author.name}!')
        else:
            await ctx.send(f'{ctx.author.name}, tell me what you\'re spending points on!')

    bot.run()
