This is a blender addon for if you have a model ready with animations, to make all your anims rotate all desires facings. Plus it will output the art.ini in the text editor.
Note: This addon is created for creating sprites for the game Red Alert 2 and Tiberian Sun, but it might be usefull for other purposes.
I used chatGPT to create this addon, its not perfect but gets the job done alot faster then manually creating an empty and rotating the animations occordingly.

0 (optional) - Scale your animations if needed:
On top of the UI, a simple scale feature to quickly adjust your animation frame count:
![scale](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/0828097d-957b-4460-a238-ccda9e58fb09)

1 - Choose if you have a infantry model or a vehicle model, pick the art.ini keys that you want, and assign the anims to them:
![pick_anims](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/5c404900-b949-4eb7-bef6-64a3b2887345)

2 - Select the rig and press Execute. After (or before) clicking Execute, you have to remove any leftover strips that automatically got inserted into the NLA editor, 
simply push down on the anim (in my case, 'attack'), and press X to remove it:
![remove_other](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/d8349e52-c927-4260-87fc-14837fda01c9)
Now all your anims should properly play each direction :)

3 - check the text editor for the generated art.ini
![check_ini](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/e8911dd2-6d14-4efa-af0b-320ea784c17f)

Important: 
- for infantry, the 3rd numbers are left out, please do these manually (mostly they are the same nr as the 2nd nr, except for single anims like idle1/2, die1/2).
I have tried to add a third dropdown menu to pick a single direction ( e.g. die1, idle1, etc), but i havn't been succesfull so far 
so i recommend to put these anims last, and either edit the strips, or simply remove the redundent frames from the sprite

This is my first project in Phyton, and been a good learning practice despite ChatGPT doing most of the work. I probably won't do any requests, but i'll try to keep up with bug fixes.
Use or edit this addon however you want :)


__________________________________
Update:

- Added Additional dropdown box to pick a single direction (perfect for anims that only have 1 direction like idle1, idle2, die1 etc.)
- Added a simple button to quickly keyframe rotations, perfect for standing frames and turrets.
![rotate_directions](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/d2c429ab-38e5-4557-8e2d-f1722de9f4b7)
![quick rotate](https://github.com/HollandTS/cnc_anim_addon/assets/65047646/3ad9bd1f-61ae-4a5d-9e14-4569b260a475)

