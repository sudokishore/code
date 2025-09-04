#include <stdio.h>

int main() {
    int arrival[5], burst[5], completion[5], turnaround[5], waiting[5], v[5][2];
    int visited[5] = {0};  // 0 = not completed, 1 = completed
    int i, count = 0, currentTime = 0, minIndex;
    float totalTAT = 0, totalWT = 0;

    // Input
    printf("Enter Arrival Time and Burst Time for 5 Processes:\n");
    for (i = 0; i < 5; i++) {
        printf("Process P%d:\n", i + 1);
        printf("Arrival Time: ");
        scanf("%d", &arrival[i]);
        printf("Burst Time: ");
        scanf("%d", &burst[i]);
    }

    // SJF Scheduling
    while (count < 5) {
        minIndex = -1;
        for (i = 0; i < 5; i++) {
            if (!visited[i] && arrival[i] <= currentTime) {
                if (minIndex == -1 || burst[i] < burst[minIndex]) {
                    minIndex = i;
                }
            }
        }

        // If no process has arrived yet, jump to earliest arrival
        if (minIndex == -1) {
            int earliest = -1;
            for (i = 0; i < 5; i++) {
                if (!visited[i]) {
                    if (earliest == -1 || arrival[i] < arrival[earliest]) {
                        earliest = i;
                    }
                }
            }
            currentTime = arrival[earliest];
            minIndex = earliest;
        }

        // Calculate CT, TAT, WT
        completion[minIndex] = currentTime + burst[minIndex];
        turnaround[minIndex] = completion[minIndex] - arrival[minIndex];
        waiting[minIndex] = turnaround[minIndex] - burst[minIndex];

        // Update totals
        totalTAT += turnaround[minIndex];
        totalWT += waiting[minIndex];

        // Mark as completed
        currentTime = completion[minIndex];
        visited[minIndex] = 1;
        count++;
    }

    // Output
    printf("\nProcess\tAT\tBT\tCT\tTAT\tWT\n");
    for (i = 0; i < 5; i++) {
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n",
               i + 1, arrival[i], burst[i], completion[i],
               turnaround[i], waiting[i]);
        v[i][0] = i;
        v[i][1] = completion[i];
    }

    printf("\nAverage Turnaround Time: %.2f", totalTAT / 5);
    printf("\nAverage Waiting Time: %.2f\n", totalWT / 5);

    for (int i = 0; i < 4; i++) {
        for (int j = i + 1; j < 5; j++) {
            if (v[i][1] > v[j][1]) {
                int temp = v[i][1];
                v[i][1] = v[j][1];
                v[j][1] = temp;

                temp = v[i][0];
                v[i][0] = v[j][0];
                v[j][0] = temp;

            }
        }
    }

    printf("\nGantt Chart : \n");
    for(int i=0; i<5; i++) printf("P%d\t",v[i][0]);
    printf("\n");
    for(int i=0; i<5; i++) printf("%d\t",v[i][1]);
    printf("\n");
    return 0;
}
