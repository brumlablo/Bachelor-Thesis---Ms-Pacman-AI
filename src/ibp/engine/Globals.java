package ibp.engine;

/**
 * Created by babu on 6.3.16.
 */
public class Globals {

    //canvas size
    final static int width = 400;
    final static int height = 400;

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

    public enum actions {
        LEFT(1), UP(2), RIGHT(3), DOWN(4);

        private int num;
        private actions(int value) {
            this.num = value;
        }

        public int getNum() {
            return num;
        }
    }

}
