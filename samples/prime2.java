// PrimeChecker2.java
public class PrimeChecker2 {

    // Function to check if a number is prime
    public static boolean checkPrime(int num) {
        if (num <= 1) {
            return false;
        }
        for (int i = 2; i < num; i++) {
            if (num % i == 0) {
                return false;
            }
        }
        return true;
    }

    // Main method to test the function
    public static void main(String[] args) {
        int numberToCheck = 29;
        boolean isPrime = checkPrime(numberToCheck);
        if (isPrime) {
            System.out.println(numberToCheck + " is a prime number.");
        } else {
            System.out.println(numberToCheck + " is not a prime number.");
        }
    }
}
