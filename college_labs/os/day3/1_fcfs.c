#include <stdio.h>

int main() {
    int arrival[5], burst[5], completion[5], turnaround[5], waiting[5];
    int i, j, temp, currentTime = 0;
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

    // Sort by Arrival Time
    for (i = 0; i < 4; i++) {
        for (j = i + 1; j < 5; j++) {
            if (arrival[i] > arrival[j]) {
                // swap arrival
                temp = arrival[i];
                arrival[i] = arrival[j];
                arrival[j] = temp;
                // swap burst
                temp = burst[i];
                burst[i] = burst[j];
                burst[j] = temp;
            }
        }
    }

    // FCFS Calculation
    for (i = 0; i < 5; i++) {
        if (currentTime < arrival[i]) {
            currentTime = arrival[i]; // CPU idle until process arrives
        }
        completion[i] = currentTime + burst[i];         // CT
        turnaround[i] = completion[i] - arrival[i];     // TAT
        waiting[i] = turnaround[i] - burst[i];          // WT
        currentTime = completion[i];

        totalTAT += turnaround[i];
        totalWT += waiting[i];
    }

    // Output
    printf("\nProcess\tAT\tBT\tCT\tTAT\tWT\n");
    for (i = 0; i < 5; i++) {
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n",
               i + 1, arrival[i], burst[i],
               completion[i], turnaround[i], waiting[i]);
    }

    printf("\nAverage Turnaround Time: %.2f", totalTAT / 5);
    printf("\nAverage Waiting Time: %.2f\n", totalWT / 5);

    return 0;
}
