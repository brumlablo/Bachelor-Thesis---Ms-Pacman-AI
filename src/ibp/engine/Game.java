package ibp.engine;

public class Game
{
    public int timeout;
    public GameState initState;
    public Agent [] agents;
    private boolean isWin;
    private boolean isLost;

    public Game() {
        timeout = 30;
    }

    public Game(int t) {
        timeout = t;
    }

    public MsPacman newGame (Maze lay, //pacmanAgent, ghostAgents, display, quiet = False, catchExceptions=False)
    {
        agents.add(new Agent(0,(lay.mspacPos[0] * lay.mazeDimensions[1] + lay.mspacPos[1])));
        int i;
        for(i = 0, i < lay.ghostNum,i++)
        {
            agents.add(new Agent(i+1,(lay.initGhostsPos[0] * lay.mazeDimensions[1] + lay.initGhostsPos[1])));
        }

        initState = new GameState();
        initState.initialize(lay, agents);
        game = Game(agents);// display, self, catchExceptions = catchExceptions)
        game.state = initState;
        return game;
    }
/*
    void process(GameState st,Game g)
    {
        if(st.isWin)
            isWin = true;
        if(st.isLost)
            isLost = false;
    }

    void win(GameState st, Game g)
    {
        //if display/guiet
        System.out.println("Pacman WON! Score: ");
        game.gameOver = true;
    }

    void lost(GameState st, Game g)
    {
        //if display/guiet
        System.out.println("Pacman DIED! Score: ");
        game.gameOver = true;
    }
*/
    /*def getProgress(self, game):
        return float(game.state.getNumFood()) / self.initialState.getNumFood()

        def agentCrash(self, game, agentIndex):
        if agentIndex == 0:
        print "Pacman crashed"
        else:
        print "A ghost crashed"

    int getMaxTotalTime(agentIndex) {
        return timeout;
    }
    int getMaxStartupTime(agentIndex) {
        return timeout;
    }
    int getMoveWarningTime(agentIndex) {
        return timeout;
    }
    int getMoveTimeout(agentIndex) {
        return timeout;
    }
    int getMaxTimeWarnings(agentIndex) {
        return 0;
    }*/
}
