package ibp.engine;

import static ibp.engine.Globals.*;

/**
 * Created by babu on 3.3.16.
 */
public class Agent {
    private int agentIndex;
    private int posIndex;
    public double speed = 0.5;
    public ghostState state = ghostState.RAND;


    public Agent(int agentIndex, int posIndex) {
        this.agentIndex = agentIndex;
        this.posIndex = posIndex;
    }
}
