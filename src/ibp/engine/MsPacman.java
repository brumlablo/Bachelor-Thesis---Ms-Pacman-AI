package ibp.engine;

import ibp.gui.GameWindow;
import java.awt.*;


public class MsPacman {

    public static void main(String[] args) {

        EventQueue.invokeLater(new Runnable() {

            @Override
            public void run() {
                readArgs(args);
                initGUI();

                };
            });
    }

    private static void readArgs(String[] args)
    {
        //arguments parsing
    }

    private static void initGUI() {
        GameWindow game = new GameWindow(Globals.width, Globals.height);
        game.setVisible(true);
        Maze m = Maze.createMaze("data/maps/2011.map");
        System.out.println("----------------------chvile pravdy--------------------------");
        for (int row = 0; row < m.mazeDimensions[0]; row++) {
            for (int col = 0; col < m.mazeDimensions[1]; col++) {
                System.out.print(m.mazeBoard[row][col].type);
            }
            System.out.println();
        }
            }
}

