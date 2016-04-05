package ibp.engine;

import ibp.gui.GameWindow;
import java.awt.*;


public class MsPacman {

    public static void main(String[] args) {

        EventQueue.invokeLater(new Runnable() {

            @Override
            public void run() {
                GameWindow game = new GameWindow(Globals.width, Globals.height);
                game.setVisible(true);
                Maze m = new Maze("data/maps/2011.map");
            }
        });
    }
}
