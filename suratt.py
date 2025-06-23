import pygame
import math
import random
import sys
import textwrap

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
LIGHT_PINK = (255, 220, 230)
DARK_PINK = (255, 105, 180)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
PARCHMENT = (255, 248, 220)


class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(1, 3)
        self.size = random.randint(8, 15)
        self.alpha = 255

    def update(self):
        self.y -= self.speed
        self.alpha -= 2
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, screen):
        if self.alpha > 0:
            heart_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color = (*RED[:3], self.alpha)
            # Simple heart shape using circles
            pygame.draw.circle(heart_surface, color, (self.size // 2, self.size // 2), self.size // 3)
            pygame.draw.circle(heart_surface, color, (self.size + self.size // 2, self.size // 2), self.size // 3)
            pygame.draw.polygon(heart_surface, color, [(self.size // 4, self.size // 2),
                                                       (self.size * 1.75, self.size // 2),
                                                       (self.size, self.size * 1.5)])
            screen.blit(heart_surface, (self.x - self.size, self.y - self.size))


class AnimatedLoveLetter:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Surat Cinta untuk Nabila Khansa 💕")
        self.clock = pygame.time.Clock()

        # Fonts
        self.font_large = pygame.font.Font(None, 60)
        self.font_medium = pygame.font.Font(None, 20)

        # Try to load Times New Roman, fallback to default
        try:
            self.font_letter = pygame.font.SysFont('timesnewroman', 10)
        except:
            self.font_letter = pygame.font.Font(None, 10)

        # Game state
        self.state = "start"  # "start" or "letter"

        # Animation variables
        self.pulse_timer = 0
        self.hearts = []
        self.current_char = 0
        self.typing_speed = 0.5
        self.typing_timer = 0

        # Letter content
        self.letter_text = """Haiidedeee,

mungkinn suratt inii ga akann ngubah apapun, gaa akan nyembuhin lukaa dan gaa akann ngilangin rasa sakitt yangg udahh pernahh apii kasih, 
apii jugaa ga ngetikk inii buat mintaa dimaafinn, apii nuliss inii karenaa sadarr, apii udahh nyakitinn seseorangg yangg seharusnyaa apii jagaa.
dedee ituu wanitaa palingg tuluss yangg pernahh adaa dalam hidup apii, dedee ituu sabarr, lembutt, jugaa kuatt, dan sayangg nyaa gaa pernahh setengahh setengahh,
dan yang paling bikinn apii kesel samaa diri apii sendiri karnaa ituu semuaa apii sendirii yang ngerusakk.
apii gatauu apakahh dedee masihh nyimpen perasaan yang samaa atauu enggaa, kaloo pun iyaa, apii yakinn rasa sakitt dan lukaa yang dedee alamin jauhh lebih besarr daripadaa perasaan ituu,
apii pahamm, perasaan ituu gaa bisaa dipaksaa sepertii duluu.
tapii apii pengenn berubahh, bukann buat dramaa, bukan karenaa kehilangan, 
tapii karnaa apii sadar dedee ituu satuu satuunyaa orangg yang bikinn apii ngerasaa berartii, apii pengen jadi versi terbaik dari diri apii.
dedeee ituu luarr biasaa, dedee ituu benerr benerr wanitaa yangg kuatt, apii banggaa punyaa wanitaaa sepertii dedee, 
palingg layakk disayangii sepenuhhnyaaa, apii akann teruss mencintaii dedee walauu harus dari nol, 
suatuu harii entahh ituu besokk, lusaa, minggu depan, atau mungkin tahun depan, atau kapanpun ituu ketikaa dedee ngeliatt apii, apii pengenn nunjukinn ke dedee, dan ngebuat dedee berkataa "dia berubah dan beneran berubah jadi yang lebihh baikk"
karnaa kapanpun ituu perasaan apii tetep samaa, apii sayangg dedee, apii akan selaluu mencintaii kamuu sayangg.

karnaa kamuu layakk buatt dicintaiii, apii mintaa maafff.
wopyouuu moreee moreee and foreverr.

- apii ❤️"""

        # Process text for display
        self.wrapped_lines = []
        self.displayed_text = ""
        self.wrap_text()

    def wrap_text(self):
        """Wrap text to fit in the letter area"""
        # Split into paragraphs
        paragraphs = self.letter_text.split('\n\n')

        # Available width for text (letter width minus margins)
        max_width = 100  # characters per line

        for paragraph in paragraphs:
            if paragraph.strip():
                # Wrap each paragraph
                wrapped = textwrap.fill(paragraph.strip(), width=max_width)
                self.wrapped_lines.extend(wrapped.split('\n'))
            self.wrapped_lines.append("")  # Empty line between paragraphs

        # Remove trailing empty lines
        while self.wrapped_lines and not self.wrapped_lines[-1]:
            self.wrapped_lines.pop()

    def draw_start_screen(self):
        """Draw the start screen with LOVE button"""
        self.screen.fill(WHITE)

        # Pulsing effect for LOVE text
        self.pulse_timer += 0.1
        pulse_scale = 1 + 0.15 * math.sin(self.pulse_timer)

        # Draw LOVE text
        love_text = self.font_large.render("LOVE", True, RED)
        love_rect = love_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

        # Scale the text
        scaled_love = pygame.transform.scale(love_text,
                                             (int(love_rect.width * pulse_scale),
                                              int(love_rect.height * pulse_scale)))
        scaled_rect = scaled_love.get_rect(center=love_rect.center)

        self.screen.blit(scaled_love, scaled_rect)

        # Draw instruction
        instruction = self.font_medium.render("Klik LOVE untuk membuka surat! 💕", True, BLACK)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(instruction, instruction_rect)

        # Add floating hearts
        if random.random() < 0.08:
            self.hearts.append(Heart(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT))

        # Update and draw hearts
        for heart in self.hearts[:]:
            heart.update()
            heart.draw(self.screen)
            if heart.alpha <= 0:
                self.hearts.remove(heart)

        return scaled_rect

    def draw_letter_screen(self):
        """Draw the letter with pink background and parchment"""
        # Pink gradient background
        for y in range(SCREEN_HEIGHT):
            intensity = int(255 - (y / SCREEN_HEIGHT) * 60)
            color = (255, intensity, intensity)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))

        # Letter dimensions
        letter_width = 680
        letter_height = 520
        letter_x = (SCREEN_WIDTH - letter_width) // 2
        letter_y = (SCREEN_HEIGHT - letter_height) // 2

        # Draw parchment background
        parchment_rect = pygame.Rect(letter_x, letter_y, letter_width, letter_height)
        pygame.draw.rect(self.screen, PARCHMENT, parchment_rect)
        pygame.draw.rect(self.screen, GOLD, parchment_rect, 4)

        # Draw decorative border
        inner_rect = pygame.Rect(letter_x + 20, letter_y + 20, letter_width - 40, letter_height - 40)
        pygame.draw.rect(self.screen, GOLD, inner_rect, 2)

        # Typing animation
        self.typing_timer += 0.5
        if self.typing_timer >= self.typing_speed:
            self.typing_timer = 0
            if self.current_char < len(self.letter_text):
                self.displayed_text += self.letter_text[self.current_char]
                self.current_char += 1

        # Draw text
        self.draw_justified_text(letter_x + 40, letter_y + 40, letter_width - 80, letter_height - 80)

        # Add floating hearts
        if random.random() < 0.03:
            self.hearts.append(Heart(
                random.randint(letter_x, letter_x + letter_width),
                random.randint(letter_y, letter_y + letter_height)
            ))

        # Update and draw hearts
        for heart in self.hearts[:]:
            heart.update()
            heart.draw(self.screen)
            if heart.alpha <= 0:
                self.hearts.remove(heart)

    def draw_justified_text(self, x, y, width, height):
        """Draw justified text in the letter area"""
        # Split displayed text into paragraphs
        paragraphs = self.displayed_text.split('\n\n')

        current_y = y
        line_height = 20

        for paragraph in paragraphs:
            if paragraph.strip():
                # Wrap paragraph to fit width
                words = paragraph.strip().split()
                lines = []
                current_line = []

                for word in words:
                    # Test if adding word exceeds width
                    test_line = ' '.join(current_line + [word])
                    text_width = self.font_letter.size(test_line)[0]

                    if text_width <= width - 20:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(current_line)
                            current_line = [word]
                        else:
                            lines.append([word])

                if current_line:
                    lines.append(current_line)

                # Draw lines with justification
                for i, line_words in enumerate(lines):
                    if current_y > y + height - line_height:
                        break  # Stop if we exceed the letter area

                    if len(line_words) == 1:
                        # Single word - center align
                        if line_words[0].startswith('-'):  # Signature
                            text = ' '.join(line_words)
                            text_surface = self.font_letter.render(text, True, BLACK)
                            text_x = x + (width - text_surface.get_width()) // 2
                            self.screen.blit(text_surface, (text_x, current_y))
                        else:
                            # Regular single word - left align
                            text_surface = self.font_letter.render(line_words[0], True, BLACK)
                            self.screen.blit(text_surface, (x, current_y))
                    else:
                        # Multiple words - justify
                        total_text_width = sum(self.font_letter.size(word)[0] for word in line_words)
                        total_spaces = len(line_words) - 1

                        if total_spaces > 0:
                            space_width = (width - 20 - total_text_width) // total_spaces
                            current_x = x

                            for j, word in enumerate(line_words):
                                word_surface = self.font_letter.render(word, True, BLACK)
                                self.screen.blit(word_surface, (current_x, current_y))
                                current_x += word_surface.get_width()

                                if j < len(line_words) - 1:  # Not the last word
                                    current_x += space_width + self.font_letter.size(' ')[0]
                        else:
                            # Fallback to left align
                            text = ' '.join(line_words)
                            text_surface = self.font_letter.render(text, True, BLACK)
                            self.screen.blit(text_surface, (x, current_y))

                    current_y += line_height

            # Add space between paragraphs
            current_y += line_height // 2

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "start":
                    # Check if clicked on LOVE
                    mouse_pos = pygame.mouse.get_pos()
                    love_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                    distance = math.sqrt((mouse_pos[0] - love_center[0]) ** 2 +
                                         (mouse_pos[1] - love_center[1]) ** 2)

                    if distance < 100:  # Click area around LOVE
                        self.state = "letter"
                        self.hearts.clear()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE and self.state == "letter":
                    # Reset to start
                    self.state = "start"
                    self.current_char = 0
                    self.displayed_text = ""
                    self.hearts.clear()

        return True

    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()

            if self.state == "start":
                self.draw_start_screen()
            else:
                self.draw_letter_screen()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = AnimatedLoveLetter()
    game.run()