package Tyrael;
import java.util.Scanner;

public class Scores {
    public static void main (String[]args) {

        int score1, score2, score3;
        Scanner Input = new Scanner(System.in);

        int i;
        do {
            i = 0;
            System.out.println("Enter Quiz score: ");
            score1 = Input.nextInt();

            if (score1 < 0 || score1 > 30) {
                System.out.println("Score invalid");


            }
            ;
        } while (i != 0);
        








        System.out.println("Enter Activity score: ");
        score2 = Input.nextInt();

        System.out.println("Enter Exam score: ");
        score3 = Input.nextInt();


    }
}
