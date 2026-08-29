## <font color="#92cddc">Rook Sacrifice Detector</font>
<p align="center">
  <img width="200" height="200" alt="icon" src="https://github.com/user-attachments/assets/ef99d1b8-4a7f-4a38-b4df-7578cff51221" />
</p>

---
**<h1 align="center">♟️ Take My ROOOOOOOOOOK! ♟️</h1>**

<p align="center">A Python application that analyses your Chess.com games for rook sacrifices- ALL rook sacrifices (you'll see what I mean😁)</p>

### 📂 The Project
- It uses the Chess.com PubAPI to gather all your **public** games & the **python-chess** library to parse through each game. A heuristic is used to determine if the capture of a rook is a sacrifice: if the player who gave up the rook receives more than 5 points of material (the value of a rook) in the next 6 moves, then it's likely not a sacrifice.
- If they receive less than 5, then it may be a sacrifice.
- But, I'm not that sure how sound this really is because I think it counts blunders too (I mean, ig they're BAD rook sacs? 😁). If you have any better ideas, feel free to share them in the Ideas categories in the Discussions.
- After identifying the rook sacs, the program will display how many that you have & open a Matplotlib window to display the games with rook sacs

- This was initially a website I made with a lot of help from AI (wanted to try what vibe-coding was about).

![](https://github.com/Coder-kanji95/sacrifice-the-rook/blob/main/aw-heck-naw.gif)

- But that fell apart quick when the website wasn't counting any rook sacs & me, with my VERY mediocre knowledge of JS, had no idea what was wrong or how to fix it (so yes, another example of why you shouldn't vibe-code💀 an entire project, especially as a beginner (like myself)😔)
- But, I must confess, I did use ChatGPT while making the Python app, for figuring out some python-chess stuff & how to move pieces on a chessboard on MATPLOTLIB

Anywayyy.....on to the installation.....

### 💾 Installation
Go to the website (https://coder-kanji95.github.io/sacrifice-the-rook/) & download the EXE for your OS (currently, it's just Windows but I'm gonna add macOS & Linux in the coming days)

**If you encounter any errors or trouble when trying to run the EXE, create an Issue & I'll address the problem as fast as I can :)**

### 🧑‍💻 Possible Future Updates
- ~~Inclusion of bot games when checking for rook sacrifices~~ ✅
- ~~Displaying the games with the rook sacrifices (as opposed to just telling the number of rook sacrifices across games)~~ ✅
- ...

### 💬 Discussions & Feedback
https://github.com/Coder-kanji95/sacrifice-the-rook/discussions 
- You can share your thoughts & opinions under the 'General' category (and just chat :)) in the Discussions or email wrathnofnmathn@gmail.com 
- Share ideas for features under the 'Ideas' category in the Discussion, ask questions under 'Q&A' & watch for posts from me under 'Announcements'!

🔥🔥🔥 [https://www.youtube.com/watch?v=08jEcWKzxWU](https://www.youtube.com/watch?v=08jEcWKzxWU) 🔥🔥🔥🔥

P.S Feel free to inspect the source code :)
