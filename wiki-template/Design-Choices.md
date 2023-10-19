# Design Choices

summary of your design choices


## General Comments

_General comments about the project goes here_

## Heuristic Search
### Offense
1) For the heuristic search agent, the offense was pretty straightforward. The goal is to just get
to the food or border, depending on the agent's current conditions, while attempting to dodge or evade
opponent ghosts. However, if there is an opportunity to go after an opponent scared ghost, that would be prioritized.
### Defense
1) This approach was to go after the opponent's agents directly when our agent is able to see them/get their location. We
realised that an opponent agent has to be relatively close for our agent to get their accurate location, so we thought that
if they are close enough, it is probably also worth it to go straight for the opponent pacman.