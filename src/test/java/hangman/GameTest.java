package hangman;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class GameTest {

    @Test
    void initialDisplayWordIsAllUnderscores() {
        Game game = new Game("JAVA");
        assertEquals("____", game.getDisplayWord());
    }

    @Test
    void spacesStayVisibleInPhrases() {
        Game game = new Game("HI THERE");
        assertEquals("__ _____", game.getDisplayWord());
    }

    @Test
    void correctGuessRevealsAllMatchingLetters() {
        Game game = new Game("BANANA");
        boolean found = game.guessLetter('A');
        assertTrue(found);
        assertEquals("_A_A_A", game.getDisplayWord());
    }

    @Test
    void incorrectGuessIncrementsCounter() {
        Game game = new Game("JAVA");
        game.guessLetter('Z');
        assertEquals(1, game.getIncorrectGuesses());
    }

    @Test
    void repeatedGuessIsIgnoredAndNotDoubleCounted() {
        Game game = new Game("JAVA");
        game.guessLetter('Z');
        game.guessLetter('Z');
        assertEquals(1, game.getIncorrectGuesses());
    }

    @Test
    void guessIsCaseInsensitive() {
        Game game = new Game("JAVA");
        game.guessLetter('j');
        assertEquals("J___", game.getDisplayWord());
    }

    @Test
    void isWonWhenAllLettersRevealed() {
        Game game = new Game("HI");
        game.guessLetter('H');
        game.guessLetter('I');
        assertTrue(game.isWon());
        assertTrue(game.isGameOver());
    }

    @Test
    void isLostAfterMaxIncorrectGuesses() {
        Game game = new Game("JAVA");
        for (char c : new char[] {'B', 'C', 'D', 'E', 'F', 'G'}) {
            game.guessLetter(c);
        }
        assertEquals(6, game.getIncorrectGuesses());
        assertTrue(game.isLost());
        assertTrue(game.isGameOver());
        assertFalse(game.isWon());
    }

    @Test
    void gameIsNotOverWhileGuessesRemainAndWordIncomplete() {
        Game game = new Game("JAVA");
        game.guessLetter('B');
        assertFalse(game.isGameOver());
    }

    @Test
    void guessedLettersAreTracked() {
        Game game = new Game("JAVA");
        game.guessLetter('j');
        game.guessLetter('z');
        assertEquals(2, game.getGuessedLetters().size());
        assertTrue(game.getGuessedLetters().contains('J'));
        assertTrue(game.getGuessedLetters().contains('Z'));
    }
}
