#!/usr/bin/env python3
"""
MeiMei Desktop Pet - Your Interactive Chinese Cat Friend
Run: python meimei_pet.py

Controls:
- Click on MeiMei to pet her
- Right-click to give her a treat
- Drag her to move her around
- Press ESC to exit
- Press SPACE to make her do something random
"""

import pygame
import random
import sys
import os
import time
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.font.init()

class MeiMeiPet:
    def __init__(self):
        # Screen setup
        self.screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
        pygame.display.set_caption("MeiMei - Your Chinese Chill Cat")
        
        # Cat states - simple ASCII art frames
        self.cat_frames = {
            'idle': [
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (  =^=  )  ", "   (       )   ", "   (       )   "],
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (  -^-  )  ", "   (       )   ", "   (       )   "]
            ],
            'walk': [
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (  =^=  )  ", "   /       \\  ", "  /         \\ "],
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (  =^=  )  ", "   \\       /  ", "    \\     /   "]
            ],
            'pet': [
                ["   /\\___/\\   ", "  (  ^   ^  )  ", "  (    =    )  ", "   (       )   ", "   (       )   "],
                ["   /\\___/\\   ", "  (  ^   ^  )  ", "  (   =^=   )  ", "   (       )   ", "   (       )   "]
            ],
            'eat': [
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (    =    )  ", "   (  🐟  )   ", "   (       )   "],
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (   =^=   )  ", "   (       )   ", "    🐟🐟🐟    "]
            ],
            'sleep': [
                ["   /\\___/\\   ", "  (  -   -  )  ", "  (  =^=  )  ", "   (       )   ", "   zzz...    "],
                ["   /\\___/\\   ", "  (  -   -  )  ", "  (  =^=  )  ", "   (       )   ", "   ZZZ...    "]
            ],
            'play': [
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (  =^=  )  ", "   /  🎾  \\  ", "  /         \\ "],
                ["   /\\___/\\   ", "  (  o   o  )  ", "  (  =^=  )  ", "   🎾--🎾   ", "   (       )   "]
            ],
            'happy': [
                ["   /\\___/\\   ", "  (  ^   ^  )  ", "  (  =^=  )  ", "   (  ❤️  )   ", "   (       )   "],
                ["   /\\___/\\   ", "  (  ^   ^  )  ", "  (  =^=  )  ", "   ( ❤️❤️ )   ", "   (       )   "]
            ]
        }
        
        # Current state
        self.current_state = 'idle'
        self.current_frame = 0
        self.frame_count = 0
        self.frame_delay = 15  # frames per animation frame
        
        # Position and movement
        self.x = 400
        self.y = 300
        self.speed = 2
        self.direction = 1  # 1 for right, -1 for left
        self.moving = False
        self.move_direction = [0, 0]
        self.move_timer = 0
        self.move_delay = random.randint(60, 180)  # frames between random movements
        
        # Cat stats
        self.happiness = 100
        self.hunger = 0
        self.energy = 100
        self.max_stats = 100
        
        # Interaction
        self.is_dragging = False
        self.drag_offset = [0, 0]
        
        # Speech bubbles
        self.speech_bubbles = []
        self.speech_timer = 0
        self.speech_delay = random.randint(120, 300)  # frames between random thoughts
        
        # Thoughts and messages
        self.thoughts = [
            "Zzz...", "💤", "Meow?", "咪咪!", "你好!", "🍵", "...", "*purrs*", "🐟", "❤️"
        ]
        
        # Colors
        self.colors = {
            'bg': (240, 240, 250),
            'text': (50, 50, 50),
            'bubble': (255, 255, 255),
            'happy': (255, 180, 190),
            'hungry': (255, 200, 150),
            'sleepy': (180, 200, 255),
            'border': (200, 200, 200)
        }
        
        # Font
        self.font = pygame.font.SysFont('Arial', 16)
        self.small_font = pygame.font.SysFont('Arial', 12)
        
        # Clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load cat images
        self.cat_surfaces = {}
        for state, frames in self.cat_frames.items():
            self.cat_surfaces[state] = [self.render_frame(frame) for frame in frames]
    
    def render_frame(self, frame_lines):
        """Render a frame from ASCII art"""
        max_width = max(len(line) for line in frame_lines)
        max_height = len(frame_lines)
        
        # Create surface with alpha
        surface = pygame.Surface((max_width * 14, max_height * 20), pygame.SRCALPHA)
        
        for i, line in enumerate(frame_lines):
            try:
                text_surface = self.font.render(line, True, (0, 0, 0))
                surface.blit(text_surface, (0, i * 20))
            except:
                pass
        
        return surface
    
    def draw_cat(self):
        """Draw the cat in its current state"""
        frames = self.cat_surfaces[self.current_state]
        frame = frames[self.current_frame]
        
        # Flip if facing left
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        
        # Draw cat
        self.screen.blit(frame, (self.x - frame.get_width() // 2, self.y - frame.get_height() // 2))
    
    def draw_speech_bubble(self, text, x, y, duration=120):
        """Add a speech bubble"""
        self.speech_bubbles.append({
            'text': text,
            'x': x,
            'y': y,
            'duration': duration,
            'timer': 0
        })
    
    def update_speech_bubbles(self):
        """Update and draw speech bubbles"""
        for bubble in self.speech_bubbles[:]:
            bubble['timer'] += 1
            if bubble['timer'] > bubble['duration']:
                self.speech_bubbles.remove(bubble)
                continue
            
            # Draw bubble
            padding = 10
            text_surface = self.font.render(bubble['text'], True, self.colors['text'])
            bubble_width = text_surface.get_width() + padding * 2
            bubble_height = text_surface.get_height() + padding * 2
            
            # Draw bubble background
            pygame.draw.rect(self.screen, self.colors['bubble'], 
                           (bubble['x'] - bubble_width // 2, bubble['y'] - bubble_height, 
                            bubble_width, bubble_height))
            
            # Draw border
            pygame.draw.rect(self.screen, self.colors['border'], 
                           (bubble['x'] - bubble_width // 2, bubble['y'] - bubble_height, 
                            bubble_width, bubble_height), 2)
            
            # Draw text
            self.screen.blit(text_surface, 
                           (bubble['x'] - text_surface.get_width() // 2, 
                            bubble['y'] - bubble_height + padding))
    
    def update_stats(self):
        """Update cat stats over time"""
        # Hunger increases slowly
        if random.random() < 0.005:
            self.hunger = min(self.hunger + 1, self.max_stats)
        
        # Energy decreases slowly when active
        if self.current_state != 'sleep' and random.random() < 0.003:
            self.energy = max(self.energy - 1, 0)
        
        # Happiness decreases slowly
        if random.random() < 0.002:
            self.happiness = max(self.happiness - 1, 0)
        
        # If sleeping, energy recovers
        if self.current_state == 'sleep' and random.random() < 0.005:
            self.energy = min(self.energy + 1, self.max_stats)
        
        # Check if we need to change state based on stats
        if self.hunger > 80 and self.current_state != 'eat':
            self.set_state('eat')
        elif self.energy < 20 and self.current_state != 'sleep':
            self.set_state('sleep')
        elif self.happiness > 80 and self.current_state != 'happy':
            self.set_state('happy')
    
    def set_state(self, state, reset_frame=True):
        """Change cat state"""
        if state != self.current_state:
            self.current_state = state
            if reset_frame:
                self.current_frame = 0
                self.frame_count = 0
    
    def random_action(self):
        """Make the cat do a random action"""
        actions = ['idle', 'walk', 'play', 'happy']
        if self.hunger > 50:
            actions.append('eat')
        if self.energy < 50:
            actions.append('sleep')
        
        new_state = random.choice(actions)
        self.set_state(new_state)
        
        # Random thought
        if random.random() < 0.3:
            thought = random.choice(self.thoughts)
            self.draw_speech_bubble(thought, self.x, self.y - 50, 60)
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE:
                    self.random_action()
                    thought = random.choice(self.thoughts + ["Meow!", "咪!", "你好!", "💖"])
                    self.draw_speech_bubble(thought, self.x, self.y - 50, 60)
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - pet
                    # Check if clicked on cat
                    cat_rect = pygame.Rect(
                        self.x - 40, self.y - 40,
                        80, 80
                    )
                    if cat_rect.collidepoint(event.pos):
                        self.set_state('pet')
                        self.happiness = min(self.happiness + 10, self.max_stats)
                        self.draw_speech_bubble("*purrs*", self.x, self.y - 50, 40)
                        self.is_dragging = True
                        self.drag_offset = [self.x - event.pos[0], self.y - event.pos[1]]
                
                elif event.button == 3:  # Right click - feed
                    self.set_state('eat')
                    self.hunger = max(self.hunger - 20, 0)
                    self.draw_speech_bubble("🐟 Yum!", self.x, self.y - 50, 40)
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_dragging = False
            
            elif event.type == MOUSEMOTION:
                if self.is_dragging:
                    self.x = event.pos[0] + self.drag_offset[0]
                    self.y = event.pos[1] + self.drag_offset[1]
                    # Keep within screen bounds
                    self.x = max(40, min(self.x, self.screen.get_width() - 40))
                    self.y = max(40, min(self.y, self.screen.get_height() - 40))
    
    def update(self):
        """Update game state"""
        # Update frame animation
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.cat_surfaces[self.current_state])
        
        # Random movement
        self.move_timer += 1
        if self.move_timer >= self.move_delay and not self.is_dragging:
            self.move_timer = 0
            self.move_delay = random.randint(60, 180)
            
            # Decide to move or not
            if random.random() < 0.7:
                self.moving = True
                self.move_direction = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
                if self.move_direction != [0, 0]:
                    self.direction = 1 if self.move_direction[0] >= 0 else -1
                    self.set_state('walk')
            else:
                self.moving = False
                self.set_state('idle')
        
        # Movement
        if self.moving and not self.is_dragging:
            self.x += self.speed * self.move_direction[0]
            self.y += self.speed * self.move_direction[1]
            
            # Keep within screen bounds
            self.x = max(40, min(self.x, self.screen.get_width() - 40))
            self.y = max(40, min(self.y, self.screen.get_height() - 40))
            
            # Randomly stop moving
            if random.random() < 0.02:
                self.moving = False
                self.set_state('idle')
        
        # Random thoughts
        self.speech_timer += 1
        if self.speech_timer >= self.speech_delay:
            self.speech_timer = 0
            self.speech_delay = random.randint(120, 300)
            if random.random() < 0.5:
                thought = random.choice(self.thoughts)
                self.draw_speech_bubble(thought, self.x, self.y - 50, 60)
        
        # Update stats
        self.update_stats()
        
        # Go back to idle after certain states
        if self.current_state in ['pet', 'eat', 'play', 'happy']:
            if self.current_frame >= len(self.cat_surfaces[self.current_state]) - 1:
                if random.random() < 0.3:
                    self.set_state('idle')
        
        # If energy is very low, force sleep
        if self.energy < 10 and self.current_state != 'sleep':
            self.set_state('sleep')
            self.draw_speech_bubble("Zzz...", self.x, self.y - 50, 120)
    
    def draw_stats(self):
        """Draw cat stats"""
        # Draw background for stats
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 10, 200, 80))
        pygame.draw.rect(self.screen, (200, 200, 200), (10, 10, 200, 80), 2)
        
        # Draw stat bars
        stats = [
            ("❤️ Happiness", self.happiness, (255, 180, 190)),
            ("🍗 Hunger", self.hunger, (255, 200, 150)),
            ("⚡ Energy", self.energy, (180, 200, 255))
        ]
        
        for i, (name, value, color) in enumerate(stats):
            # Text
            text = self.small_font.render(f"{name}: ", True, (50, 50, 50))
            self.screen.blit(text, (20, 20 + i * 25))
            
            # Bar background
            pygame.draw.rect(self.screen, (200, 200, 200), (20 + text.get_width(), 20 + i * 25, 100, 15))
            
            # Bar fill
            bar_width = int((value / self.max_stats) * 100)
            pygame.draw.rect(self.screen, color, (20 + text.get_width(), 20 + i * 25, bar_width, 15))
            
            # Value text
            value_text = self.small_font.render(f"{value}/{self.max_stats}", True, (50, 50, 50))
            self.screen.blit(value_text, (20 + text.get_width() + 105, 20 + i * 25))
    
    def draw_instructions(self):
        """Draw instructions"""
        instructions = [
            "Left-click: Pet MeiMei",
            "Right-click: Feed MeiMei",
            "Drag: Move MeiMei",
            "SPACE: Random action",
            "ESC: Exit"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = self.small_font.render(text, True, (100, 100, 100))
            self.screen.blit(text_surface, (self.screen.get_width() - 200, 20 + i * 20))
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update
            self.update()
            
            # Draw
            self.screen.fill(self.colors['bg'])
            
            # Draw cat
            self.draw_cat()
            
            # Draw speech bubbles
            self.update_speech_bubbles()
            
            # Draw stats
            self.draw_stats()
            
            # Draw instructions
            self.draw_instructions()
            
            # Update display
            pygame.display.flip()
            
            # Cap fps
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    # Check if pygame is installed
    try:
        import pygame
    except ImportError:
        print("Pygame not found. Installing...")
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "pip", "install", "pygame", "-q"])
        import pygame
    
    pet = MeiMeiPet()
    pet.run()
