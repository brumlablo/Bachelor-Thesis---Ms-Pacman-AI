package ibp.engine;

import java.util.ArrayList;

public class Game
{
    public int timeout;
    public GameState initState;
    public GameState actState;
    public ArrayList<Agent> agents;
    private boolean isWin;
    private boolean isLost;

    public Game() {
        timeout = 30;
    }

    public Game(int t) {
        timeout = t;
    }

    public GameState newGame (Maze m)
    {
        agents.add(new Agent(0,(m.mspacPos[0] * m.mazeDimensions[1] + m.mspacPos[1])));
        int i;
        for(i = 0, i < m.ghostNum,i++)
        {
            agents.add(new Agent(i+1,(m.initGhostsPos[0] * m.mazeDimensions[1] + m.initGhostsPos[1])));
        }

        initState = new GameState(m,agents);
        actState = initState;
        return actState;
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
