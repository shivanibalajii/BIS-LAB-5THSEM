#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define N 5
float R[N]={.14,.18,.12,.15,.11}, V[N]={.22,.25,.20,.28,.21};
float cur[N], best[N], best_score;

void create(){ for(int i=0;i<N;i++) cur[i]=1.f/N; }

void mutate(){
    int i=rand()%N;
    cur[i]+= (rand()/(float)RAND_MAX-.5f)*.2f;
    if(cur[i]<0) cur[i]=0;
    float s=0; for(int j=0;j<N;j++) s+=cur[j];
    for(int j=0;j<N;j++) cur[j]/=s;
}

float evaluate(){
    float r=0,v=0;
    for(int i=0;i<N;i++){ r+=cur[i]*R[i]; v+=cur[i]*V[i]; }
    return r/v*100;
}

void kill(){ for(int i=0;i<N;i++) cur[i]=best[i]; }

int main(){
    srand(time(0));
    create(); best_score=evaluate();
    for(int i=0;i<N;i++) best[i]=cur[i];

    for(int g=0; g<1000; g++){
        mutate();
        float s=evaluate();
        if(s>best_score){ best_score=s; for(int i=0;i<N;i++) best[i]=cur[i]; }
        else kill();
    }

    // Calculate final portfolio performance
    float total_return=0, total_vol=0;
    for(int i=0;i<N;i++){ total_return+=best[i]*R[i]; total_vol+=best[i]*V[i]; }

    const char* names[N]={"RELIANCE","TCS","HDFC","INFY","ICICI"};
    printf("=== Portfolio Performance ===\n");
    printf("Total Return:   %.1f%%\n", total_return*100);
    printf("Total Volatility: %.1f%%\n", total_vol*100);
    printf("Sharpe Ratio:   %.2f\n", total_return/total_vol);
    printf("\n--- Allocation ---\n");
    for(int i=0;i<N;i++)
        printf("  %-9s %5.1f%%  (return %.1f%%, vol %.1f%%)\n",
               names[i], best[i]*100, R[i]*100, V[i]*100);
}   
