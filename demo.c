#include<stdio.h>

int fun(int a, int b) {
        int val = 0;
        if (a > b) {
                val = a + b;
        } else {
                val = a - b;
        }
        return val;
}

int main() {
        printf("hello gdb!\n");

        int i;
        for (i=0; i<10; i++) {
                printf("what is gdb? %d\n", i);
        }

        int a = 1, b=3;
        printf("%d\n", fun(a, b));

        return 0;
}