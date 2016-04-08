package ibp.engine;

import ibp.engine.Globals.*;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.InputMismatchException;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by babu on 6.3.16.
 */
public class Maze {

    public String mazeName = "";
    public int [] mazeDimensions = new int[2];
    public char [][] mazeChar;
    public Node [][] mazeBoard = null;
    private String mazePlan = "";

    /*agents positions*/
    public int[] mspacPos = new int[2];
    public int [][] ghostsPos;
    public int ghostNum = 0;

    /**
     * Maze constructor
     * @param fileName path to a file.map with the Maze info
     */
    public Maze(String fileName)
    {
        this.mazeName = fileName;
        String in = "";
        try(Scanner s = new Scanner(new FileReader(mazeName));)
        {
             while(s.hasNext()){
                in += s.next();
            }
        }
        catch (IOException | InputMismatchException e) {
            System.err.println("Error reading maze file path: " + mazeName);
            e.printStackTrace();
        }

        /* input maze values
        * [0] maze size
        * [1] maze
        * [2] MsPacman position
        * [3] Ghosts positions
         */
        String[] tokens = null;
        try {
            tokens = in.split("-");
        }
        catch (Exception e)
        {
            System.err.println("Invalid format of maze file: + fileName");
            e.printStackTrace();
        }

        //getting map dimensions
        String[] dims = tokens[0].split("\\*");
        for (int i = 0; i < dims.length; i++)
        {
            try
            {
                this.mazeDimensions[i] = Integer.parseInt(dims[i]);
            }
            catch (Exception e)
            {
                System.err.println("Invalid format of maze dimensions: " + tokens[0]);
                e.printStackTrace();
            }
        }
        System.out.println("dims: " + mazeDimensions[0]+ ", " + mazeDimensions[1]);

        //creating map
        //******************************TEST********************************************************//
        mazeChar = new char [mazeDimensions[0]] [mazeDimensions[1]];

        for (int row = 0; row < mazeDimensions[0]; row++) {
            for (int col = 0; col < mazeDimensions[1]; col++) {
                int index = (row*mazeDimensions[1]+col);
                mazeChar[row][col] = tokens[1].charAt(index);
            }
        }
        //-------------------------------------------------------------------------------//

        this.mazePlan = tokens[1];

        for(int i = 0; i < mazeDimensions[0] ;i++)
        {
            for(int j = 0; j < mazeDimensions[1] ;j++)
            {
                //System.out.print(mazeChar[i][j]);
            }
            //System.out.println();
        }

        //getting player/Ms. Pacman position, split as {P, #1, , #2}
        String [] postmp = tokens[2].split("[\\[\\]]");
        this.mspacPos[0] = Integer.parseInt(postmp[1]);
        this.mspacPos[1] = Integer.parseInt(postmp[3]);
        System.out.println("P:" + mspacPos[0]+ "," + mspacPos[1]);

        //parsing ghosts
        for(Integer i = 0; i < tokens[3].length();i++)
        {
            //total number of ghosts based on number of Gs in .map file
            if(tokens[3].charAt(i) == 'G')
                this.ghostNum++;
        }
        //ghosts spawning coordinates
        this.ghostsPos = new int[ghostNum][2];
        for (int i = 1; i <= ghostNum; i++) {

            ghostsPos[i-1][0] = Integer.parseInt(tokens[3].split("G")[i].split("[\\[\\]]")[1]);
            ghostsPos[i-1][1] = Integer.parseInt(tokens[3].split("G")[i].split("[\\[\\]]")[3]);
        }

        for (int i = 0; i < ghostNum; i ++) {
            System.out.print(ghostsPos[i][0] + "-");
            System.out.print(ghostsPos[i][1]);
            System.out.println();
        }
    }

    public static Maze createMaze(String fileName) {
        Maze tmp = new Maze(fileName);
        tmp.mazeBoard = new Node [tmp.mazeDimensions[0]][tmp.mazeDimensions[1]];
        tileType t = null;
        ArrayList <Integer> neighbours = new ArrayList <Integer> ();
        ArrayList <Integer> successors = new ArrayList <Integer> ();

        for (int row = 0; row < tmp.mazeDimensions[0]; row++) {
            for (int col = 0; col < tmp.mazeDimensions[1]; col++) {
                switch(tmp.mazeChar[row][col])
                {
                    case 'C':
                        t = tileType.WALL;
                        break;
                    case 'T':
                        t = tileType.WALL;
                        break;
                    case 'W':
                        t = tileType.WALL;
                        break;
                    case '.':
                        t = tileType.PILL;
                        break;
                    case ':':
                        t = tileType.POWERPILL;
                        break;
                    case '/':
                        t = tileType.NONE;
                        break;
                    case 'G':
                        t = tileType.GHOST;
                        break;
                    case 'P':
                        t = tileType.MSPAC;
                        break;
                    default:
                        System.err.println("Error parsing mazeBoard string from file.");
                        System.exit(1);
                }
                int index = (row*(tmp.mazeDimensions[1])+col);
                tmp.mazeBoard[row][col] = new Node(row, col, index,t,neighbours,successors);
            }
        }
        return tmp;
    }
}
