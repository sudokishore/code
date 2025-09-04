#include <stdio.h>
#define N 5
#define MAX 100

void print_gantt(int g[], int len) {
    int i=0, j;
    // Top border
    while (i < len) {
        j = i+1;
        while (j < len && g[j] == g[i]) j++;
        printf("+");
        for (int k=0; k < (j - i)*4 - 1; k++) printf("-");
        i = j;
    }
    printf("+\n");
    // Process labels
    i = 0;
    while (i < len) {
        j = i+1;
        while (j < len && g[j] == g[i]) j++;
        int pad = ((j - i)*4 - 3) / 2;
        printf("|");
        for (int k=0; k < pad; k++) printf(" ");
        printf("P%d", g[i] + 1);
        for (int k=0; k < (j - i)*4 - 3 - pad; k++) printf(" ");
        i = j;
    }
    printf("|\n");
    // Bottom border
    i=0;
    while (i < len) {
        j = i+1;
        while (j < len && g[j] == g[i]) j++;
        printf("+");
        for (int k=0; k < (j - i)*4 - 1; k++) printf("-");
        i = j;
    }
    printf("+\n");
    // Time labels
    printf("0");
    i=0;
    while (i < len) {
        j = i+1;
        while (j < len && g[j] == g[i]) j++;
        for (int k=0; k < (j - i)*4 - 1; k++) printf(" ");
        printf("%d", j);
        i = j;
    }
    printf("\n");
}

int main() {
    int at[N], bt[N], rt[N], ct=0, completed=0, shortest, min;
    int gantt[MAX], idx=0;
    int tat[N], wt[N];

    printf("Enter arrival time and burst time for 5 processes:\n");
    for (int i=0; i<N; i++) {
        printf("P%d Arrival Time: ", i+1);
        scanf("%d", &at[i]);
        printf("P%d Burst Time: ", i+1);
        scanf("%d", &bt[i]);
        rt[i] = bt[i];
    }

    while (completed < N) {
        min = 1e9; shortest = -1;
        for (int i=0; i<N; i++) {
            if (at[i] <= ct && rt[i] > 0) {
                if (rt[i] < min || (rt[i] == min && at[i] < at[shortest])) {
                    min = rt[i];
                    shortest = i;
                }
            }
        }
        if (shortest == -1) {
            ct++;
            continue;
        }
        gantt[idx++] = shortest;
        rt[shortest]--;
        ct++;
        if (rt[shortest] == 0) {
            completed++;
            tat[shortest] = ct - at[shortest];
            wt[shortest] = tat[shortest] - bt[shortest];
        }
    }
    printf("\nGantt Chart : \n");
    print_gantt(gantt, idx);

    printf("\nProcess | Arrival | Burst | Turnaround | Waiting\n");
    int total_tat = 0, total_wt = 0;
    for (int i=0; i<N; i++) {
        printf("P%d      |   %2d    |  %2d   |     %2d     |    %2d\n",
               i+1, at[i], bt[i], tat[i], wt[i]);
        total_tat += tat[i];
        total_wt += wt[i];
    }
    printf("\nAverage Turnaround Time: %.2f\n", (float)total_tat / N);
    printf("Average Waiting Time   : %.2f\n", (float)total_wt / N);

    return 0;
}

