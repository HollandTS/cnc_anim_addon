This is a blender addon for if you have a model ready with animations, to make all your anims rotate all desires facings. Plus it will output the **complete** art.ini for both vehicles and infantry sequence in the text editor.

This addon is created for creating sprites for the game Red Alert 2 and Tiberian Sun, but it might be usefull for other purposes.

I used chatGPT to create this addon. Created this to help with unit creating workflow, it gets the job done alot faster then manually creating an empty and rotating the animations occordingly.

Updated Preview pic:
![2025-01-26 12_53_36-_ bison_mech_addontesting  F__tibsun shit_blendah files_bison_mech_addontesting](https://github.com/user-attachments/assets/05d2f616-f572-4aaa-85ec-e9b48319fa14)


0 (optional) - Scale your animations if needed:
On top of the UI, a simple scale feature to quickly adjust your animation frame count:
![scale](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/0828097d-957b-4460-a238-ccda9e58fb09)

1 - Choose if you have a infantry model or a vehicle model, pick the art.ini keys that you want, and assign the anims to them:
![pick_anims](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/5c404900-b949-4eb7-bef6-64a3b2887345)

*Update: enable 'Loop Clip' checkbox (see gif at bottom) for animations with a single frame, such as StandingFrame, Ready, Guard, Prone, etc. This should also be checked if the anim has a Loop Clip (first and last frame are the same). *

2 - Select the rig and press Execute. ~~After (or before) clicking Execute, you have to remove any leftover strips that automatically got inserted into the NLA editor, 
simply push down on the anim (in my case, 'attack'), and press X to remove it:
Now all your anims should properly play each direction :)~~  **(fixed)**

3 - check the text editor for the generated art.ini
![check_ini](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/e8911dd2-6d14-4efa-af0b-320ea784c17f)

~~Important:
for infantry, the 3rd numbers are left out, please do these manually (mostly they are the same nr as the 2nd nr, except for single anims like idle1/2, die1/2).
I have tried to add a third dropdown menu to pick a single direction ( e.g. die1, idle1, etc), but i havn't been succesfull so far 
so i recommend to put these anims last, and either edit the strips, or simply remove the redundent frames from the sprite~~
**(fixed)**

This is my first project in Phyton, and been a good learning practice despite ChatGPT doing most of the work. I probably won't do any requests, but i'll try to keep up with bug fixes.
Use or edit this addon however you want :)


__________________________________
Update 2024-06-02
- Added Additional dropdown box to pick a single direction (perfect for anims that only have 1 direction like idle1, idle2, die1 etc.)
- Added a simple button to quickly keyframe rotations, perfect for ~~standing frames~~ and turrets.

## Update 2025-01-26

- Renamed Addon to AnimFacer CnC Addon
- Replaced empty with a circle and arrow for facing direction.
- Added 'Loop Clip' checkbox for animations with a single frame, such as StandingFrame, Ready, Guard, Prone, etc. This should also be checked if the anim has a Loop Clip (first and last frame are the same).
- Ensured NLA strips appear on the top layer upon execution and mute all other strips.
- Set the rendering range from start to end.
- Integrated new INI processor to generate a complete art.ini Infantry Sequence in the Text Editor.
- Corrected the vehicle INI key 'StartAnimFrames' to 'StartAnimFrame', and related keys too.
- Enhanced UI design for improved user experience.
- Increased the size of the Execute button.
- Added 'Skip Frames' slider for the 'Rotate Selected Object' feature, useful for additional objects like muzzle flashes and blood effects.
- Included all available YR infantry sequences.
- Adjusted default order of infantry sequences in the UI.
- Fixed error message when clicking 'Add Animation'.
- Split the code into multiple Python files for better organization and maintainability.
  ![AnimFacer CnC Addon](https://github.com/user-attachments/assets/1b6e9714-615c-47c0-a02e-75e9c83e7e18)
