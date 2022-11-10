# 🤖 ESP Controller with Telegram Bot (MicroPython)

- 🔥 With this code you can control yoyr electronic things
- ⚡️ **[click here for connect to author](https://t.me/Soltan_Python)**

# ⚙ config

**Go to the `config.json` file** :

- 📌 connect a jumper wire to your pin then connect the jumper to your electronic thing , Now add your GPIO pin number to the `pins` list

- 📌 if you want all pins in the `pins` list to be turned off when the program runs, change the `auto_off_pins` value to `true`

- 📌 you must add your Telegram bot token to the `token` variable in line 5

- 📌 add the SSID of your wireless router or access point to the `SSID` variable

- 📌 add the password of your wireless router or access point to the `key` variable

- 📌 the `API_URL` variable is optional. if Telegram is filtered in your country, you can use this variable. how is works? You need to deploy [this API]() to a host or server (I use www.Deta.sh) then add your "API URL" to the `API_URL` variable. But if you don't have problem with Telegram APIs, don't change the `API_URL` value

- 📌 Finally, add the user ID of your Telegram bot admins in the `ADMIN` list variable
