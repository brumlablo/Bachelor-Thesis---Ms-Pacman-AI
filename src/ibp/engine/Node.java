package ibp.engine;

import ibp.engine.Globals.*;

import java.util.ArrayList;

/**
 * Created by babu on 7.4.16.
 */
public class Node {

    public int row,col;
    public int index;
    public tileType type;
    public ArrayList <Integer> neighbours = new ArrayList <Integer> ();
    //public ArrayList <Integer> successors = new ArrayList <Integer> ();

    public Node(int r, int c, int i,tileType t,ArrayList <Integer>neigh) {
        this.row = r;
        this.col = c;
        this.index = i;
        this.type = t;
        this.neighbours = neigh;

    }
}
