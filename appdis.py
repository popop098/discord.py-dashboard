import os
from datetime import timedelta

import requests
from requests_oauthlib import OAuth2Session
from quart import Quart, request, redirect, render_template, session, url_for
#from flask import Flask, request, redirect, render_template, session, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, models
from routes.discord_oauth import DiscordOauth
from discord.ext import ipc
app = Quart(__name__)
ipc_client = ipc.Client(
    secret_key="aswedfghjuygfvcdxs"
)
app.secret_key = "aswedfghjuygfvcdxs"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"    # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = id
app.config["DISCORD_CLIENT_SECRET"] = 'secret'
app.config["DISCORD_BOT_TOKEN"] = 'token'
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/redirect"

discord = DiscordOAuth2Session(app)

@app.route('/')
async def index():
    return redirect('/home')
@app.route('/home')
async def home():
    if not await discord.authorized:
        return await render_template('index.html',LOG=False)
    else:
        user = await discord.fetch_user()
        return await render_template('index.html',LOG=True,IMG=user.avatar_url or user.default_avatar_url,NAME=user.name)

@app.route('/select')
async def select():
    if not await discord.authorized:
        return redirect(url_for('.index'))
    else:
        user = await discord.fetch_user()
        return await render_template('select.html',LOG=True,IMG=user.avatar_url or user.default_avatar_url,NAME=user.name)
# Route for index page
# Provides user login capabilities
@app.route('/login', methods=['GET'])
async def login():
    return await discord.create_session(scope=['identify','guilds'])

@app.route('/dm')
async def dm():
    user = await discord.fetch_user()
    m=await ipc_client.request(
        "send_", id=int(user.id)
    )
    if m == True:
        return "success"
    else:
        return "fail"
@app.route('/logout')
async def logout():
    discord.revoke()
    return redirect(url_for(".index"))

@app.route("/redirect")
async def Code():
    data = await discord.callback()
    redirect_to = data.get("redirect", "/home")
    return redirect(redirect_to)

@app.route('/dashboard')
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for('.login'))
    user = await discord.fetch_user()
    guilds = await discord.fetch_guilds()
    m = await ipc_client.request("guild_",us=user.name)
    return await render_template('dashboard.html', CHECK=m,IMG=user.avatar_url or user.default_avatar_url,NAME=user.name, render_guild=guilds,LOG=True)

@app.route('/me')
async def me():
    if not await discord.authorized:
        return redirect(url_for('.login'))
    user = await discord.fetch_user()
    guilds = await discord.fetch_guilds()
    return await render_template('me.html', IMG=user.avatar_url or user.default_avatar_url,NAME=user.name,LOG=True)

@app.route('/dashboard/<int:ID>')
async def dashboard_guild(ID):
    if not await discord.authorized:
        return redirect(url_for('.login'))
    user = await discord.fetch_user()
    guilds = await discord.fetch_guilds()
    for i in guilds:
        if str(i.id)==str(ID):
            if i.icon_url is None:
                return await render_template('guild_dash.html',
                                             IMG=user.avatar_url or user.default_avatar_url, NAME=user.name,
                                             ICON=False, GNAME=i.name, LOG=True)
            return await render_template('guild_dash.html',
                                   IMG=user.avatar_url or user.default_avatar_url,NAME=user.name,
                                   ICON=i.icon_url, GNAME=i.name,LOG=True,iCON=True)

if __name__ == '__main__':
    app.run(debug=True)
