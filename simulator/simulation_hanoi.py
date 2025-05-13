import json
import pygame
import sys
import argparse  # <- Import argparse

# Importing custom modules
import animator
import background
import logic
import sprites
import synchronizer
from constants import *


# ----------------------------------------------
# Argument Parsing
# ----------------------------------------------

def parse_arguments():
    parser = argparse.ArgumentParser(description="Hanoi Tower Simulation")
    parser.add_argument(
        "--sequence",
        type=str,
        default="./sequence.json",
        help="Path to the sequence JSON file"
    )
    return parser.parse_args()


# ----------------------------------------------
# Sequence Loading
# ----------------------------------------------

# Function to load configuration from JSON file
def load_configuration(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


# ----------------------------------------------
# Pygame Initialization
# ----------------------------------------------

# Initialize Pygame and create the display screen
def initialize_pygame():
    pygame.init()
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Main game loop
def main():
    # Parse command-line arguments
    args = parse_arguments()

    # Load initial and sequence states
    initial_state = load_configuration("./initial_state.json")
    sequence = load_configuration(args.sequence)

    # These two variables are important for the animator and the sequencer
    number_of_disks = sprites.obtain_number_of_disks(initial_state)
    disk_height = sprites.obtain_disks_height(number_of_disks)

    # Initialize Pygame
    screen = initialize_pygame()
    clock = pygame.time.Clock()
    pygame.display.set_caption("Hanoi's tower simulation")

    # Initialize the logic
    hanoi_base = logic.initialize_logic(initial_state, disk_height)

    # Initialize the disk sprites
    disks_sprites_groups = pygame.sprite.Group()
    disks_sprites = sprites.create_sprites(
        number_of_disks, disk_height, hanoi_base, initial_state)
    for disk_id in disks_sprites:
        disks_sprites_groups.add(disks_sprites[disk_id])

    # Initiate the synchronizer and animator
    sync_manager = synchronizer.Synchronizer(sequence)
    anim_manager = animator.Animator(hanoi_base, disk_height)

    # Flag to execute the next sequence
    flag_execute_next_seq = anim_manager.ask_new_seq

    while True:  # Sequence Loop
        handle_events()  # Handle Pygame events

        if flag_execute_next_seq:
            seq = sync_manager.update()
            anim_manager.get_sequence(seq)

        anim_manager.animate(disks_sprites)
        disks_sprites_groups.update()
        flag_execute_next_seq = anim_manager.ask_new_seq

        background.draw_background(screen)
        disks_sprites_groups.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# Handle Pygame events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Entry point
if __name__ == "__main__":
    main()
