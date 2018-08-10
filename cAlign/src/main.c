#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/param.h>

int penalty(int k){
    int g_op = -11;
    int g_ex = -2;
    return g_op + g_ex*(k-1);
}
 
void printmat(char *si, char*sj, int i_len, int j_len, int matrix[][j_len]){
    int i, j;
    printf("            ");
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
            printf("%5d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int submat(char aa_i, char aa_j){
    const char aa_key[20] = {'A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V'};
    int b62[20][20] = {
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

	int aa_i_index, aa_j_index;
	int i;
	for(i=0; i<20;i++){
        if(aa_i == aa_key[i]){
            aa_i_index = i;
            break;
        }
	}
    for(i=0; i<20;i++){
        if(aa_j == aa_key[i]){
            aa_j_index = i;
            break;
        }
	}
	int score = b62[aa_i_index][aa_j_index];
    return score;
}

int max(int size, int *elements){
    int i;
    int m = elements[0];
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
    int **matrix;
    matrix = (int**)malloc(sizeof(int*)*lines);
    for(i=0;i<lines;i++){
        matrix[i] = (int*)malloc(sizeof(int)*columns);
    }
    matrix[0][0] = 0;
    for (i = 1; i < lines; i++) {
        matrix[i][0] = penalty(i);
    }
    for (j = 1; j < columns; j++) {
        matrix[0][j] = penalty(j);
    }
    printf("DONE\n");
    printf("COMPUTING SUBMAT...");
    for (i = 1; i < lines; i++) {
        for (j = 1; j < columns; j++) {
            matrix[i][j] = submat(si[i-1], sj[j-1]);
        }
    }
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
    printf("STARTING MAIN ITERATION...\n");
    //int percentage;
    int score, score_i, score_j, score_ij, index_i, index_j;
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

            int scores[3] = {score_ij, score_i, score_j};
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
