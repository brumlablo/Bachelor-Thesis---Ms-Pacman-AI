package ibp.gui;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

/**
 * Created by babu on 20.3.16.
 */
public class GameLoop extends JPanel implements Runnable{

    private Thread thread;
    private boolean running;

    private int fps; //frames per second
    private int tps; //ticks per second

    private int width;
    private int height;

    public Graphics2D graphics2D;
    private BufferedImage img;

    public static double currentFps = 120D;

    public GameLoop(final int width, final int height) {
        this.width = width;
        this.height = height;

        setPreferredSize(new Dimension(width,height));
        setFocusable(false);
        requestFocus();
    }

    @Override
    public void addNotify() {
        super.addNotify();

        if(thread == null)
        {
            thread = new Thread(this);
            thread.start();
        }
    }

    @Override
    public void run() {
        init();
        long lastTime = System.nanoTime();
        double nsPerTick = 10000000000D / currentFps;
        int frames = 0;
        int ticks = 0;
        long lastTimer = System.currentTimeMillis();
        double deltaTime = 0; //for speeding up the game

        while(running)
        {
            long now = System.nanoTime();
            deltaTime += (now - lastTime) / nsPerTick;
            lastTime = now;
            boolean shouldRender = false;

            while(deltaTime >= 1)
            {
                ticks++;
                tick(deltaTime); // update the slowed game
                deltaTime -= 1;
                shouldRender = true;
            }

            if(shouldRender)
            {
                frames++;
                render();
            }

            /*SLEEP*/
            try {
                Thread.sleep(2);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            if((System.currentTimeMillis() - lastTimer) >= 100)
            {
                lastTimer += 1000;
                tps = frames;
                fps = ticks;
                frames = 0;
                ticks = 0;
            }
        }
    }

    public void init() {
        img = new BufferedImage(width,height,BufferedImage.TYPE_INT_RGB);
        graphics2D = (Graphics2D) img.getGraphics();
        running = true;
    }

    public void render() {
        graphics2D.clearRect(0,0,width,height);
        clear();
    }

    public void tick(double deltaTime) {
    }

    public void clear () {
        Graphics g2 = getGraphics();
        if(img != null)
        {
            g2.drawImage(img,0,0,null);
        }
        g2.dispose();
    }
}