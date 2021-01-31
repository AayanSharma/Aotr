import pygame
import math

class AnimationManager():
    """
    An AnimationManager stores all the Animations needed for one fighter.
    However, all of these variables are set to None. You'll need to make
    a new class that inherits AnimationManager for each fighter in your game.
    """
    def __init__(self):
        self.icon = None
        
        self.idle_anim = None
        self.run_anim = None
        self.midair_anim = None
        self.jump_anim = None
        self.attack1_anim = None
        self.attack2_anim = None
        self.attack3_anim = None
        
        self.current_anim = None

    def ChangeState(self, state):
        self.current_anim.reset()
        self.current_anim = getattr(self, state + "_anim")

    def getImage(self, flipped=False):
        next_anim = self.current_anim.changeAnim()
        if next_anim:
            self.ChangeState(next_anim)
        return self.current_anim.getImage(flipped)

    def getRect(self, flipped, midbottom):
        if flipped:
            x = midbottom[0] - self.current_anim.offset[0]
        else:
            x = midbottom[0] + self.current_anim.offset[0]
        y = midbottom[1] + self.current_anim.offset[1]
        return self.current_anim.currentImage().get_rect(midbottom=(x,y)) 


class ExampleAnimationManager(AnimationManager):
    """
    This is an example of a fully set up AnimationManager!
    """
    def __init__(self):
        AnimationManager.__init__(self)

        # Icon image
        self.icon = pygame.image.load("../assets/Demo/Demo_icon.png")

        # Idle animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_idle_1.png"),
                        pygame.image.load("../assets/Demo/Demo_idle_2.png"),
                        pygame.image.load("../assets/Demo/Demo_idle_3.png"), ]
        self.idle_anim = Animation(anim_frames, 8)

        # Run animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_run_1.png"),
                        pygame.image.load("../assets/Demo/Demo_run_2.png"), ]
        self.run_anim = Animation(anim_frames, 6)

        # Mid-air animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_jump_3.png"), ]
        self.midair_anim = Animation(anim_frames, 2)
        
        # Jump animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_jump_1.png"),
                        pygame.image.load("../assets/Demo/Demo_jump_2.png"), ]
        self.jump_anim = Animation(anim_frames, 2, next_anim="midair")

        # Attack 1 animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_highAttack_1.png"),
                        pygame.image.load("../assets/Demo/Demo_highAttack_2.png"), ]
        self.attack1_anim = Animation(anim_frames, 6, next_anim="idle")

        # Attack 2 animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_midAttack_1.png"),
                        pygame.image.load("../assets/Demo/Demo_midAttack_2.png"),
                        pygame.image.load("../assets/Demo/Demo_midAttack_3.png"), ]
        self.attack2_anim = Animation(anim_frames, 3, next_anim="idle")

        # Attack 3 animation
        anim_frames = [ pygame.image.load("../assets/Demo/Demo_lowAttack_1.png"), ]
        self.attack3_anim = Animation(anim_frames, 6, next_anim="idle")

        # Starting animation
        self.current_anim = self.idle_anim




#######################
### Animation class ###
#######################

class Animation():
    """
    An Animation stores the images needed for one animation.
    If next_anim is None, the animation will loop forever.
    Otherwise, the animation will play once and then switch to the next animation.
    (Don't mess with my Animation code unless you know what you're doing!  -Andy)
    """
    def __init__(self, anim_images, anim_speed, offset=(0,0), next_anim=None):
        self.anim_images = anim_images
        self.anim_speed = anim_speed
        self.offset = offset
        self.next_anim = next_anim
        self.frame_timer = 0
        self.frame_on = 0
        self.finished = False

        # Generate flipped versions of all images
        self.anim_images_flip = []
        for image in self.anim_images:
            flipped_image = pygame.transform.flip(image, True, False)
            self.anim_images_flip.append(flipped_image)

    def getImage(self, flipped=False):
        """
        getImage should be called exactly once every frame. This will return the image
        that should be showing on that frame.
        """
        if flipped:
            image_to_return = self.anim_images_flip[self.frame_on]
        else:
            image_to_return = self.anim_images[self.frame_on]

        self.frame_timer += 1
        if self.frame_timer >= self.anim_speed:
            self.frame_timer = 0
            self.frame_on += 1
            
        if self.frame_on >= len(self.anim_images):
            if self.next_anim:
                self.finished = True
            self.frame_on = 0

        return image_to_return

    def currentImage(self, flipped=False):
        """
        This is basically the same as getImage, but it doesn't increase the timer.
        """
        if flipped:
            return self.anim_images_flip[self.frame_on]
        else:
            return self.anim_images[self.frame_on]

    def changeAnim(self):
        """
        Returns None if this animation doesn't want to change yet,
        or next_anim if it is finished.
        """
        if self.finished:
            return self.next_anim
        else:
            return None

    def reset(self):
        """
        Reset should be called whenever a different animation starts
        (or to make this animation start over from the beginning).
        """
        self.frame_timer = 0
        self.frame_on = 0
        self.finished = False
