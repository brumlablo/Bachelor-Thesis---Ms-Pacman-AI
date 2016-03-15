package ibp.engine;

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

    private String mazeName = "";
    private int [] mazeDimensions = new int[2];
    private char [][] maze;
    private String mazePlan = "";

    /*agents positions*/
    private int[] mspacPos = new int[2];
    private int [][] ghostsPos;
    private int ghostNum = 0;

    /**
     * Maze constructor
     * @param fileName
     */
    public Maze(String fileName)
    {
        this.mazeName = fileName;
        readMaze(this.mazeName);
    }

    /**
     * Init Maze by reading selected Maze file.map
     * @param fileName path to a file.map with the Maze info
     */
    private void readMaze(String fileName)
    {
        String in = "";
        try(Scanner s = new Scanner(new FileReader(fileName));)
        {
             while(s.hasNext()){
                in += s.next();
            }
        }
        catch (IOException | InputMismatchException e) {
            System.err.println("Error reading maze file path: " + fileName);
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

        //Parsing dimensions of map
        String[] dims = tokens[0].split("\\*");
        for (int i = 0; i < dims.length; i++)
        {
            this.mazeDimensions[i] = Integer.parseInt(dims[i]);
        }
        System.out.println("dims: " + mazeDimensions[0]+ ", " + mazeDimensions[1]);

        //Whole map
        maze = new char [mazeDimensions[0]] [mazeDimensions[1]];

        for (int row = 0; row < mazeDimensions[0]; row++) {
            for (int col = 0; col < mazeDimensions[1]; col++) {
                int index = (row*mazeDimensions[1]+col);
                maze[row][col] = tokens[1].charAt(index);
            }
        }

        this.mazePlan = tokens[1];

        for(int i = 0; i < mazeDimensions[0] ;i++)
        {
            for(int j = 0; j < mazeDimensions[1] ;j++)
            {
                System.out.print(maze[i][j]);
            }
            System.out.println();
        }
        //------------------------


        //Player/Ms. Pacman position, split as {P, #1, , #2}
        String [] postmp = tokens[2].split("[\\[\\]]");
        this.mspacPos[0] = Integer.parseInt(postmp[1]);
        this.mspacPos[1] = Integer.parseInt(postmp[3]);
        System.out.println("P:" + mspacPos[0]+ "," + mspacPos[1]);
        //------------------------------------------------



        //Parsing ghosts
        for(Integer i = 0; i < tokens[3].length();i++)
        {
            //Getting total number of ghosts based on number of Gs in .map file
            if(tokens[3].charAt(i) == 'G')
                this.ghostNum++;
        }
        //Now they coordinates
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
        //--------------------------------------------------------
    }

}
