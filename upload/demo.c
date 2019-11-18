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
        printf("hello gdbweb!\n");

        int i;
        for (i=0; i<10; i++) {
                printf("what is gdbweb? %d\n", i);
        }

        int a, b;
        scanf("%d%d", &a, &b);
        printf("%d\n", fun(a, b));

        return 0;
}
