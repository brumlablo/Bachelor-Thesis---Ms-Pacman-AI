package ibp.engine;

/**
 * Created by babu on 6.3.16.
 */
public class Globals {

    //canvas size
    final static int mazeWidth = 400;
    final static int mazeHeight = 400;

    //single item size
    public static int itemWidth = 16;
    public static int itemHeight = 16;

    //  consts
    public enum tileType {
        NONE(0), WALL(1), PILL(2), POWERPILL(3), GHOST(4), MSPAC(5);

    private int num;
    private tileType(int value) {
        this.num = value;
    }

    public int getNum() {
        return num;
    }

    }

    public enum ghostState {
        RAND(1), CHASE(2), SCATTER(3), AFRAID(4);

        private int num;
        private ghostState(int value) {
            this.num = value;
        }

        public int getNum() {
            return num;
        }
    }

    public enum mspacState {
        MANUAL(1), LEARN(2), AI(3);

        private int num;
        private mspacState(int value) {
            this.num = value;
        }

        public int getNum() {
            return num;
        }
    }

    public enum direction {
        LEFT(1), UP(2), RIGHT(3), DOWN(4);

        private int num;
        private direction(int value) {
            this.num = value;
        }

        public int getNum() {
            return num;
        }
    }

    public static direction reverseDirection(direction dir)
    {
        direction tmp = dir;
        switch(dir)
        {
            case LEFT:
                tmp = direction.RIGHT;
                break;
            case UP:
                tmp = direction.DOWN;
                break;
            case RIGHT:
                tmp = direction.LEFT;
                break;
            case DOWN:
                tmp = direction.UP;
                break;
        }
        return tmp;
    }

}
