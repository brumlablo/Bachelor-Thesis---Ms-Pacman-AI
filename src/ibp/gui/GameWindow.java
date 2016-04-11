package ibp.gui;


import ibp.engine.Globals.*;

import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

/**
 * Created by babu on 3.3.16.
 */
public class GameWindow extends JFrame {

    public Graphics2D graphics2D;
    private BufferedImage img;
    private int width;
    private int height;

    // Arrays containing the items' data
    private ArrayList<ImageIcon> arrayItems = new ArrayList<ImageIcon>();
    private ArrayList<Integer> xPixel = new ArrayList<Integer>();
    private ArrayList<Integer> yPixel = new ArrayList<Integer>();
    private ArrayList<Integer> itemType = new ArrayList<Integer>();
    private ArrayList<Short> itemDirection = new ArrayList<Short>();

    //Images needed
    private final ImageIcon imgPacUp = new ImageIcon("data/sprites/pac_up.gif");
    private final ImageIcon imgPacDown = new ImageIcon("data/sprites/pac_down.gif");
    private final ImageIcon imgPacLeft = new ImageIcon("data/sprites/pac_left.gif");
    private final ImageIcon imgPacRight = new ImageIcon("data/sprites/pac_right.gif");
    private final ImageIcon imgGhostUp = new ImageIcon("data/sprites/ghost_up.gif");
    private final ImageIcon imgGhostDown = new ImageIcon("data/sprites/ghost_down.gif");
    private final ImageIcon imgGhostLeft = new ImageIcon("data/sprites/ghost_left.gif");
    private final ImageIcon imgGhostRight = new ImageIcon("data/sprites/ghost_right.gif");
    private final ImageIcon imgScaredUp = new ImageIcon("data/sprites/scared_up.gif");
    private final ImageIcon imgScaredDown = new ImageIcon("data/sprites/scared_down.gif");
    private final ImageIcon imgScaredLeft = new ImageIcon("data/sprites/scared_left.gif");
    private final ImageIcon imgScaredRight = new ImageIcon("data/sprites/scared_right.gif");
    private final ImageIcon imgPill = new ImageIcon("data/sprites/pill.gif");
    private final ImageIcon imgPowerPill = new ImageIcon("data/sprites/powerpill.gif");
    private final ImageIcon imgWall = new ImageIcon("data/sprites/wall.gif");
    private final ImageIcon imgEmpty = new ImageIcon("data/sprites/empty.gif");
    private final ImageIcon imgEmptyMark = new ImageIcon("data/sprites/empty_mark.gif");

    public GameWindow(final int w, final int h) {
        this.width = w;
        this.height = h;
        //add(new Board());
        setTitle("IBP: Ms Pacman Demo");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(width, height);
        setLocationRelativeTo(null);
        setVisible(true);
        setResizable(false);
        setBackground(Color.BLACK);
    }

    @Override
    public void paint(Graphics g) {

        int width = getWidth();
        int height = getHeight();

        if (img == null) {
            img = createImage(width, height);
            graphics2D = img.getGraphics();
        }


        // clear the off screen image
        graphics2D.clearRect(0, 0, width + 1, height + 1);
        graphics2D.setColor(Color.BLACK);
        graphics2D.fillRect(Globals.itemWidth * mazeWidth, Globals.itemHeight * mazeHeight);

        // draw your image off screen
        for (int i = 0; i < arrayItems.size(); i++) {
            try {
                graphics2D.drawImage(arrayItems.get(i).getImage(), xPixel.get(i), yPixel.get(i), Globals.itemWidth, Globals.itemHeight, this);
            } catch (IndexOutOfBoundsException e) {
                // Don't draw images that don't exist. :)
            }
        }

        // show the off screen image
        g.drawImage(img, 0, 0, this);

    }

    // Use an item's type and location to get the correct image. Some item types have a different image per moving direction.
    private Image properImage(int type, short direction) {
        Image properImage = imgEmpty.getImage();
        switch (type) {
            case Globals.MAZE_WALL: // Wall
                properImage = imgWall.getImage();
                break;
            case Globals.MAZE_PILL: // Pill
                properImage = imgPill.getImage();
                break;
            case Globals.MAZE_POWER_PILL: // Powerpill
                properImage = imgPowerPill.getImage();
                break;
            case Globals.MAZE_PACMAN: // Pacman
                if (direction == Globals.ACTION_UP) {
                    properImage = imgPacUp.getImage();
                } else if (direction == Globals.ACTION_DOWN) {
                    properImage = imgPacDown.getImage();
                } else if (direction == Globals.ACTION_LEFT) {
                    properImage = imgPacLeft.getImage();
                } else {
                    properImage = imgPacRight.getImage();
                }
                break;
            case Globals.MAZE_GHOST: // Ghost
                if (direction == Globals.ACTION_UP) {
                    properImage = imgGhostUp.getImage();
                } else if (direction == Globals.ACTION_DOWN) {
                    properImage = imgGhostDown.getImage();
                } else if (direction == Globals.ACTION_LEFT) {
                    properImage = imgGhostLeft.getImage();
                } else {
                    properImage = imgGhostRight.getImage();
                }
                break;
            case Globals.MAZE_FRIGHT_GHOST: // Scared ghost
                if (direction == Globals.ACTION_UP) {
                    properImage = imgScaredUp.getImage();
                } else if (direction == Globals.ACTION_DOWN) {
                    properImage = imgScaredDown.getImage();
                } else if (direction == Globals.ACTION_LEFT) {
                    properImage = imgScaredLeft.getImage();
                } else {
                    properImage = imgScaredRight.getImage();
                }
                break;
            default:
                if (Globals.markSpaces == true) {
                    properImage = imgEmptyMark.getImage();
                }
                break;
        }
        return properImage;
    }

    public void getRidOf() {
        this.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        this.setVisible(false);
        this.dispose();
    }

    public void update() {
        repaint();
    }

    // Calculate an item's pixel position based on its maze position, the screen offset and movefloat
    private int calculatePos(int pos1, int pos2, int multiply, int offset, double movefloat) {
        int floatpos;
        if (pos1 > pos2) {
            floatpos = pos2 * multiply + offset + (int) (movefloat * multiply);
        } else {
            floatpos = pos2 * multiply + offset - (int) (movefloat * multiply);
        }
        return floatpos;
    }

    // Add a new item to the visualisation
    public int addItem(int type, int x1, int y1, int x2, int y2, double movefloat) {
        short direction = -1;

        if (x1 > x2) {
            direction = Globals.ACTION_RIGHT;
        } else if (x1 < x2) {
            direction = Globals.ACTION_LEFT;
        } else if (y1 > y2) {
            direction = Globals.ACTION_DOWN;
        } else if (y1 < y2) {
            direction = Globals.ACTION_UP;
        }

        ImageIcon itemImage = new ImageIcon(properImage(type, direction));
        arrayItems.add(itemImage);
        xPixel.add(arrayItems.size() - 1, calculatePos(x1, x2, Globals.itemWidth, xOffset, movefloat));
        yPixel.add(arrayItems.size() - 1, calculatePos(y1, y2, Globals.itemHeight, yOffset, movefloat));
        itemType.add(type);
        itemDirection.add(direction);

        return arrayItems.size() - 1;
    }

    // Edit an existing item in the visualisation
    public void editItem(int itemid, int type, int x1, int y1, int x2, int y2, double movefloat) {
        boolean changeSprite = false;
        short direction = -1;

        if (x1 > x2) {
            direction = Globals.ACTION_RIGHT;
        } else if (x1 < x2) {
            direction = Globals.ACTION_LEFT;
        } else if (y1 > y2) {
            direction = Globals.ACTION_DOWN;
        } else if (y1 < y2) {
            direction = Globals.ACTION_UP;
        } else {
            direction = itemDirection.get(itemid);
        }

        if (itemType.get(itemid) != type) {
            itemType.set(itemid, type);
            changeSprite = true;
        }
        if (itemDirection.get(itemid) != direction) {
            itemDirection.set(itemid, direction);
            changeSprite = true;
        }
        if (Globals.showVisualisation == true && changeSprite == true) {
            ImageIcon itemImage = new ImageIcon(properImage(type, direction));
            arrayItems.set(itemid, itemImage);
        }
        double movefloatx = movefloat;
        double movefloaty = movefloat;
        if (x1 == x2) {
            movefloatx = 0;
        }
        if (y1 == y2) {
            movefloaty = 0;
        }

        xPixel.set(itemid, calculatePos(x1, x2, Globals.itemWidth, xOffset, movefloatx));
        yPixel.set(itemid, calculatePos(y1, y2, Globals.itemHeight, yOffset, movefloaty));
    }

    public int getItemType(int itemid) {
        return itemType.get(itemid);
    }

}