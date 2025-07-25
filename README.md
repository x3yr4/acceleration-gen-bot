# 🚀 Acceleration G3N – Free Discord Generator Bot

A powerful, open-source **Discord Gen Bot** built with Python and `discord.py`, featuring category-based account generation, admin tools, and beautiful embeds. Designed by **acceleration.back** to bring premium functionality to everyone – for free.

---

## 🧩 Features

✅ `.gen` – Generate account to user DM (1-hour cooldown)  
✅ `.stock` – Display available & out-of-stock categories  
✅ `.create`, `.delete` – Create or remove stock categories  
✅ `.add` – Upload `.txt` account files  
✅ `.set` – Configure server-specific keys (channels, roles, etc.)  
✅ `.kick`, `.ban`, `.timeout` – Advanced moderation tools  
✅ 🎨 Colorful embedded logs & UI  
✅ 🔐 Role-based access for commands  
✅ 🔔 Restock alerts (soon)  

---

## 📸 Screenshot Preview

<a href='https://postimg.cc/5Yw6qcxd' target='_blank'><img src='https://i.postimg.cc/5Yw6qcxd/Screenshot.jpg' border='0' alt='Screenshot'/></a>
---

## ⚙️ Command Guide

```bash
.stock <Usage>           # Displays available and out-of-stock categories  
.gen <category> <Usage>  # Public command - Sends account to DM (1-hour cooldown)  
.create <category> <Admin>     # Create a new stock file  
.delete <category> <Admin>     # Delete a stock category  
.add <category> (attach.txt) <Admin>   # Upload account list  
.set <key> <value> <Admin>     # Set keys like vouch_channel, access_role, etc.  
.kick @user <reason> <Admin>   # Kick a user with reason  
.ban @user <reason> <Admin>    # Ban a user with reason  
.timeout @user <duration> <reason> <Admin>  # Timeout a user (1h/1d/1w)
