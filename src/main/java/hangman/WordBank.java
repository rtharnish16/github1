package hangman;

import java.util.Random;

/**
 * Supplies the word to guess when the computer is choosing (as opposed to
 * one player entering a custom word/phrase for the others to guess).
 */
public class WordBank {

    private static final String[] WORDS = {
        "JAVA", "PROGRAMMING", "OBJECT", "ORIENTED", "HANGMAN",
        "COMPUTER", "ALGORITHM", "DATABASE", "INTERFACE", "ENCAPSULATION"
    };

    private final Random random = new Random();

    /**
     * @return a random word from the built-in word list, in upper case.
     */
    public String selectRandomWord() {
        int index = random.nextInt(WORDS.length);
        return WORDS[index];
    }
}
