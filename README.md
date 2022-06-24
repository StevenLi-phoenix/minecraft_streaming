# minecraft_streaming

This project is used for streaming in minecraft through webcam

using the "function" function in minecraft to do that.
1. Create datapack in minecraft
2. change file_path to the functions folder
3. INGAME: using two command block to run reload command and function command


main function:

- update() or blockid2rgb.py

  using texture pack picture to convert minecraftid with avg rgb value and save in json file
  
- class matchBlock or rgb2blockid.py

  using rgb value to find the best match block texture with the avg rgb json file
  
- class stream

  using camera pic and save files to game path
  
 Warnning: not sure why it sometimes lagging and stuck, but mannual reload and execute helped.
 
 Warnning: Old version of this is using brute force to find match rgb2blockid, this may take hours, depending on computer, for my trash computer it take 2 hrs to complete. Although this find optimal solution it is too slow.
 
 todo: change algorithm.
