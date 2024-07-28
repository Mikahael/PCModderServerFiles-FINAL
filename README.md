# 𝐵𝑜𝓂𝒷𝓈𝓆𝓊𝒶𝒹1.4||𝐹𝓊𝓁𝓁𝒮𝑒𝓇𝓋𝑒𝓇𝐹𝒾𝓁𝑒𝓈[𝒫𝒞𝑀𝑜𝒹𝒹𝑒𝓇] (UPDATED - 5.0)-FINAL - VERSION!
- How to run server : 

- Download the file - extract in the server

- Open terminal, install python or run the followng commands :
  - cd <your_bs_folder>
  - sudo apt-get update -y
  - sudo apt-get install -y python2.7-dev
  - chmod 777 bombsquad_server
  - chmod 777 config.py
  - chmod 777 bs_headless
  - pkill -f tmux
  - tmux
  - ./bombsquad_server
 
- Edit the files for simple changes
  - fire.py - server settings - includes welcome msg
  - settings_spaz - player settings
  - settings_bomb - bomb settings
  - settings_powerups - powerup settings
  - getPermissionsHashes - add owner/admin hashes
  - bsTextOnMap - to change textonmap

- Edit for powerup dist changes
  - dist_vanilla - default powerups
  - dist_regular - regular powerups with extra
  - dist_modded - full modded powerups
  - enable the dist you want in setttings_powerups.py
    - make sure both dist values never becomes true
    - both dist values false means, dist_regular turned true
  
- What has changed in this 5.0 version?
  - added endvote - /endvote to start, /vote to vote
  - improved chat filter
  - chat commands now transient
  - coinsystem more transient
  - time added in textonmap
  - member_count added in textonmap
  - authentication mod has been added
    - enable it in fire.py under authentication
    - no one can spoof id else kick
  - scoreboard and gamename changes
  - improved whitelist
    - use /white to add players
    - use ?whitelist to start setting
    - server will restart at once whitelist enabled
   
- Prevent Brute Entry attacks - fail2ban
  - mod to prevent hackers crashing server or gaining entry
  - install fail2ban module
    - sudo apt-get update
    - sudo apt-get install fail2ban
  - configure the module
    - open the folder - /etc/fail2ban/
      - open jail.local file
      - change bantime value to -1
      - change findtime value to 30
      - change maxentry value to 3
        - three chances to enter correct or ban
      - use cntrl+f to search for the terms, and change values as said
      - save the file
  - open terminal and enter commands
    - sudo systemctl start fail2ban
    - sudo systemctl enable fail2ban
  - Server will now ban all those trying to brute entry attack - usefull
  - Will work depending on the attack
  
# 𝒲𝒽𝒶𝓉 𝒾𝓉 𝒞𝑜𝓃𝓉𝒶𝒾𝓃𝓈

- Enjoy the full beauty of Ankit System and PCModder System

- Can be used in server builds and client builds

- Contains 2 admin systems in 1 big package.
 
- Stongest Admin system to be ever created ~

- A total of 73 powerups with triple configuration

- Special roles for friends or top players

- Top Notch server commmands for configuration in real time

- Live New Bombsquad Textures configured in real time

- Players can use any Characters even if they dont have

- Awesome New mods such as PCFloater

- Live time working whitelist and ban list

- Full working server files created by Avarohana or PCModder

# 𝒯𝒽𝒶𝓃𝓀𝓈

- Thanks to PCModder/PC231392/PC290717/Avarohana/Arohana(All are Me)

- Thanks to Blitz

- Thanks to SobyDamn

- Thanks to Vortex

- Thanks to Vivek

- Thanks to Bombdash

- Thanks to Esie-Eyen

- Thanks to Knight
  
- Special thanks to ByAngel3L and Froshlee14

Thank You for all Using, kindly to give me some credit to those who use,
Avarohana/PCModder

# 𝒮𝑒𝓇𝓋𝑒𝓇 𝒞𝑜𝓂𝓂𝒶𝓃𝒹𝓈

- A few special server commands -

- For PC commands use '?'

- For Ankit commands use '/'

- ?verification

- ?mute

- ?teamMode on

- ?ffaMode on

- ?floater

- ?maps

- ?shower and ?snowy

- /endvote to start endvote

- /vote to vote for endvote

- View Full Cmds in commmandList.pdf or scroll down

# 𝐻𝑜𝓌 𝓉𝑜 𝓊𝓈𝑒 𝓌𝒽𝒾𝓉𝑒𝓁𝒾𝓈𝓉

- To enable or disable whitelist, use ?whitelist

- To add a whitelisted client, use /white (ID) add

- To remove a whitelisted client, open getPermissionHashes.py and
 remove the id under whitelist hashes.

- Server will restart after enabling whitelist

# 𝒞𝒽𝒶𝓉 𝐹𝒾𝓁𝓉𝑒𝓇𝓈 𝒶𝓃𝒹 𝒩𝒶𝓂𝑒 𝐹𝒾𝓁𝓉𝑒𝓇𝓈

- Server filters both chat messages and Names!

- To add a word to chat fiter, open fiter.py and add the word
 in the f_word hashes.
 
- To add a word to the Name filter, open filter.py and add the
 name in the name_filter hashes.
 
- Anyone with blacklisted name gets kicked immedietly

# Add or Remove roles

- Roles work on both systems

- Roles include admin, vip, mod, owner, owner2, mod2

- owner2 and mod2 are tags with permissions, but tag name is emoty

- Use owner2, owner, mod2 using --> ?owner2 instead of /owner2

- For custom tag, use the defualt ankit system tag

- For PC tag, use ?dtag, ?ctag, ?ftag, ?tag (ID) add or remove

- To MUTE, use ?mute (ID) add or remove - muted until id removed

- To BAN, use /ban (ID) add or remove - defualt ankit sys layout

#To whom ever this may concern, All rights to Mikahael aka PCModder/Avarohana as the License states above.

# 𝒜𝓊𝓉𝑜𝒩𝒾𝑔𝒽𝓉𝑀𝑜𝒹𝑒 𝒶𝓃𝒹 𝒮𝑒𝓇𝓋𝑒𝓇 𝒞𝑜𝓂𝓅𝓁𝒶𝒾𝓃𝒾𝓃𝑔

- Server features an auto night mode

- To enable the time, open the terminal, and change the TIMEZONE to desired

- Example - sudo timedatectl set-timezone <your_time_zone>

- Find your timezone in terminal - timedatectl list-timezones

- Server has arranged a way for clients to complain to owner for improvments

- View complaints in complaints.txt in first directory, next to bs_headless.py, not scripts

- Use comp (your message here) + add your name to the complaint

- Example - comp they are teaming, comp add this powerup to server

# 𝐿𝑜𝑔𝑔𝒾𝓃𝑔 𝒻𝑒𝒶𝓉𝓊𝓇𝑒𝓈

- Server has many logging features

- Open complaints.txt to see complaints log

- Use kicklog.txt to see who has been kicked

- Use cmdlog.txt to see which commands admins/vips or owners have been using

# 𝒮𝓅𝑒𝒸𝒾𝒶𝓁 𝒞𝑜𝓂𝓂𝒶𝓃𝒹𝓈 𝒻𝑜𝓇 𝒢𝒶𝓂𝑒

- Includes the special commands owner or admins can use for server

- ?? special text for OWNERS only,
 Example - ??hey_guys
 Dont use spaces, use something else like .
 Example - ?? hey_guys_how_are_you or ?? hi,guys,bye
 
- ? special text for ADMIN/MOD only,
 Example - ??hey_guys
 Dont use spaces, use something else like .
 Example - ?? hey_guys_how_are_you or ?? hi,guys,bye

- ?tag - enables tag for every person

- ?charf - forces everyone to use that char perm until turned off,
 Works with wizard, pixie, ninja, santa, robot, ali, frosty, pengu,
 Example - ?wizardf, to turn off, type same command again
 
- ?rchar - forces everyone to use a random char perm,
 Example - ?rchar,
 To diable, type ?rchar or type same command again
 
- ?(bombtype)shower 0 - enables meteor shower with specified bomb,
 Works with bombtypes - normal, sticky, ice, cursy, frozen, pwp, glue, impact,
 Example - ?nomalshower 0, ?stickyshower 0,
 There is no disabling it - stops at end of match
 
- ?(snowtype)snow 0 - enables snow on maps,
 Works with sweat, ice, spark, splinter, slime,
 Example - ?sweatsnow 0, ?sparksnow 0, etc,
 There is no disabling it - stops at end of match

- ?pow(emittype) - enables pwp emition with specified emittype,
 Works with sweat, slime, splinter, ice,
 Example - ?powslime, ?powice, ?powsplint, ?powsweat,
 To distable, type the same command again
 
- ?color - changes color of player when punch button pressed,
 Example - ?color,
 To disable, type ?color or same command again
 
- ?randomchar - changes character of player when hold button pressed,
 Example - ?randomchar,
 To disable, type ?randomchar or same command again
 
- ?(bombtype)f - changes default bombtype to desire,
 Works with shock, ice, sticky, spike, glue, impact, knock,
 Example - ?shockf, ?icef, ?stickyf, etc,
 To disable, type same command again,
 Use only one default bomb at a time! Dont mix and match

- ?hp - enabled HP tag for players,
 Example - ?hp,
 To disable, type the same command again,
 When used, removes PC tag and rank tag
 
- ?shieldf - enables default shield for players,
 Example - ?shieldf,
 To disable, type the same command again
 
- ?glovef - enables default gloves for players,
 Example - ?glovef,
 To disable, type the same command again
 
- ?maps - enables new maps textures,
 Example - Use ?map1 or ?map2, then type what it says,
 Use /reset to disable the map until game over
 
- ?pwp - enables or disables the powerup,
 Example - ?pwp,
 To disable, type the same command again
 
- ?vanilla - enables default pwp distribution,
 Example - ?vanilla,
 To disable, type the same command again,
 Do not use with ?powerups, disable ?powerups if on, then use
 
- ?powerups - enables PC powerups, or modded powerups,
 Example - ?powerups,
 To disable, type the same command again,
 Do not use with ?vanilla, disable ?vanilla if on, then use
 
- ?bombmodel - enables new bombmodel for all bombs,
 Example - ?bombmodel,
 To disable, type this same command again
 
- ?powerupname - enables or disables powerup name,
 Example - ?powerupname,
 To disable or enable, type ?powerupname or same command again
 
- ?animate - enables flashy name color on pwp and bomb, and shield on bomb,
 Example - ?animate,
 To disable, type ?animate or same command again
 
- ?discolight - enables discolight on the powerups,
 Example - ?discolight,
 To disable, type ?discolight or same command again
 
- ?bombname - enables or disables bomb name,
 Example - ?bombname,
 To disable, type ?bombname or same command again
 
- ?ffaMode on - enables ffamode immediately,
 Example - ?ffaMode on,
 To revert back to teammode, use ?teamMode on

- ?teamMode on - enables teammode immediately,
 Example - ?teamMode on,
 To revert back to ffamode, use ?ffaMode on
 
- ?plo - enables or disables explosion when powerup spawns,
 Example - ?plo,
 To disable, type ?plo or the same command again
 
- ?pop - enables or disables popuptext when pwp touched,
 Example - ?pop,
 To disable, type ?pop or same command again
 
- ?flash - enables or disables powerup model addition,
 Example - ?flash,
 To disable, type ?flash or same command again
 
- ?lightning - enables or disables powerup lightning effect,
 Example - ?lightning,
 To disable, type ?lightning or same command again
 
- ?floater - enables floater to be turned on
 Example - ?floater,
 To disable, type ?floater or same command again,
 During daytime, floater is regular/landmine floater,
 During night time, floater is PC floater
 
# Concerns/AutoRole

- Server has rank system enabled

- Auto admin and auto vip works on commands

- To update ADMIN in top 1, type /auto admin

- To update VIP in top 4, type /auto vip
 
~ To whomsoever this may concern, all rights to PCMODDER/PC231392/Mikahael, as the license states.
