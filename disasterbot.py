import sys
sys.modules['audioop'] = None  # prevents Discord.py from importing audioop

import discord
from discord.ext import commands
from datetime import datetime
import os
from dotenv import load_dotenv
from discord.ui import View, Button


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # 👈 very important
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def start(ctx):
    # ========== MAIN MENU VIEW CLASS ==========
    class MenuButtonView(View):
        def __init__(self, exclude=None):
            super().__init__(timeout=None)
            self.exclude = exclude or []

            if "commands" not in self.exclude:
                self.add_item(self.CommandsButton())
            if "hotlines" not in self.exclude:
                self.add_item(self.HotlinesButton())
            if "resources" not in self.exclude:
                self.add_item(self.ResourcesButton())
            if "disasters" not in self.exclude:
                self.add_item(self.DisastersButton())

        # ----- COMMANDS -----
        class CommandsButton(Button):
            def __init__(self):
                super().__init__(label="Commands", style=discord.ButtonStyle.primary, emoji="📘")

            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(
                    title="📘 Available Commands",
                    description=(
                        "`!info` — About this chatbot\n"
                        "`!hotlines` — List of emergency hotlines\n"
                        "`!time` — Show current date and time\n"
                        "`!resources` — View official government websites\n\n"
                        "**Disaster Commands:**\n"
                        "`!earthquake` — Earthquake info and precautions\n"
                        "`!flood` — Flood preparedness and alerts\n"
                        "`!landslide` — Landslide precautions\n"
                        "`!tsunami` — Tsunami evacuation guide\n"
                        "`!typhoon` — Typhoon warnings and safety tips\n"
                        "`!volcano` — Volcano updates and safety measures"
                    ),
                    color=0x95A5A6,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await interaction.followup.send("Select another category below:", view=MenuButtonView(exclude=["commands"]))

        # ----- HOTLINES -----
        class HotlinesButton(Button):
            def __init__(self):
                super().__init__(label="Hotlines", style=discord.ButtonStyle.danger, emoji="☎️")

            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(
                    title="📞 Emergency Hotlines (Philippines)",
                    description=(
                        "**National Emergency Hotline:** 911\n"
                        "**Philippine Red Cross:** 143\n"
                        "**NDRRMC Trunklines:** (02) 8911-5061 to 65 local 100\n"
                        "**NDRRMC Operations Center:** (02) 8911-1406\n"
                        "**DSWD Text Hotline:** 0918-912-2813\n"
                        "**Philippine National Police (PNP):** 117\n"
                        "**Bureau of Fire Protection (BFP):** (02) 8426-0219 / (02) 8426-0246\n"
                        "**Philippine Coast Guard (PCG):** (02) 8527-8481 to 89 / (02) 8527-3877\n"
                        "**MMDA Hotline:** 136 / (02) 8882-4151 to 77"
                    ),
                    color=0xE74C3C,
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await interaction.followup.send("Select another category below:", view=MenuButtonView(exclude=["hotlines"]))

        # ----- RESOURCES -----
        class ResourcesButton(Button):
            def __init__(self):
                super().__init__(label="Resources", style=discord.ButtonStyle.secondary, emoji="🔗")

            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(
                    title="🔗 Official Disaster Resources (Philippines)",
                    description="Trusted websites for real-time updates and safety information.",
                    color=0x27AE60,
                )
                embed.add_field(
                    name="🌋 PHIVOLCS (Volcano & Earthquake Monitoring)",
                    value="[https://www.phivolcs.dost.gov.ph](https://www.phivolcs.dost.gov.ph)",
                    inline=False,
                )
                embed.add_field(
                    name="🌧 PAGASA (Weather, Typhoon & Flood Alerts)",
                    value="[https://bagong.pagasa.dost.gov.ph](https://bagong.pagasa.dost.gov.ph)",
                    inline=False,
                )
                embed.add_field(
                    name="🏛 NDRRMC (National Disaster Response)",
                    value="[https://ndrrmc.gov.ph](https://ndrrmc.gov.ph)",
                    inline=False,
                )
                embed.add_field(
                    name="💬 DSWD (Relief & Social Services)",
                    value="[https://www.dswd.gov.ph](https://www.dswd.gov.ph)",
                    inline=False,
                )
                embed.add_field(
                    name="🧭 Mines and Geosciences Bureau (Landslide Info)",
                    value="[https://www.mgb.gov.ph](https://www.mgb.gov.ph)",
                    inline=False,
                )
                embed.add_field(
                    name="🛰 MMDA (Metro Manila Disaster Response)",
                    value="[https://www.mmda.gov.ph](https://www.mmda.gov.ph)",
                    inline=False,
                )
                embed.set_footer(text="Always rely on official sources for disaster information.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await interaction.followup.send("Select another category below:", view=MenuButtonView(exclude=["resources"]))

                # ----- DISASTERS -----
        class DisastersButton(Button):
            def __init__(self):
                super().__init__(label="Disasters", style=discord.ButtonStyle.success, emoji="🌋")

            async def callback(self, interaction: discord.Interaction):
                # Recreate the same embed used in your !helpdisaster command
                embed = discord.Embed(
                    title="🌏 Disaster Preparedness Menu",
                    description=(
                        "React with an emoji below to learn about each disaster:\n\n"
                        "🌎 — Earthquake\n"
                        "🌧️ — Flood\n"
                        "🏔️ — Landslide\n"
                        "🌊 — Tsunami\n"
                        "🌪️ — Typhoon\n"
                        "🌋 — Volcanic Eruption\n\n"
                        "Stay safe and informed! 💪"
                    ),
                    color=0x00FFFF,
                )

                # Send the embed
                message = await interaction.response.send_message(embed=embed)

                # Add the emojis for reactions
                emojis = ["🌎", "🌧️", "🏔️", "🌊", "🌪️", "🌋"]
                sent_message = await interaction.original_response()
                for emoji in emojis:
                    await sent_message.add_reaction(emoji)

                # Define check for reactions
                def check(reaction, user):
                    return (
                        user != bot.user
                        and str(reaction.emoji) in emojis
                        and reaction.message.id == sent_message.id
                    )

                # Wait for user reactions and respond accordingly
                while True:
                    try:
                        reaction, user = await bot.wait_for("reaction_add", timeout=120.0, check=check)
                        emoji = str(reaction.emoji)

                        if emoji == "🌎":
                            e = discord.Embed(
                                title="🌎 Earthquake Preparedness",
                                description=(
                                    "**Definition:** Sudden shaking of the ground caused by movement of Earth’s crust.\n\n"
                                    "**Active Fault Lines (PHIVOLCS):**\n"
                                    "- West Valley Fault\n- East Valley Fault\n- Philippine Fault Zone\n"
                                    "- Central Leyte Fault\n- Cotabato Fault System\n- North & South Mindanao Faults\n\n"
                                    "**Precautions:** Secure heavy furniture, prepare emergency kits, know evacuation areas.\n"
                                    "**During:** Drop, Cover, and Hold On. Stay away from windows.\n"
                                    "**After:** Check for injuries, avoid damaged structures, expect aftershocks.\n\n"
                                    "🔗 [PHIVOLCS FaultFinder](https://faultfinder.phivolcs.dost.gov.ph/)"
                                ),
                                color=0x2ECC71,
                            )
                            await interaction.followup.send(embed=e, ephemeral=True)

                        elif emoji == "🌧️":
                            e = discord.Embed(
                                title="🌧️ Flood Preparedness",
                                description=(
                                    "**Flood-Prone Areas (PAGASA):** Metro Manila, Bulacan, Pampanga, Cagayan Valley, "
                                    "Eastern Visayas, Davao Region, and Northern Mindanao.\n\n"
                                    "**Rainfall Warning Levels (PAGASA):**\n"
                                    "🟡 **Yellow:** 7.5–15 mm rain (Monitor weather updates)\n"
                                    "🟠 **Orange:** 15–30 mm rain (Flooding possible; be alert)\n"
                                    "🔴 **Red:** >30 mm rain (Severe flooding expected; evacuate immediately)\n\n"
                                    "**Precautions:** Move to higher ground, unplug electrical devices, avoid floodwaters."
                                ),
                                color=0x3498DB,
                            )
                            await interaction.followup.send(embed=e, ephemeral=True)

                        elif emoji == "🏔️":
                            e = discord.Embed(
                                title="🏔️ Landslide Preparedness",
                                description=(
                                    "**Definition:** Downward movement of soil or rock due to rain or earthquakes.\n\n"
                                    "**Areas with Landslide History:** Benguet, Mountain Province, Ifugao, Leyte, Compostela Valley, Bukidnon.\n"
                                    "**Causes:** Heavy rain, deforestation, earthquakes, steep terrain.\n\n"
                                    "**Before:** Avoid building homes near steep slopes.\n"
                                    "**During:** Move to stable ground immediately.\n"
                                    "**After:** Stay away from landslide-prone zones until declared safe."
                                ),
                                color=0x8E44AD,
                            )
                            await interaction.followup.send(embed=e, ephemeral=True)

                        elif emoji == "🌊":
                            e = discord.Embed(
                                title="🌊 Tsunami Preparedness",
                                description=(
                                    "**Definition:** Large sea waves caused by underwater earthquakes or volcanic eruptions.\n\n"
                                    "**High-Risk Areas (PAGASA):** Coastal regions of Eastern Samar, Surigao, Davao Oriental, "
                                    "Batanes, and other eastern seaboards.\n\n"
                                    "**Before:** Know evacuation routes; be aware of sirens or official warnings.\n"
                                    "**During:** If you feel a strong earthquake, move immediately inland or to higher ground.\n"
                                    "**After:** Stay tuned for official all-clear announcements before returning."
                                ),
                                color=0x1ABC9C,
                            )
                            await interaction.followup.send(embed=e, ephemeral=True)

                        elif emoji == "🌪️":
                            e = discord.Embed(
                                title="🌪️ Typhoon Preparedness",
                                description=(
                                    "**Definition:** Intense tropical cyclone bringing strong winds and heavy rain.\n\n"
                                    "**Rainfall Warning (PAGASA):**\n"
                                    "🟡 Yellow – 7.5–15mm: Be alert, monitor updates.\n"
                                    "🟠 Orange – 15–30mm: Flooding possible, prepare to evacuate.\n"
                                    "🔴 Red – >30mm: Serious flooding expected, evacuate immediately.\n\n"
                                    "**Precautions:** Store clean water, secure roofs, charge devices, stay indoors."
                                ),
                                color=0xE67E22,
                            )
                            await interaction.followup.send(embed=e, ephemeral=True)

                        elif emoji == "🌋":
                            e = discord.Embed(
                                title="🌋 Volcanic Eruption Preparedness",
                                description=(
                                    "**Active Volcanoes (PHIVOLCS):** Mayon, Taal, Kanlaon, Bulusan, and Pinatubo.\n\n"
                                    "**Status (Last 5 Years):**\n"
                                    "- **Mayon:** Active – Eruptions in 2018, 2023\n"
                                    "- **Taal:** Active – Eruptions in 2020, 2021\n"
                                    "- **Kanlaon:** Active – Increased activity 2023–2024\n"
                                    "- **Bulusan:** Active – Minor eruptions 2022\n"
                                    "- **Pinatubo:** Dormant – No eruptions since 1991\n\n"
                                    "**Precautions:** Prepare masks for ashfall, avoid river valleys, follow evacuation orders."
                                ),
                                color=0xC0392B,
                            )
                            await interaction.followup.send(embed=e, ephemeral=True)

                    except asyncio.TimeoutError:
                        await interaction.followup.send("⏰ Reaction timeout. Type `!start` again to reopen the disaster menu.", ephemeral=True)
                        break

    # ========== START BUTTON VIEW ==========
    class StartButtonView(View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
        async def start_button(self, interaction: discord.Interaction, button: Button):
            user = interaction.user
            # Personalized greeting embed
            greeting_embed = discord.Embed(
                title=f"👋 Hello, {user.name}!",
                description=(
                    f"Welcome to the **Disaster Preparedness Bot**, {user.mention}! 🌍\n\n"
                    "This bot provides **disaster awareness, emergency hotlines**, and **safety resources** "
                    "to help you stay informed and ready for natural hazards in the Philippines.\n\n"
                    "Select a category below to begin!"
                ),
                color=0x00FFAA,
            )
            greeting_embed.set_thumbnail(url=user.display_avatar.url)
            greeting_embed.set_footer(text="Stay safe and always be prepared 💪")

            await interaction.response.send_message(embed=greeting_embed)
            await interaction.followup.send("🔽 **Choose a category:**", view=MenuButtonView())

    # Initial message with only Start button
    intro_embed = discord.Embed(
        title="👋 Welcome to the Disaster Preparedness Bot!",
        description="Click **Start** to begin your experience.",
        color=0x00FFAA,
    )
    intro_embed.set_footer(text="Powered by Team Iternity ⚡")

    await ctx.send(embed=intro_embed, view=StartButtonView())


# ========================
# BASIC INFO COMMANDS
# ========================

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="🌍 Disaster Preparedness Bot",
        description=(
            "This chatbot provides **disaster awareness, safety guides, and emergency information** for the Philippines.\n\n"
            "It aims to help you **prepare, respond, and recover** from natural disasters like earthquakes, floods, "
            "landslides, tsunamis, typhoons, and volcanic eruptions.\n\n"
            "Type `!commands` to see all available commands."
        ),
        color=0x00AEEF,
    )
    await ctx.send(embed=embed)


@bot.command()
async def time(ctx):
    now = datetime.now()
    date_time = now.strftime("%B %d, %Y - %I:%M %p")
    await ctx.send(f"🕒 Current date and time: **{date_time}**")


# ========================
# DISASTER COMMANDS
# ========================

@bot.command()
async def earthquake(ctx):
    embed1 = discord.Embed(
        title="🌍 Earthquake Preparedness",
        description="**Definition:** Sudden shaking of the ground caused by movement of the Earth's crust.\n\n🔗 [PHIVOLCS FaultFinder](https://faultfinder.phivolcs.dost.gov.ph/)",
        color=0x2ECC71,
    )
    embed2 = discord.Embed(
        title="⚪ Alert Level 0 — No Significant Activity",
        description="No felt earthquakes or active ground movement.\nContinue monitoring; ensure emergency kits are ready.",
        color=0x95A5A6,
    )
    embed3 = discord.Embed(
        title="🟡 Alert Level 1 — Weak Tremors Detected",
        description="Minor earthquakes felt; aftershocks possible.\nInspect surroundings for cracks; secure fragile items.",
        color=0xF1C40F,
    )
    embed4 = discord.Embed(
        title="🟠 Alert Level 2 — Moderate Earthquake",
        description="Strong shaking felt indoors; some damage possible.\nDrop, Cover, and Hold On. Stay away from glass and heavy objects.",
        color=0xE67E22,
    )
    embed5 = discord.Embed(
        title="🔴 Alert Level 3 — Strong to Major Earthquake",
        description="Intense ground shaking; structural collapse possible.\nEvacuate when shaking stops; stay alert for aftershocks and landslides.",
        color=0xE74C3C,
    )

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)
    await ctx.send(embed=embed5)



@bot.command()
async def flood(ctx):
    embed1 = discord.Embed(title="🌊 Flood-Prone Areas", description="Metro Manila, Bulacan, Pampanga, Cagayan Valley, Bicol, Eastern Visayas, Davao del Norte, Agusan del Sur.", color=0x3498DB)
    embed2 = discord.Embed(title="🟢 Yellow Alert", description="Flooding possible; monitor updates from PAGASA.", color=0xF1C40F)
    embed3 = discord.Embed(title="🟠 Orange Alert", description="Flooding threatening; prepare to evacuate.", color=0xE67E22)
    embed4 = discord.Embed(title="🔴 Red Alert", description="Serious flooding expected; evacuation mandatory.", color=0xE74C3C)
    embed5 = discord.Embed(title="✅ Precautions", description="- Avoid floodwaters.\n- Move valuables to higher ground.\n- Follow LGU evacuation instructions.", color=0x2ECC71)
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)
    await ctx.send(embed=embed5)



@bot.command()
async def landslide(ctx):
    embed1 = discord.Embed(title="⛰️ Landslide-Prone Areas", description="Benguet, Mountain Province, Southern Leyte, Davao de Oro, Cebu, Quezon, and parts of Mindanao.", color=0x8E44AD)
    embed2 = discord.Embed(title="⚠️ Causes", description="Heavy rainfall, earthquakes, steep slopes, and deforestation.", color=0xE67E22)
    embed3 = discord.Embed(title="✅ Precautions", description="- Avoid steep slopes after rains.\n- Watch for cracks or leaning trees.\n- Evacuate if advised.", color=0x2ECC71)
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)



@bot.command()
async def tsunami(ctx):
    embed1 = discord.Embed(title="🌊 Tsunami-Prone Areas", description="Eastern Visayas, Bicol, Davao Oriental, Surigao del Sur, Palawan.", color=0x1ABC9C)
    embed2 = discord.Embed(title="🟢 Information", description="No threat; for awareness only.", color=0x2ECC71)
    embed3 = discord.Embed(title="🟠 Advisory", description="Minor waves possible; stay alert for updates.", color=0xF39C12)
    embed4 = discord.Embed(title="🔴 Warning", description="Major waves expected. Evacuate to high ground immediately!", color=0xE74C3C)
    embed5 = discord.Embed(title="✅ Precautions", description="Move inland or to higher ground when a strong quake is felt near the coast.", color=0x3498DB)
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)
    await ctx.send(embed=embed5)

@bot.command()
async def typhoon(ctx):
    embed1 = discord.Embed(
        title="🌪️ Typhoon Preparedness and Information",
        description="Intense tropical cyclones bringing strong winds and heavy rains. Common in the Philippines between June and November.",
        color=0xF1C40F
    )

    embed2 = discord.Embed(
        title="🟡 Yellow Rainfall Warning",
        description="7.5–15 mm rain (moderate to heavy) within 1 hour.\nBe alert — possible flooding in low-lying areas.",
        color=0xF1C40F
    )

    embed3 = discord.Embed(
        title="🟠 Orange Rainfall Warning",
        description="15–30 mm rain (heavy to intense) within 1 hour.\nBe prepared — flooding is threatening; move valuables to higher ground.",
        color=0xE67E22
    )

    embed4 = discord.Embed(
        title="🔴 Red Rainfall Warning",
        description="More than 30 mm rain (intense to torrential) within 1 hour.\nEvacuate immediately — severe flooding expected.",
        color=0xE74C3C
    )

    embed5 = discord.Embed(
        title="✅ Safety Precautions",
        description=(
            "• Secure your house and roof.\n"
            "• Prepare emergency supplies and charge phones.\n"
            "• Stay indoors and away from windows.\n"
            "• Evacuate to higher ground if advised.\n"
            "• After the storm, avoid downed power lines and report damage."
        ),
        color=0x2ECC71
    )

    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)
    await ctx.send(embed=embed4)
    await ctx.send(embed=embed5)


@bot.command()
async def volcano(ctx):
    embed1 = discord.Embed(title="🌋 Active Volcanoes", description="- Mayon (Active)\n- Taal (Active)\n- Kanlaon (Active)\n- Bulusan (Restive)\n- Hibok-Hibok (Dormant)", color=0xE74C3C)
    embed2 = discord.Embed(title="📅 Activity (Last 5 Years)", description="- Mayon – 2023 eruption\n- Taal – 2022 phreatic eruption\n- Kanlaon – 2024 seismic activity", color=0xC0392B)
    embed3 = discord.Embed(title="⚠️ Precautions", description="Follow PHIVOLCS alerts and maintain a 6-km danger zone radius.", color=0x2ECC71)
    await ctx.send(embed=embed1)
    await ctx.send(embed=embed2)
    await ctx.send(embed=embed3)


@bot.command()
async def resources(ctx):
    embed = discord.Embed(
        title="🔗 Official Disaster Resources (Philippines)",
        description="Trusted websites for real-time updates and safety information.",
        color=0x27AE60,
    )

    embed.add_field(
        name="🌋 PHIVOLCS (Volcano & Earthquake Monitoring)",
        value="[https://www.phivolcs.dost.gov.ph](https://www.phivolcs.dost.gov.ph)",
        inline=False,
    )

    embed.add_field(
        name="🌧 PAGASA (Weather, Typhoon & Flood Alerts)",
        value="[https://bagong.pagasa.dost.gov.ph](https://bagong.pagasa.dost.gov.ph)",
        inline=False,
    )

    embed.add_field(
        name="🏛 NDRRMC (National Disaster Response)",
        value="[https://ndrrmc.gov.ph](https://ndrrmc.gov.ph)",
        inline=False,
    )

    embed.add_field(
        name="💬 DSWD (Relief & Social Services)",
        value="[https://www.dswd.gov.ph](https://www.dswd.gov.ph)",
        inline=False,
    )

    embed.add_field(
        name="🧭 Mines and Geosciences Bureau (Landslide Info)",
        value="[https://www.mgb.gov.ph](https://www.mgb.gov.ph)",
        inline=False,
    )

    embed.add_field(
        name="🛰 MMDA (Metro Manila Disaster Response)",
        value="[https://www.mmda.gov.ph](https://www.mmda.gov.ph)",
        inline=False,
    )

    embed.set_footer(text="Always rely on official sources for disaster information.")
    await ctx.send(embed=embed)


# ========================
# HELP COMMAND
# ========================

@bot.command()
async def helpdisaster(ctx):
    embed = discord.Embed(
        title="🌏 Disaster Preparedness Menu",
        description=(
            "React with an emoji below to learn about each disaster:\n\n"
            "🌎 — Earthquake\n"
            "🌧️ — Flood\n"
            "🏔️ — Landslide\n"
            "🌊 — Tsunami\n"
            "🌪️ — Typhoon\n"
            "🌋 — Volcanic Eruption\n\n"
            "Stay safe and informed! 💪"
        ),
        color=0x00FFFF,
    )
    message = await ctx.send(embed=embed)

    # Add the emojis
    emojis = ["🌎", "🌧️", "🏔️", "🌊", "🌪️", "🌋"]
    for emoji in emojis:
        await message.add_reaction(emoji)

    def check(reaction, user):
        return (
            user != bot.user
            and str(reaction.emoji) in emojis
            and reaction.message.id == message.id
        )

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120.0, check=check)
            emoji = str(reaction.emoji)

            if emoji == "🌎":
                embed = discord.Embed(
                    title="🌎 Earthquake Preparedness",
                    description=(
                        "**Definition:** Sudden shaking of the ground caused by movement of Earth’s crust.\n\n"
                        "**Active Fault Lines (PHIVOLCS):**\n"
                        "- West Valley Fault\n- East Valley Fault\n- Philippine Fault Zone\n"
                        "- Central Leyte Fault\n- Cotabato Fault System\n- North & South Mindanao Faults\n\n"
                        "**Precautions:** Secure heavy furniture, prepare emergency kits, know evacuation areas.\n"
                        "**During:** Drop, Cover, and Hold On. Stay away from windows.\n"
                        "**After:** Check for injuries, avoid damaged structures, expect aftershocks.\n\n"
                        "🔗 [PHIVOLCS FaultFinder](https://faultfinder.phivolcs.dost.gov.ph/)"
                    ),
                    color=0x2ECC71,
                )

            elif emoji == "🌧️":
                embed = discord.Embed(
                    title="🌧️ Flood Preparedness",
                    description=(
                        "**Flood-Prone Areas (PAGASA):** Metro Manila, Bulacan, Pampanga, Cagayan Valley, "
                        "Eastern Visayas, Davao Region, and Northern Mindanao.\n\n"
                        "**Rainfall Warning Levels (PAGASA):**\n"
                        "🟡 **Yellow:** 7.5–15 mm rain (Monitor weather updates)\n"
                        "🟠 **Orange:** 15–30 mm rain (Flooding possible; be alert)\n"
                        "🔴 **Red:** >30 mm rain (Severe flooding expected; evacuate immediately)\n\n"
                        "**Precautions:** Move to higher ground, unplug electrical devices, avoid floodwaters."
                    ),
                    color=0x3498DB,
                )

            elif emoji == "🏔️":
                embed = discord.Embed(
                    title="🏔️ Landslide Preparedness",
                    description=(
                        "**Definition:** Downward movement of soil or rock due to rain or earthquakes.\n\n"
                        "**Areas with Landslide History:** Benguet, Mountain Province, Ifugao, Leyte, Compostela Valley, Bukidnon.\n"
                        "**Causes:** Heavy rain, deforestation, earthquakes, steep terrain.\n\n"
                        "**Before:** Avoid building homes near steep slopes.\n"
                        "**During:** Move to stable ground immediately.\n"
                        "**After:** Stay away from landslide-prone zones until declared safe."
                    ),
                    color=0x8E44AD,
                )

            elif emoji == "🌊":
                embed = discord.Embed(
                    title="🌊 Tsunami Preparedness",
                    description=(
                        "**Definition:** Large sea waves caused by underwater earthquakes or volcanic eruptions.\n\n"
                        "**High-Risk Areas (PAGASA):** Coastal regions of Eastern Samar, Surigao, Davao Oriental, "
                        "Batanes, and other eastern seaboards.\n\n"
                        "**Before:** Know evacuation routes; be aware of sirens or official warnings.\n"
                        "**During:** If you feel a strong earthquake, move immediately inland or to higher ground.\n"
                        "**After:** Stay tuned for official all-clear announcements before returning."
                    ),
                    color=0x1ABC9C,
                )

            elif emoji == "🌪️":
                embed = discord.Embed(
                    title="🌪️ Typhoon Preparedness",
                    description=(
                        "**Definition:** Intense tropical cyclone bringing strong winds and heavy rain.\n\n"
                        "**Rainfall Warning (PAGASA):**\n"
                        "🟡 Yellow – 7.5–15mm: Be alert, monitor updates.\n"
                        "🟠 Orange – 15–30mm: Flooding possible, prepare to evacuate.\n"
                        "🔴 Red – >30mm: Serious flooding expected, evacuate immediately.\n\n"
                        "**Precautions:** Store clean water, secure roofs, charge devices, stay indoors."
                    ),
                    color=0xE67E22,
                )

            elif emoji == "🌋":
                embed = discord.Embed(
                    title="🌋 Volcanic Eruption Preparedness",
                    description=(
                        "**Active Volcanoes (PHIVOLCS):** Mayon, Taal, Kanlaon, Bulusan, and Pinatubo.\n\n"
                        "**Status (Last 5 Years):**\n"
                        "- **Mayon:** Active – Eruptions in 2018, 2023\n"
                        "- **Taal:** Active – Eruptions in 2020, 2021\n"
                        "- **Kanlaon:** Active – Increased activity 2023–2024\n"
                        "- **Bulusan:** Active – Minor eruptions 2022\n"
                        "- **Pinatubo:** Dormant – No eruptions since 1991, stable gas emissions\n\n"
                        "**Precautions:** Prepare masks for ashfall, avoid river valleys, follow evacuation orders."
                    ),
                    color=0xC0392B,
                )

            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send("⏰ Reaction timeout. Type `!helpdisaster` again to reopen the menu.")
            break


@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title="📘 Available Commands",
        description=(
            "`!info` — About this chatbot\n"
            "`!hotlines` — List of emergency hotlines\n"
            "`!time` — Show current date and time\n"
            "`!resources` — View official government websites\n\n"
            "**Disaster Commands:**\n"
            "`!earthquake` — Earthquake info and precautions\n"
            "`!flood` — Flood preparedness and alerts\n"
            "`!landslide` — Landslide precautions\n"
            "`!tsunami` — Tsunami evacuation guide\n"
            "`!typhoon` — Typhoon warnings and safety tips\n"
            "`!volcano` — Volcano updates and safety measures"
        ),
        color=0x95A5A6,
    )
    await ctx.send(embed=embed)


# ========================
# BOT STATUS
# ========================

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Type !commands"))

TOKEN="MTQzMzM0NjI4MDQ2NTI0MDA3NA.GUTpPB.LkL6b5mU9KaFXWRajuSWjqgAw0WkeA2MG4E7KE"
bot.run(TOKEN)


