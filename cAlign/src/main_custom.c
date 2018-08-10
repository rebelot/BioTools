#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/param.h>
#include <float.h>

float penalty(int k){
    float g_op = -11.;
    float g_ex = -2.;
    return g_op + g_ex*(k-1.);
}

void printmat(char *si, char*sj, int i_len, int j_len, float matrix[][j_len]){
    int i, j;
    printf("      ");
    for(j = 0; j < j_len; j++){
        printf("%5c ", sj[j]);
    }
    printf("\n");
    for(i = 0; i < i_len; i++) {
        if (i > 0){
        printf("%5c ", si[i-1]);
        }
        else{
            printf("      ");
        }
        for(j = 0; j < j_len; j++){
            printf("%5.2f ", matrix[i][j]);
        }
        printf("\n");
    }
}

float submat(char aa_i, char aa_j){
    const char aa_key[20] = {'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'};
    const char aa_custom_key[21] = {'A', 'R', 'N', 'D', 'C', 'E', 'Q', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'X', 'V'};
    /*int b62[20][20] = {
	{ 4, -1, -2, -2,  0, -1, -1,  0, -2, -1, -1, -1, -1, -2, -1,  1,  0, -3, -2,  0},
	{-1,  5,  0, -2, -3,  1,  0, -2,  0, -3, -2,  2, -1, -3, -2, -1, -1, -3, -2, -3},
	{-2,  0,  6,  1, -3,  0,  0,  0,  1, -3, -3,  0, -2, -3, -2,  1,  0, -4, -2, -3},
	{-2, -2,  1,  6, -3,  0,  2, -1, -1, -3, -4, -1, -3, -3, -1,  0, -1, -4, -3, -3},
	{ 0, -3, -3, -3,  9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1},
	{-1,  1,  0,  0, -3,  5,  2, -2,  0, -3, -2,  1,  0, -3, -1,  0, -1, -2, -1, -2},
	{-1,  0,  0,  2, -4,  2,  5, -2,  0, -3, -3,  1, -2, -3, -1,  0, -1, -3, -2, -2},
	{ 0, -2,  0, -1, -3, -2, -2,  6, -2, -4, -4, -2, -3, -3, -2,  0, -2, -2, -3, -3},
	{-2,  0,  1, -1, -3,  0,  0, -2,  8, -3, -3, -1, -2, -1, -2, -1, -2, -2,  2, -3},
	{-1, -3, -3, -3, -1, -3, -3, -4, -3,  4,  2, -3,  1,  0, -3, -2, -1, -3, -1,  3},
	{-1, -2, -3, -4, -1, -2, -3, -4, -3,  2,  4, -2,  2,  0, -3, -2, -1, -2, -1,  1},
	{-1,  2,  0, -1, -3,  1,  1, -2, -1, -3, -2,  5, -1, -3, -1,  0, -1, -3, -2, -2},
	{-1, -1, -2, -3, -1,  0, -2, -3, -2,  1,  2, -1,  5,  0, -2, -1, -1, -1, -1,  1},
	{-2, -3, -3, -3, -2, -3, -3, -3, -1,  0,  0, -3,  0,  6, -4, -2, -2,  1,  3, -1},
	{-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4,  7, -1, -1, -4, -3, -2},
	{ 1, -1,  1,  0, -1,  0,  0,  0, -1, -2, -2,  0, -1, -2, -1,  4,  1, -3, -2, -2},
	{ 0, -1,  0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1,  1,  5, -2, -2,  0},
	{-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1,  1, -4, -3, -2, 11,  2, -3},
	{-2, -2, -2, -3, -2, -1, -2, -3,  2, -1, -1, -2, -1,  3, -3, -2, -2,  2,  7, -1},
	{ 0, -3, -3, -3, -1, -2, -2, -3, -3,  3,  1, -2,  1, -1, -2, -2,  0, -3, -1,  4}};
	*/
	float custom_mat[21][21] = {
	{5.83, 3.46, 3.64, 3.39, 3.86, 3.65, 3.58, 3.69, 3.50, 3.80, 3.55, 3.75, 3.89, 3.39, 3.49, 3.91, 3.91, 3.05, 4.11, 3.37, 3.92},
	{3.46, 6.92, 3.99, 3.68, 3.12, 3.80, 4.15, 3.13, 4.69, 3.06, 3.03, 4.72, 3.43, 2.95, 3.27, 3.65, 3.53, 3.00, 4.78, 3.61, 3.11},
	{3.64, 3.99, 6.22, 4.54, 3.46, 4.10, 4.10, 3.73, 4.51, 3.21, 3.09, 4.28, 3.55, 3.16, 3.50, 4.14, 3.90, 3.21, 4.10, 3.69, 3.27},
	{3.39, 3.68, 4.54, 6.62, 3.16, 4.54, 3.98, 3.73, 3.81, 2.72, 2.61, 4.06, 2.98, 2.63, 3.44, 3.85, 3.65, 2.41, 4.52, 3.17, 2.82},
	{3.86, 3.12, 3.46, 3.16, 8.85, 3.04, 3.37, 3.07, 3.45, 3.89, 3.70, 3.25, 3.95, 3.88, 2.69, 3.74, 3.74, 3.08, 3.61, 3.85, 4.17},
	{3.65, 3.80, 4.10, 4.54, 3.04, 6.70, 4.33, 3.34, 3.85, 2.92, 2.87, 4.36, 3.28, 2.89, 3.30, 3.71, 3.63, 2.51, 4.35, 3.33, 3.07},
	{3.58, 4.15, 4.10, 3.98, 3.37, 4.33, 6.02, 3.25, 4.18, 3.28, 3.37, 4.41, 3.91, 3.08, 3.26, 3.76, 3.74, 3.22, 4.34, 3.65, 3.30},
	{3.69, 3.13, 3.73, 3.73, 3.07, 3.34, 3.25, 6.85, 3.28, 2.77, 2.63, 3.48, 2.99, 2.80, 3.34, 3.81, 3.34, 2.70, 3.36, 2.84, 2.86},
	{3.50, 4.69, 4.51, 3.81, 3.45, 3.85, 4.18, 3.28, 6.67, 3.29, 3.36, 4.20, 3.55, 3.56, 3.43, 3.79, 3.70, 4.68, 4.04, 4.58, 3.35},
	{3.80, 3.06, 3.21, 2.72, 3.89, 2.92, 3.28, 2.77, 3.29, 6.48, 4.74, 3.09, 4.66, 4.38, 3.19, 3.34, 3.81, 3.58, 4.11, 3.78, 4.98},
	{3.55, 3.03, 3.09, 2.61, 3.70, 2.87, 3.37, 2.63, 3.36, 4.74, 6.12, 3.05, 4.88, 4.49, 2.97, 3.22, 3.61, 3.86, 3.38, 3.96, 4.38},
	{3.75, 4.72, 4.28, 4.06, 3.25, 4.36, 4.41, 3.48, 4.20, 3.09, 3.05, 6.45, 3.46, 3.04, 3.60, 3.86, 3.76, 3.07, 5.16, 3.57, 3.19},
	{3.89, 3.43, 3.55, 2.98, 3.95, 3.28, 3.91, 2.99, 3.55, 4.66, 4.88, 3.46, 6.57, 4.40, 3.14, 3.62, 3.96, 3.84, 3.83, 3.98, 4.35},
	{3.39, 2.95, 3.16, 2.63, 3.88, 2.89, 3.08, 2.80, 3.56, 4.38, 4.49, 3.04, 4.40, 7.24, 2.97, 3.22, 3.38, 5.23, 3.78, 4.96, 4.10},
	{3.49, 3.27, 3.50, 3.44, 2.69, 3.30, 3.26, 3.34, 3.43, 3.19, 2.97, 3.60, 3.14, 2.97, 7.31, 3.63, 3.37, 2.98, 4.08, 3.20, 3.15},
	{3.91, 3.65, 4.14, 3.85, 3.74, 3.71, 3.76, 3.81, 3.79, 3.34, 3.22, 3.86, 3.62, 3.22, 3.63, 5.49, 4.27, 3.23, 4.03, 3.46, 3.45},
	{3.91, 3.53, 3.90, 3.65, 3.74, 3.63, 3.74, 3.34, 3.70, 3.81, 3.61, 3.76, 3.96, 3.38, 3.37, 4.27, 6.31, 3.25, 5.07, 3.46, 3.96},
	{3.05, 3.00, 3.21, 2.41, 3.08, 2.51, 3.22, 2.70, 4.68, 3.58, 3.86, 3.07, 3.84, 5.23, 2.98, 3.23, 3.25, 8.90, 3.58, 4.85, 3.54},
	{4.11, 4.78, 4.10, 4.52, 3.61, 4.35, 4.34, 3.36, 4.04, 4.11, 3.38, 5.16, 3.83, 3.78, 4.08, 4.03, 5.07, 3.58, 10.0, 3.95, 3.61},
	{3.37, 3.61, 3.69, 3.17, 3.85, 3.33, 3.65, 2.84, 4.58, 3.78, 3.96, 3.57, 3.98, 4.96, 3.20, 3.46, 3.46, 4.85, 3.95, 7.26, 3.77},
	{3.92, 3.11, 3.27, 2.82, 4.17, 3.07, 3.30, 2.86, 3.35, 4.98, 4.38, 3.19, 4.35, 4.10, 3.15, 3.45, 3.96, 3.54, 3.61, 3.77, 6.16}};
	// A     R     N     D     C     E     Q     G     H     I     L     K     M      F    P     S     T     W     Y     X     V
	int aa_i_index, aa_j_index;
	int i;
	for(i=0; i<21;i++){
        if(aa_i == aa_custom_key[i]){
            aa_i_index = i;
            break;
        }
	}
    for(i=0; i<21;i++){
        if(aa_j == aa_custom_key[i]){
            aa_j_index = i;
            break;
        }
	}
	float score = custom_mat[aa_i_index][aa_j_index];
    return score;
}

float max(int size, float *elements){
    int i;
    float m = elements[0];
    for (i=0; i<size; i++){
        if (elements[i] > m) {
            m = elements[i];
        }
    }
    return m;
}

void printtrack(int lines, int columns, int track[lines][columns][2]){
    int i, j;
    for(i=0;i<lines;i++){
        for(j=0;j<columns;j++){
            printf("%2d,%2d   ", track[i][j][0], track[i][j][1]);
        }
        printf("\n");
    }
}

int main(int args, char* argv[]) {
    char *si = argv[1];
    char *sj = argv[2];
/*    char *si = "MMKPAASFPLLLLGLCHVSAISGIRKCDRNEFQCGDGKCIPYKWICDGSAECKDSSDESP"
"ETCREVTCGTDQFSCGGRLNRCIPMSWKCDGQTDCENGSDENDCTHKVCADDQFTCRSGK"
"CISLDFVCDEDLDCDDGSDESYCPAPTCNPAMFQCKDKGICIPKLWACDGDPDCEDGSDE"
"EHCEGREPIKTDKPCSPLEFHCGSGECIHMSWKCDGGFDCKDKSDEKDCVKPTCRPDQFQ"
"CNTGTCIHGSRQCDREYDCKDLSDEEGCVNVTKCEGPDVFKCRSGECITMDKVCNKKRDC"
"RDWSDEPLKECGENECLRNNGGCSHICNDLKIGYECLCNEGYRLVDQKRCEDINECENPN"
"TCSQICINLVGGYKCECREGYQMDPVTASCKSIGTVAYLFFTNRHEVRKMTLDRSEYTSV"
"IPRLKNVVALDMEIASNKIYWSDLTQRKIYSASMEKADNTSHHETVISNQIQAPDGIAVD"
"WIHGNIYWTDSKFSTISVANTEGSKRRTPPSDDLEKPRDIVVDPSQGFMYWTDWGLPAKI"
"EKGGLNGVDRYPLVTENIEWPNGITLDLINQRLYWVDSKLHSLSCIDVTGENRRTVISDE"
"THLAHPFGLTIFEDLVFWTDIENEAIFSANRLTGRNIMKVAEDLLSPEDIVLYHNLRQPK"
"AENWCEAHHLGNGGCEYLCLPAPHITARSPKFTCACPDGMHLGDDMRSCVKEPVIPEASP"
"TTTTSAPVTTTTSAPVTTTTSAPVTTTSTTARPTSRSTTLAKITSTTSTLAPQRPKMAST"
"TIAPQRPTTNSPKTTLRMITEKVPDHTTQQPMTHSQLADNNFAKAGVVENVRSHPTALYI"
"VLPIVILCLVAFGGFLVWKNWRLKNTNSINFDNPVYQKTTEEDQVHICRSQDGYTYPSRQ"
"MVSLEDDIA";

    char *sj = "MGPWGWKLRWTVALLLAAAGTAVGDRCERNEFQCQDGKCISYKWVCDGSAECQDGSDESQ"
"ETCLSVTCKSGDFSCGGRVNRCIPQFWRCDGQVDCDNGSDEQGCPPKTCSQDEFRCHDGK"
"CISRQFVCDSDRDCLDGSDEASCPVLTCGPASFQCNSSTCIPQLWACDNDPDCEDGSDEW"
"PQRCRGLYVFQGDSSPCSAFEFHCLSGECIHSSWRCDGGPDCKDKSDEENCAVATCRPDE"
"FQCSDGNCIHGSRQCDREYDCKDMSDEVGCVNVTLCEGPNKFKCHSGECITLDKVCNMAR"
"DCRDWSDEPIKECGTNECLDNNGGCSHVCNDLKIGYECLCPDGFQLVAQRRCEDIDECQD"
"PDTCSQLCVNLEGGYKCQCEEGFQLDPHTKACKAVGSIAYLFFTNRHEVRKMTLDRSEYT"
"SLIPNLRNVVALDTEVASNRIYWSDLSQRMICSTQLDRAHGVSSYDTVISRDIQAPDGLA"
"VDWIHSNIYWTDSVLGTVSVADTKGVKRKTLFRENGSKPRAIVVDPVHGFMYWTDWGTPA"
"KIKKGGLNGVDIYSLVTENIQWPNGITLDLLSGRLYWVDSKLHSISSIDVNGGNRKTILE"
"DEKRLAHPFSLAVFEDKVFWTDIINEAIFSANRLTGSDVNLLAENLLSPEDMVLFHNLTQ"
"PRGVNWCERTTLSNGGCQYLCLPAPQINPHSPKFTCACPDGMLLARDMRSCLTEAEAAVA"
"TQETSTVRLKVSSTAVRTQHTTTRPVPDTSRLPGATPGLTTVEIVTMSHQALGDVAGRGN"
"EKKPSSVRALSIVLPIVLLVFLCLGVFLLWKNWRLKNINSINFDNPVYQKTTEDEVHICH"
"NQDGYSYPSRQMVSLEDDVA";
*/
    const int si_len = strlen(si);
    const int sj_len = strlen(sj);
    const int lines = si_len + 1;
    const int columns = sj_len + 1;
    printf("INITIALIZING SUBMAT...");
    int i, j, k, l;
    float **matrix;
    matrix = malloc(sizeof(float*)*lines);
    for(i=0;i<lines;i++){
        matrix[i] = malloc(sizeof(float)*columns);
    }
    matrix[0][0] = 0;
    for (i = 1; i < lines; i++) {
        matrix[i][0] = penalty(i);
    }
    for (j = 1; j < columns; j++) {
        matrix[0][j] = penalty(j);
    }
    printf("DONE\n");
    printf("COMPUTING SUBMAT...\n");
    for (i = 1; i < lines; i++) {
        for (j = 1; j < columns; j++) {
            matrix[i][j] = submat(si[i-1], sj[j-1]);
        }
    }
    
    printf("InitMat:\n");
	printmat(si, sj, si_len, sj_len, matrix);
    
    printf("DONE\n");
    printf("INITIALIZING TRACK...");
    int ***track;
    track = (int***)malloc(sizeof(int**)*lines);
    for(i=0;i<lines;i++){
        track[i] = (int**)malloc(sizeof(int*)*columns);
        for(j=0; j<columns;j++){
            track[i][j] = (int*)malloc(sizeof(int)*2);
        }
    }
    track[0][0][0] = 0;
    track[0][0][1] = 0;
    for (i = 1; i < lines; i++) {
        track[i][0][0] = 0;
        track[i][0][1] = 0;
    }
    for (j = 1; j < columns; j++) {
        track[0][j][0] = 0;
        track[0][j][1] = 0;
    }
    printf("DONE\n");
    printf("STARTING MAIN ITERATION...");
    //int percentage;
    float score, score_i, score_j, score_ij;
    int index_i, index_j;
    for (i = 1; i < lines; i++) {
        for (j = 1; j < columns; j++) {
            score_ij = matrix[i-1][j-1] + matrix[i][j];

            score_i = matrix[i-1][j] + penalty(1);
            index_i = 1;
            for(k = 1; k <= i; k++){
                if (matrix[i-k][j] + penalty(k) > score_i){
                    score_i = matrix[i-k][j] + penalty(k);
                    index_i = k;
                }
            }
            score_j = matrix[i][j-1] + penalty(1);
            index_j = 1;
            for(l = 1; l <= j; l++){
                if (matrix[i][j-l] + penalty(l) > score_j){
                    score_j = matrix[i][j-l] + penalty(l);
                    index_j = l;
                }
            }

            float scores[3] = {score_ij, score_i, score_j};
            score = max(3, scores);
            matrix[i][j] = score;

            if(score == score_ij){
                track[i][j][0] = i-1;
                track[i][j][1] = j-1;
            }
            else if(score == score_i){
                track[i][j][0] = i-index_i;
                track[i][j][1] = j;
            }
            else if(score == score_j){
                track[i][j][0] = i;
                track[i][j][1] = j - index_j;
            }

        //percentage = 100*i/(lines-1);
        //printf("\r%3d%% ", percentage);
        //fflush(stdout);
        }
    }

    printf("DONE\n");
    printf("FREEING MATRIX...");
    for (i = 0; i < lines; i++){
        free(matrix[i]);
    }
    free(matrix);
    printf("DONE\n");

    printf("Track:\n");
	printtrack(lines, columns, track);

    printf("PATHFINDING...");
    int maxlen = si_len + sj_len;
    int path[maxlen][2];
    int p = lines - 1;
    int q = columns - 1;
    int P, Q;
    int step;
    int pathlen = 0;
    for(step=maxlen-1;step >= 0;step--){
        if(p == 0 || q == 0){
            if(p == q){
            path[step][0] = p;
            path[step][1] = q;
            pathlen++;
            break;
            }
            else{
            path[step][0] = p;
            path[step][1] = q;
            p = 0;
            q = 0;
            pathlen++;
            }
        }
        else{
            path[step][0] = p;
            path[step][1] = q;
            P = p;
            Q = q;
            p = track[P][Q][0];
            q = track[P][Q][1];

            pathlen++;
        }
    }
    printf("DONE\n");
    printf("FREEING TRACK...");
    for(i=0;i<lines;i++){
        for(j=0;j<columns;j++){
            free(track[i][j]);
        }
        free(track[i]);
    }
    free(track);
    printf("DONE\n");
    printf("BUILDING STRINGS...");
    char x[maxlen];
    char y[maxlen];
    int gap, cur_i, cur_j, next_i, next_j;
    int fromx = 0;
    int fromy = 0;
    int al_length = 0;
    for(step=maxlen-pathlen;step<maxlen;step++){
        cur_i = path[step][0];
        cur_j = path[step][1];
        next_i = path[step+1][0];
        next_j = path[step+1][1];
        if(cur_i == next_i){
            gap = next_j - cur_j;
            for(i=0;i<gap;i++){
                x[fromx] = '-';
                y[fromy] = sj[cur_j+i];
                fromx++;
                fromy++;
                al_length++;
            }
        }else if(cur_j == next_j){
            gap = next_i - cur_i;
            for(i=0;i<gap;i++){
                x[fromx] = si[cur_i+i];
                y[fromy] = '-';
                fromx++;
                fromy++;
                al_length++;
            }
        }else{
            x[fromx] = si[cur_i];
            y[fromy] = sj[cur_j];
            fromx++;
            fromy++;
            al_length++;
        }
    }
    printf("DONE\n");
    x[al_length] = '\0';
    y[al_length] = '\0';
    //printf("\n%s\n%s", x, y);

    char cwd[MAXPATHLEN];
    getcwd(cwd, MAXPATHLEN);
    char *filename = "/tmp.txt";
    char full_path[strlen(cwd)+strlen(filename)];
    strcpy(full_path, cwd);
    strcat(full_path, filename);
    //printf("%s", full_path);
    FILE *allineamelo;
    allineamelo = fopen(full_path,"w");
    fputs(x, allineamelo);
    fputs("\n", allineamelo);
    fputs(y, allineamelo);
    fclose(allineamelo);

    return 0;
}
