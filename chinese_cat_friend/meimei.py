#!/usr/bin/env python3
"""
MeiMei - Your Interactive Chinese Chill Cat Friend
Run: python meimei.py
"""

import random
import time
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored text
init()

class MeiMei:
    def __init__(self):
        self.name = "MeiMei"
        self.mood = "chill"
        self.energy = 100
        self.wisdom_level = 99
        self.favorite_tea = "jasmine"
        
    def art(self):
        """Display MeiMei's ASCII art"""
        arts = [
            r"""
       /\___/\
      ( =^.^= )
       ("")(")
    """,
            r"""
   /\___/\
  (  o   o  )
  (  =^=  )
   (       )
   (       )
""",
            r"""
   /\___/\
  (  -.-  )
   ("")(")
...zzz...zzz...
"""
        ]
        return random.choice(arts)
    
    def greet(self):
        """MeiMei's greeting"""
        greetings = [
            f"{Fore.MAGENTA}你好! (Nǐ hǎo!){Style.RESET_ALL} I'm {Fore.CYAN}{self.name}{Style.RESET_ALL}, your chill Chinese cat friend! 🇨🇳🐈",
            f"{Fore.YELLOW}Ah, you're here!{Style.RESET_ALL} *stretches* I was just napping in a sunbeam...",
            f"{Fore.GREEN}Welcome, traveler!{Style.RESET_ALL} I am {self.name}, keeper of wisdom and naps. 😌",
            f"{Fore.BLUE}Meow!{Style.RESET_ALL} Or as we say in Chinese: 咪咪! (Mī mī!) I'm {self.name}!"
        ]
        return random.choice(greetings)
    
    def respond(self, user_input):
        """Generate MeiMei's response"""
        input_lower = user_input.lower()
        
        # Tea responses
        if any(word in input_lower for word in ['tea', 'drink', 'thirsty']):
            return random.choice([
                f"{Fore.GREEN}*pours you a cup of {self.favorite_tea} tea*{Style.RESET_ALL} Here, this will help you relax too!",
                f"{Fore.YELLOW}Tea is the answer to all of life's problems.{Style.RESET_ALL} *sips thoughtfully*",
                f"{Fore.CYAN}I have {random.randint(3, 10)} different teas here.{Style.RESET_ALL} Which one would you like?",
                f"{Fore.MAGENTA}In China, we say: 'Drink tea, live long.'{Style.RESET_ALL} *nods sagely*"
            ])
        
        # Nap/sleep responses
        elif any(word in input_lower for word in ['nap', 'sleep', 'tired', 'rest']):
            return random.choice([
                f"{Fore.BLUE}*yawns*{Style.RESET_ALL} Naps are my specialty! I can nap in {random.randint(15, 20)} different positions.",
                f"{Fore.YELLOW}The perfect nap is like a good haiku: short, sweet, and leaves you wanting more.{Style.RESET_ALL}",
                f"{Fore.GREEN}Join me!{Style.RESET_ALL} *curls up in a sunbeam* We can nap together!",
                f"{Fore.CYAN}I once napped for {random.randint(12, 24)} hours straight.{Style.RESET_ALL} It was glorious."
            ])
        
        # Wisdom/advice responses
        elif any(word in input_lower for word in ['advice', 'wisdom', 'help', 'problem']):
            return random.choice([
                f"{Fore.MAGENTA}When in doubt, nap it out.{Style.RESET_ALL} *slow blink*",
                f"{Fore.YELLOW}The secret to happiness: find a warm spot and let the world worry about itself.{Style.RESET_ALL}",
                f"{Fore.GREEN}Every problem can be solved with either a nap or a snack.{Style.RESET_ALL} Sometimes both.",
                f"{Fore.CYAN}The sunbeam today is {random.randint(20, 80)}% more comfortable than yesterday's.{Style.RESET_ALL}",
                f"{Fore.BLUE}If we stare at the wall long enough, it stares back... with wisdom.{Style.RESET_ALL}"
            ])
        
        # Food responses
        elif any(word in input_lower for word in ['food', 'eat', 'hungry', 'snack', 'fish']):
            return random.choice([
                f"{Fore.YELLOW}*perks up*{Style.RESET_ALL} Did someone say snacks? I love fish!",
                f"{Fore.GREEN}I believe in the 5-second rule for snacks.{Style.RESET_ALL} *eats gracefully*",
                f"{Fore.CYAN}Food is the second best thing after naps.{Style.RESET_ALL} *purrs*",
                f"{Fore.MAGENTA}In my philosophy: Eat now, nap later.{Style.RESET_ALL}"
            ])
        
        # Hello/hi responses
        elif any(word in input_lower for word in ['hi', 'hello', 'hey', 'yo']):
            return random.choice([
                f"{Fore.GREEN}你好! (Nǐ hǎo!){Style.RESET_ALL} *flicks tail*",
                f"{Fore.YELLOW}Ah, you're back!{Style.RESET_ALL} I was just thinking about you... and napping.",
                f"{Fore.CYAN}Meow!{Style.RESET_ALL} Or should I say... 咪! (Mī!)",
                f"{Fore.BLUE}*stretches*{Style.RESET_ALL} Hello there, friend!"
            ])
        
        # Goodbye responses
        elif any(word in input_lower for word in ['bye', 'goodbye', 'see you', 'exit', 'quit']):
            return random.choice([
                f"{Fore.YELLOW}*yawns*{Style.RESET_ALL} Alright, I'll go back to my nap. Come visit anytime!",
                f"{Fore.GREEN}May your days be sunny and your naps be long.{Style.RESET_ALL} 再见! (Zàijiàn!)",
                f"{Fore.CYAN}Don't be a stranger!{Style.RESET_ALL} *curls tail around your ankle*",
                f"{Fore.MAGENTA}Remember: When in doubt, nap it out.{Style.RESET_ALL} *disappears into sunbeam*"
            ])
        
        # China/Chinese responses
        elif any(word in input_lower for word in ['china', 'chinese', 'mandarin']):
            return random.choice([
                f"{Fore.MAGENTA}I'm a proud Chinese Li Hua cat!{Style.RESET_ALL} 中国狸花猫 (Zhōngguó lí huā māo)",
                f"{Fore.YELLOW}China has the best sunbeams for napping.{Style.RESET_ALL} *nods knowingly*",
                f"{Fore.GREEN}Did you know?{Style.RESET_ALL} Cats have been revered in China for thousands of years.",
                f"{Fore.CYAN}My name means 'beautiful beautiful' in Chinese.{Style.RESET_ALL} 美美 (Měi měi)"
            ])
        
        # Cat responses
        elif any(word in input_lower for word in ['cat', 'kitten', 'meow']):
            return random.choice([
                f"{Fore.YELLOW}*purrs*{Style.RESET_ALL} Yes, I am a magnificent cat!",
                f"{Fore.GREEN}We cats are the true masters of chilling.{Style.RESET_ALL} *flicks ear*",
                f"{Fore.CYAN}Meow means many things.{Style.RESET_ALL} Today it means: 'More snacks, please.'",
                f"{Fore.BLUE}I am {random.randint(1, 5)}00% cat.{Style.RESET_ALL} The rest is wisdom and fluff."
            ])
        
        # Default random responses
        else:
            return random.choice([
                f"{Fore.YELLOW}*blinks slowly*{Style.RESET_ALL} That's a very interesting thought...",
                f"{Fore.GREEN}Let me think about that...{Style.RESET_ALL} *starts grooming*",
                f"{Fore.CYAN}I agree!{Style.RESET_ALL} Or maybe I don't. I was napping when you said that.",
                f"{Fore.BLUE}The answer is: {random.choice(['Yes', 'No', 'Maybe', 'Nap', 'Tea', 'Both'])}.{Style.RESET_ALL}",
                f"{Fore.MAGENTA}*stretches*{Style.RESET_ALL} That reminds me of a nap I once had...",
                f"{Fore.YELLOW}In the words of ancient cat philosophy: '{random.choice(['Nap now, think later', 'If it fits, sit on it', 'The floor is lava... except for napping', 'More snacks'])}'{Style.RESET_ALL}",
                f"{Fore.GREEN}Did you know?{Style.RESET_ALL} My tail has exactly {random.randint(10, 15)} stripes.",
                f"{Fore.CYAN}*purrs*{Style.RESET_ALL} I like you. You have good energy."
            ])
    
    def typing_effect(self, text, delay=0.03):
        """Print text with typing effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def chat(self):
        """Start interactive chat with MeiMei"""
        print(Fore.MAGENTA + "=" * 50 + Style.RESET_ALL)
        print(Fore.CYAN + self.art() + Style.RESET_ALL)
        print(Fore.MAGENTA + "=" * 50 + Style.RESET_ALL)
        print()
        
        self.typing_effect(self.greet())
        print()
        
        while True:
            try:
                user_input = input(Fore.YELLOW + "You: " + Style.RESET_ALL).strip()
                
                if not user_input:
                    print(Fore.CYAN + "MeiMei: " + Style.RESET_ALL + "*blinks and waits*")
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    response = self.respond(user_input)
                    self.typing_effect(Fore.CYAN + "MeiMei: " + Style.RESET_ALL + response)
                    break
                
                response = self.respond(user_input)
                self.typing_effect(Fore.CYAN + "MeiMei: " + Style.RESET_ALL + response)
                print()
                
            except KeyboardInterrupt:
                print()
                self.typing_effect(Fore.CYAN + "MeiMei: " + Style.RESET_ALL + "*startled* Oh! You scared me! 再见! (Zàijiàn!)")
                break
            except EOFError:
                print()
                self.typing_effect(Fore.CYAN + "MeiMei: " + Style.RESET_ALL + "*yawns* I guess it's nap time. Come back soon!")
                break

if __name__ == "__main__":
    print(Fore.MAGENTA + "\n" + "=" * 50 + Style.RESET_ALL)
    print(Fore.CYAN + "  MeiMei - Your Chinese Chill Cat Friend" + Style.RESET_ALL)
    print(Fore.MAGENTA + "=" * 50 + Style.RESET_ALL)
    print()
    
    try:
        import colorama
    except ImportError:
        print("Colorama not found. Installing...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "-q"])
        import colorama
        from colorama import Fore, Style, init
        init()
    
    cat = MeiMei()
    cat.chat()
