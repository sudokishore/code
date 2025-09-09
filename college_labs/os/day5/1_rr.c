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
    // Process labels centered
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
    int at[N], bt[N], completed=0, current_time=0;
    int gantt[MAX], gantt_idx=0, q;
    int tat[N], wt[N];
    printf("Enter arrival time and burst time for 5 processes:\n");
    for (int i=0; i<N; i++) {
        printf("P%d Arrival Time : ", i+1); scanf("%d", &at[i]);
        printf("P%d Burst Time : ", i+1); scanf("%d", &bt[i]);
    }
    printf("Enter the quantum value : "); scanf("%d", &p);
    int is_completed[N] = {0}, start_time[N];
    for(int i=0; i<N; i++) start_time[i] = -1;

    while (completed < N) {
        int idx = -1;
        for (int i=0; i<N; i++) {
            if (at[i] <= current_time && !is_completed[i] && priority[i] < highest_priority) {
                highest_priority = priority[i];
                idx = i;
            }
        }
        if (idx == -1) {
            current_time++; // CPU idle
        } else {
            // Mark start time if first run
            if(start_time[idx] == -1) start_time[idx] = current_time;
            // Execute process fully (non-preemptive)
            for (int k=0; k < bt[idx]; k++)
                gantt[gantt_idx++] = idx;
            current_time += bt[idx];
            is_completed[idx] = 1;
            completed++;
            // Calculate turnaround and waiting time
            tat[idx] = current_time - at[idx];
            wt[idx] = tat[idx] - bt[idx];
        }
    }
    printf("\nGantt Chart : \n");
    print_gantt(gantt, gantt_idx);

    printf("\nProcess | Arrival | Burst | Turnaround | Waiting\n");
    int total_tat=0, total_wt=0;

    for(int i=0; i<N; i++){
        printf("P%d      |   %2d    |    %2d    |     %2d     |    %2d\n",
               i+1, at[i], bt[i], tat[i], wt[i]);
        total_tat += tat[i];
        total_wt += wt[i];
    }
    printf("\nAverage Turnaround Time: %.2f\n", (float)total_tat / N);
    printf("Average Waiting Time   : %.2f\n", (float)total_wt / N);

    return 0;
}

