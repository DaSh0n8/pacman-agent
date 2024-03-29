# Evolution of the approach

You can include screenshots of precompetition results and animated gifs, to showcase the evolution of your agents.

## My First Agent - Approach Foo
----

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Demo

![Demo 1](images/demo1.gif)

#### Competition results: Games - 0-0-60 | Percentile - 0%

![Demo 1](images/standing1.png)

#### Strategy summary

| Pros | Cons |
|-----------------|:-------------|
| First body part | Second cell  |
| Second line     | foo          |
----
## Heuristic Seach Implementation
----
### Iteration 1:

Our first iteration of heuristic search was very straightforward, we just created various conditions in the form of if-statements
and have them ordered by their priority in the chooseAction function. For example, running away from a ghost is a first priority,
so we'd have the if condition check if there is a ghost nearby, and have our pacman run back to the border if the condition is true.
Basically we'd just set the current target, whether it be food or border, and generate a path to the target using
Bidirectional A* Search.

#### Competition results: Games - 4-6-21 

![Iteration 1 results](images/iteration1_results.JPG)

As expected, this implementation did not perform well, as it was too simple and did not account for many scenarios, such as eating
opponent ghosts when they are scared, or going after opponent pacmans when available.
In addition, there were some bugs in ourr code that caused some of the games to fail.


### Iteration 2:

The biggest improvement we've made in this iteration is the addition of a defensive agent. This agent would go after opponent pacmans when
it's able to see them. The intuition here is that if an opponent pacman is near enough that the agent can see it, it is probably
worth going after that pacman. However, when it is not detecting any opponents close to the agent, it would act like a normal agent, 
going after the food in opponents territories. Unexpectedly, this proved to be a huge advantage, because when the agent comes back from
the border after collecting food, it would almost always block the opponent pacmans that are attempting to return to the border.

Another thing we added was the ability for pacmans to run away from ghosts, and this applies for both the offensive and defensive agents.

#### Competition results: Games - 13-3-24

![Iteration 2 results](images/iteration2_results.JPG)

After implementing these changes we were able to see some improvements in our results, but it is still not optimal 
as the winrate is fairly low.

### Iteration 3:

Although the agents are doing their jobs, they are still quite inefficient as they would often go after the same food. Therefore,
we implemented a target tracker system, that allows both the agents to communicate what food they are going after. Basically, when an
agent set its target to a specific food, that food will be taken off the food list and every time before an agent sets a target,
they would have to check if the food is in the untargeted list.

On top of that, we also implemented the cost for various conditions. For example, the cost function to an opponent ghost is
a predefined cost divided by distance to opponent ghost. Therefore, the agent would take the path with the least amount of cost, choosing
a path that the agent thinks is 'safe'.

#### Competition results: Games - 25-0-15

![Iteration 2 results](images/iteration3_results.JPG)

The new cost function and target tracker system managed to get us 25/40 wins.

## Final Technique Chosen

Other than tagging our techniques and observing their performance against staff agents, we've also matched our 
techniques against each other. We played a total of ten games and recorded who the winner is for each game.

| No. | Technique 1 | Technique 2 | Winner    |
|-----|-------------|:------------|-----------|
| 1   | MCTS        | Heuristic   | MCTS      |
| 2   | MCTS        | Q-Learning  | MCTS      |
| 3   | Q-Learning  | Heuristic   | Heuristic |
| 4   | MCTS        | Q-Learning  | MCTS      |
| 5   | Q-Learning  | MCTS        | MCTS      |
| 6   | MCTS        | Q-Learning  | MCTS      |
| 7   | Q-Learning  | Heuristic   | Heuristic |
| 8   | MCTS        | Q-Learning  | MCTS      |
| 9   | Q-Learning  | Heuristic   | Heuristic |
| 10  | MCTS        | Heuristic   | MCTS      |

As shown in the table, MCTS outperforms all the other models. Although there were games where the Heuristic Search
came close to winning, MCTS is still the more consistent technique.

Upon spectating these games live, we observed that the Heuristic Search's biggest weakness is its lack of greediness. 
The MCTS agent is far better at collecting food compared to the Heuristic Search agent. 
On top of that, The two agents
are generally not communicating very well towards the end of the games and would
often go after the same food.

Q-Learning on the other hand, is highly unoptimized and would often run into opponent ghosts. We speculate that this is 
due to the lack of data, as it'd require a lot more pretraining for the Q-table to converge.

MCTS's biggest weakness is that it performs quite poorly against defensive agents. However, the path in which the offensive
agent takes and its efficiency makes up for it.

Ultimately, we used MCTS as our final 'submission' tag on the server, as it is the best performing agent we have and yields the most
consistent scores on the server against staff agents.