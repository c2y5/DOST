import itertools
import sys
import time
import threading
import os
import fade

loadingBreak = False

os.system("title DOST v1.1")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def printTitle():
    print(fade.purpleblue("""
██████╗      ██████╗     ███████╗    ████████╗
██╔══██╗    ██╔═══██╗    ██╔════╝    ╚══██╔══╝
██║  ██║    ██║   ██║    ███████╗       ██║   
██║  ██║    ██║   ██║    ╚════██║       ██║   
██████╔╝    ╚██████╔╝    ███████║       ██║   
╚═════╝      ╚═════╝     ╚══════╝       ╚═╝   """))
    print("——————————————————————————————————————————————————")
    print("\033[90mDOST is a discord CDN based file host")
    print("Currently running DOST v1.0\033[0m")
    print("——————————————————————————————————————————————————\n")

clear()
printTitle()
print()

def _loading(text):
    global loadingBreak
    
    chars = "/—\|"

    for char in itertools.cycle(chars):
        if loadingBreak:
            print(f"\033[F{text}... \033[92mSuccess\033[0m\n")
            loadingBreak = False
            break

        sys.stdout.write('\033[F' + f'{text}... ' + char + "\n")
        sys.stdout.flush()
        time.sleep(0.1)

def loading(text):
    threading.Thread(target=_loading, args=(text,), daemon=True).start()

loading("Importing modules")

import discord
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from discord.ext import commands
import asyncio
import tkinter as tk
from tkinter import filedialog
import shutil
import gzip

loadingBreak = True
time.sleep(0.1)
loading("Initializing required functions")
def derive_key(key, salt, length=32):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(key.encode())

def encrypt(plaintext, key):
    salt = os.urandom(16)
    derived_key = derive_key(key, salt)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()  # No encoding needed
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(salt + iv + ciphertext)


def decrypt(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    salt = ciphertext[:16]
    iv = ciphertext[16:32]
    ciphertext = ciphertext[32:]
    derived_key = derive_key(key, salt)
    cipher = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

loadingBreak = True
time.sleep(0.1)
loading("Loading & checking config")
time.sleep(0.2)

if os.path.exists("./assets/config.json"):
    with open("./assets/config.json", "r") as f:
        config = json.load(f)
else:
    with open("./assets/config.json", "w") as f:
        json.dump({"BotToken": "", "ChannelID": 0}, f, indent=4)
    
    config = {"BotToken": "", "ChannelID": 0}

if not config["BotToken"] or config["ChannelID"] == 0 or not config["ChannelID"]:
    loadingBreak = True
    time.sleep(0.1)
    if not config["BotToken"]:
        while True:
            print("\033[38;2;235;52;52m[Config Error - Bot Token]\033[0m")
            print("Please enter the bot token")
            Token = input("> ")
            if not Token:
                print("\033[38;2;235;52;52mInvalid bot token")
            else:
                config["BotToken"] = str(Token)
                break

    if not config["ChannelID"] or config["ChannelID"] == 0:
        while True:
            print("\033[38;2;235;52;52m[Config Error - Channel ID]\033[0m")
            print("Please enter the channel ID")
            ID = input("> ")
            if not ID or not ID.isnumeric():
                print("\033[38;2;235;52;52mInvalid channel ID")
            else:
                config["ChannelID"] = int(ID)
                break
    
    print()
    loading("Saving new config file")
    
    with open("./assets/config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    time.sleep(0.2)
    loadingBreak = True
    time.sleep(0.1)
else:
    loadingBreak = True
    time.sleep(0.1)

loading("Reading data")

if os.path.exists("./assets/data.json"):
    with open("./assets/data.json", "r") as f:
        data = json.load(f)
else:
    with open("./assets/data.json", "w") as f:
        json.dump({}, f, indent=4)
    
    config = {}

loadingBreak = True
time.sleep(0.1)

loading("Starting discord client")
client = commands.Bot(command_prefix='DOST.Self.', intents=discord.Intents.all())

def startBot():
    client.run(config["BotToken"])

orig_stdout = sys.stdout
orig_stderr = sys.stderr
sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")
threading.Thread(target=startBot, daemon=True).start()
sys.stdout = orig_stdout
sys.stderr = orig_stderr
time.sleep(3)
loadingBreak = True
time.sleep(0.1)

def listUploads():
    clear()
    printTitle()
    if len(data) < 1:
        print("\033[33mNo files uploaded yet\033[0m\n")
        print("\033[90mPress enter to go back\033[0m")
        input()
        main()
    else:
        print(f"\033[90mYou currently have \033[0m{len(data)}\033[90m file{'' if len(data) < 2 else 's'} uploaded\033[0m\n")
        Count = 1
        for x in data:
            print(f"\033[90m{str(Count)})\033[0m {x}")
            Count += 1

    print("\033[90mPress enter to go back\033[0m")
    input()
    main()

def printInfo():
    clear()
    printTitle()
    print("""DOST is a discord CDN based file host
It utilizes discord bot and discord's free 25MB file upload
To store your files online.

DO \033[38;2;235;52;52mNOT\033[0m USE THIS AS A BACKUP, USE A \033[92mPROPER\033[0m HOSTING SERVICE FOR \033[93mIMPORTANT\033[0m FILES
DISCORD \033[38;2;235;52;52mCAN DELETE\033[0m YOUR FILES & SERVER WITHOUT NOTICE
YOU WILL \033[38;2;235;52;52mNOT\033[0m BE ABLE TO RESTORE THE FILES""")
    
    print("\n\033[90mPress enter to go back\033[0m")
    input()
    main()

def printMenu():
    choices = """—————————————————————————————————
|  [1] - List uploaded files    |
|  [2] - Upload a file          |
|  [3] - Download a file        |
|  [4] - Deletes a file         |
|  [5] - Info                   |
|  [6] - Exit                   |
—————————————————————————————————
    """
    print(choices)

def downloadFile():
    clear()
    printTitle()
    if len(data) < 1:
        print("\033[33mNo files to download\033[0m\n")
        print("\033[90mPress enter to go back\033[0m")
        input()
        main()
    else:
        print(f"\033[90mYou currently have \033[0m{len(data)}\033[90m file{'' if len(data) < 2 else 's'} uploaded\033[0m\n")
        Count = 1
        List = {}
        for x in data:
            print(f"\033[90m{str(Count)})\033[0m {x}")
            List[str(Count)] = x
            Count += 1

        print(f"\n\033[90m{str(Count)})\033[0m All")
        print(f"Please choose which file you would like to download, enter '{str(Count)}' to download all")
        print("You may place a coma (,) to download multiple files (eg: 1,2,3)")
        choice = input("> ")
        choice = choice.replace(" ", "").split(",")
        
        if str(Count) in choice:
            choice.clear()
            for ___ in range(1, Count):
                choice.append(str(___))
        
        clear()
        printTitle()
        
        async def getFile(datac, __):
            global loadingBreak
            
            saveName = list(data.keys())[int(__)-1]
            
            loading(f"Getting data for file: {saveName}")
            
            attachmentAmount = len(datac["ids"])
            downloaded = 1
            for x in datac["ids"]:
                channel = client.get_channel(config["ChannelID"])
                msg = await channel.fetch_message(x)
                loadingBreak = True
                time.sleep(0.1)
                for attachment in msg.attachments:
                    loading(f"Downloading {saveName} | Chunck {str(downloaded)}/{attachmentAmount}")
                    await attachment.save(fp=f"./assets/temp-download/{attachment.filename}.temp")
                    downloaded = downloaded + 1
                    loadingBreak = True
                    time.sleep(0.1)
            
            files = [f for f in os.listdir("./assets/temp-download") if os.path.isfile(os.path.join("./assets/temp-download", f))]
            ff = len(files)
            fff = 1
            for x in files:
                loading(f"Decrypting {saveName} | Chunck {str(fff)}/{ff}")
                with open(os.path.join("./assets/temp-download", x), "r") as f:
                    decryptedContent = decrypt(f.read(), "f697c771-2882-4d66-bc24-72727c878169")
                
                loadingBreak = True
                time.sleep(0.1)
                loading(f"Adding chunck {str(fff)}/{ff} to {saveName}.gz")
                with open(f"./downloads/{saveName}.gz", "ab") as _:
                    _.write(decryptedContent)
                    
                fff += 1
                loadingBreak = True
                time.sleep(0.1)
                
                loading(f"Removing chunck {str(fff-1)} temp")
                os.remove(os.path.join("./assets/temp-download", x))
                loadingBreak = True
                time.sleep(0.1)

            with gzip.open(f"./downloads/{saveName}.gz", 'rb') as f_in:
                with open(f"./downloads/{saveName}", 'wb') as f_out:
                    f_out.write(f_in.read())

            os.remove(f"./downloads/{saveName}.gz")

        for x in choice:
            if data[List[x]]:
                re = asyncio.run_coroutine_threadsafe(getFile(data[List[x]], x), client.loop)
                re.result()
            
        print("\n\033[0mDownload \033[92msuccess\033[0m! Files are in \033[92mdownloads\033[0m folder")
        print("\033[90mPress enter to go back\033[0m")
        input()
        main()

def deleteFile():
    clear()
    printTitle()
    if len(data) < 1:
        print("\033[33mNo files to delete\033[0m\n")
        print("\033[90mPress enter to go back\033[0m")
        input()
        main()
    else:
        print(f"\033[90mYou currently have \033[0m{len(data)}\033[90m file{'' if len(data) < 2 else 's'} uploaded\033[0m\n")
        Count = 1
        List = {}
        for x in data:
            print(f"\033[90m{str(Count)})\033[0m {x}")
            List[str(Count)] = x
            Count += 1

        print(f"\n\033[90m{str(Count)})\033[0m All (Sometimes broken)")
        print(f"Please choose which file you would like to delete, enter '{str(Count)}' to delete all")
        print("You may place a coma (,) to delete multiple files (eg: 1,2,3)")
        choice = input("> ")
        choice = choice.replace(" ", "").split(",")
        
        if str(Count) in choice:
            choice.clear()
            for ___ in range(1, Count):
                choice.append(str(___))
        
        clear()
        printTitle()
        
        async def delFile(datac, __):
            global loadingBreak, List
            
            saveName = list(data.keys())[int(__)-1]
            
            loading(f"Getting data for file: {saveName}")
            
            c = len(datac["ids"])
            cc = 1
            for x in datac["ids"]:
                channel = client.get_channel(config["ChannelID"])
                msg = await channel.fetch_message(x)
                loadingBreak = True
                time.sleep(0.1)
                loading(f"Deleting {saveName} (Chunck {str(cc)}/{c}) from discord")
                await msg.delete()
                cc += 1
                loadingBreak = True
                time.sleep(0.1)
            
            loading("Deleting discord data from local machine")
            data.pop(saveName)
            loadingBreak = True
            time.sleep(0.1)
            loading("Saving new data")
            with open("./assets/data.json", "w") as f:
                json.dump(data, f, indent=4)
            loadingBreak = True
            time.sleep(0.1)
            
        for x in choice:
            if data[List[x]]:
                re = asyncio.run_coroutine_threadsafe(delFile(data[List[x]], x), client.loop)
                re.result()
            
        print("\n\033[0mDeleted \033[92msuccessfully\033[0m!")
        print("\033[90mPress enter to go back\033[0m")
        input()
        main()

def upload():
    global loadingBreak
    
    clear()
    printTitle()
    loading("Waiting for user to select file")
    root = tk.Tk()
    root.withdraw()
    fpath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("All files", "*.*"),)
    )
    time.sleep(0.1)
    loadingBreak = True
    time.sleep(0.1)
    loading("Zipping file")
    with open(fpath, "rb") as f:
        with gzip.open("./assets/upload-temp/"+os.path.basename(fpath)+".gz", "wb") as zf:
            zf.writelines(f)

    loadingBreak = True
    time.sleep(0.1)
    origionalfname = os.path.basename(fpath)
    fpath = "./assets/upload-temp/"+os.path.basename(fpath)+".gz"
    loading("Calculating size")
    fsize = os.path.getsize(fpath)
    
    async def uploadFile(fname, filepath, fname2):
        global loadingBreak
        loading("Encrypting file")
        with open(filepath, "rb") as f:
            unencrypted = f.read()
            
        with open(filepath, "wb") as f:
            f.write(encrypt(unencrypted, "f697c771-2882-4d66-bc24-72727c878169"))
        loadingBreak = True
        time.sleep(0.1)
        channel = client.get_channel(config["ChannelID"])
        if channel:
            loading("Uploading file")
            with open(filepath, "rb") as f:
                msg = await channel.send(file=discord.File(f, filename=fname2))
                msgid = msg.id
                loadingBreak = True
            time.sleep(0.1)
            loading("Modifying data")
            if not fname in data:
                data[fname] = {}

            if not "ids" in data[fname]:
                data[fname]["ids"] = []
                
            data[fname]["ids"].append(int(msgid))
            
            with open("./assets/data.json", "w") as f:
                json.dump(data, f, indent=4)
            loadingBreak = True
            
        time.sleep(2)
        loading("Removing upload temp")
        os.remove(filepath)
        loadingBreak = True
        time.sleep(0.1)
    
    loadingBreak = True
    time.sleep(0.1)
    
    if fsize >= 18*1024*1024:
        print("\nFile > 25MB")
        chunckAmount = (fsize+(18*1024*1024)-1) // (18*1024*1024)
        print(f"Total chuncks: {str(chunckAmount)}")
        print("\n")
        cm = 1
        with open(fpath, "rb") as f:
            for i in range(chunckAmount):
                loading(f"Splitting chunck {str(cm)}/{str(chunckAmount)}")
                chunk = f.read(18*1024*1024)
                with open(f"./assets/upload-temp/{os.path.basename(fpath)}.chunck{i+1}.txt", "wb") as cf:
                    cf.write(chunk)
                loadingBreak = True
                time.sleep(0.1)
                re = asyncio.run_coroutine_threadsafe(uploadFile(origionalfname, f"./assets/upload-temp/{os.path.basename(fpath)}.chunck{i+1}.txt", f"{os.path.basename(fpath)}.chunck{i+1}.txt"), client.loop)
                re.result()
                cm += 1
    else:
        print("File < 25MB\n")
        shutil.copy(fpath, f"./assets/upload-temp/{os.path.basename(fpath)}.txt")
        
        re = asyncio.run_coroutine_threadsafe(uploadFile(os.path.basename(fpath), f"./assets/upload-temp/{os.path.basename(fpath)}.txt", origionalfname), client.loop)
        re.result()
    
    os.remove(fpath)
    print("\033[90mPress enter to go back\033[0m")
    input()
    main()
        
def main():
    clear()
    printTitle()
    printMenu()

    while True:
        print("Enter an option")
        option = input("> ")
        
        if not option.isnumeric():
            print("\033[38;2;235;52;52mInvalid Choice\033[0m")
            continue
        
        if int(option) > 6 or int(option) < 1:
            print("\033[38;2;235;52;52mInvalid Choice\033[0m")
            continue
        
        break
    
    if option == "1":
        listUploads()
    elif option == "2":
        upload()
    elif option == "3":
        downloadFile()
    elif option == "4":
        deleteFile()
    elif option == "5":
        printInfo()
    elif option == "6":
        sys.exit()
      
main()