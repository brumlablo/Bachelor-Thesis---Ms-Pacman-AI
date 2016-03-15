package ibp.engine;

import ibp.gui.GameFrame;
import java.awt.*;


public class MsPacman {

    public static void main(String[] args) {

        EventQueue.invokeLater(new Runnable() {

            @Override
            public void run() {
                //GameFrame game = new GameFrame();
                //game.setVisible(true);
                Maze m = new Maze("data/maps/2011.map");
            }
        });
    }
}
