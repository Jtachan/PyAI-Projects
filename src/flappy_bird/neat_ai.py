"""
AI module
"""
import os.path

import neat
from _elements import Bird
from game import GameApp


def load_config(file_name: str = "neat_config.txt") -> neat.Config:
    """
    Loads the configuration from the config file, which must be at this folder level
    """
    config_path = os.path.join(os.path.dirname(__file__), file_name)
    return neat.Config(
        genome_type=neat.DefaultGenome,
        reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet,
        stagnation_type=neat.DefaultStagnation,
        filename=config_path,
    )


def fitness(genomes: list[neat.DefaultGenome], config: neat.Config):
    birds = []
    networks = []
    gens = []

    for _, genome in genomes:
        genome.fitness = 0
        gens.append(genome)
        birds.append(Bird())
        networks.append(neat.nn.FeedForwardNetwork.create(genome, config))

    game = GameApp(birds=birds, pipes_distance=600)
    game.set_network_parameters(networks=networks, genomes=genomes)
    game.run()


if __name__ == "__main__":
    cfg = load_config()
    population = neat.Population(cfg)
    population.add_reporter(neat.StdOutReporter(show_species_detail=True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.run(fitness, 50)
