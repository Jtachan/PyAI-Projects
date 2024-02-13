"""
AI module
"""
import os.path
import neat


if __name__ == '__main__':
    config_path = os.path.join(os.path.dirname(__file__), "neat_config.txt")
    config = neat.Config(
        genome_type=neat.DefaultGenome,
        reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet,
        stagnation_type=neat.DefaultStagnation,
        filename=config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(show_species_detail=True))

    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(..., 50)
