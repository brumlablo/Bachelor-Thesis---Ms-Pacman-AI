package ibp.gui;


import javax.swing.*;
import java.awt.*;

/**
 * Created by babu on 3.3.16.
 */
public class GameFrame extends JFrame {
    public GameFrame(){
        start();
    }

    private void start() {
        //add(new Board());
        setTitle("IBP: Ms Pacman Demo");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(380, 380);
        setLocationRelativeTo(null);
        setVisible(true);
    }
}
