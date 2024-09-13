import sys
import pygame
import config


# depending on the winner, a new screen is displayed
def victory():
    font = pygame.font.Font(None, config.TYPEFACE)
    if config.WINNER == 'Human':
        victory_window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Victory!')

        victory_image = pygame.image.load(config.victory_human_image_const)
        victory_image = pygame.transform.scale(victory_image, (800, 600))

        victory_window.blit(victory_image, (0, 0))

        close_button = pygame.Rect(350, 550, 100, 50)
        pygame.draw.rect(victory_window, (0, 0, 0), close_button)  
        close_button_text = font.render('Close', True, (255, 255, 255))  
        text_rect = close_button_text.get_rect(center=close_button.center)  
        victory_window.blit(close_button_text, text_rect)

        font = pygame.font.Font(None, 66)
        font.set_bold(True)
        font.set_italic(True) 
        victory_message = font.render('Human win!', True, (255, 0, 0))
        text_rect = victory_message.get_rect(center=(400, 70))  
        victory_window.blit(victory_message, text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
    else:
        victory_window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Defeat!')

        victory_image = pygame.image.load(config.victory_computer_image_const)
        victory_image = pygame.transform.scale(victory_image, (800, 600))

        victory_window.blit(victory_image, (0, 0))

        close_button = pygame.Rect(350, 550, 100, 50)
        pygame.draw.rect(victory_window, (0, 0, 0), close_button)  
        close_button_text = font.render('Close', True, (255, 255, 255))  
        text_rect = close_button_text.get_rect(center=close_button.center)  
        victory_window.blit(close_button_text, text_rect)

        font = pygame.font.Font(None, 66)
        font.set_bold(True)
        font.set_italic(True)  
        victory_message = font.render('Computer win!', True, (255, 0, 0))
        text_rect = victory_message.get_rect(center=(390, 70))  
        victory_window.blit(victory_message, text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()