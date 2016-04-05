package ibp.gui;


import javax.swing.*;
import java.awt.*;

/**
 * Created by babu on 3.3.16.
 */
public class GameWindow extends JFrame {

    public GameWindow(final int width, final int height) {
        //add(new Board());
        setTitle("IBP: Ms Pacman Demo");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(width, height);
        setLocationRelativeTo(null);
        setVisible(true);
        setResizable(false);
    }
}
