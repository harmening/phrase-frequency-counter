#define MINIMUM(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))

#include <stdio.h>
#include <string.h>




int _levenshtein1(char *str1, char *str2)
{

    unsigned int x, y, str1len, str2len;
    str1len = strlen(str1);
    str2len = strlen(str2);

    unsigned int distance[str2len+1][str1len+1];
    distance[0][0] = 0;

    for (x = 1; x <= str2len; x++)
        distance[x][0] = distance[x-1][0] + 1;

    for (y = 1; y <= str1len; y++)
        distance[0][y] = distance[0][y-1] + 1;

    for (x = 1; x <= str2len; x++)
        for (y = 1; y <= str1len; y++)
            distance[x][y] = MINIMUM(distance[x-1][y] + 1, distance[x][y-1] + 1,
																		 distance[x-1][y-1] + (str1[y-1] == str2[x-1] ? 0 : 1));

    return(distance[str2len][str1len]);

}




/* Only access the contents of the previous column when filling the distance-matrix
	 column-by-column. Faster for longer words!
*/

int _levenshtein2(char *str1, char *str2)
{

    unsigned int str1len, str2len, x, y, lastdiag, olddiag;
    str1len = strlen(str1);
    str2len = strlen(str2);

    unsigned int column[str1len+1];
    for (y = 1; y <= str1len; y++)
        column[y] = y;

    for (x = 1; x <= str2len; x++)
		{
        column[0] = x;
        for (y = 1, lastdiag = x-1; y <= str1len; y++)
				{
            olddiag = column[y];
            column[y] = MINIMUM(column[y] + 1, column[y-1] + 1,
																lastdiag + (str1[y-1] == str2[x-1] ? 0 : 1));
            lastdiag = olddiag;
        }
    }

    return(column[str1len]);

}



















































int _levenshtein(char *str1, char *str2)
{

    unsigned int x, y, str1len, str2len;
    str1len = strlen(str1);
    str2len = strlen(str2);

    unsigned int distance[str2len+1][str1len+1];
    distance[0][0] = 0;

    for (x = 1; x <= str2len; x++)
        distance[x][0] = distance[x-1][0] + 1;

    for (y = 1; y <= str1len; y++)
        distance[0][y] = distance[0][y-1] + 1;

    for (x = 1; x <= str2len; x++)
        for (y = 1; y <= str1len; y++)
            distance[x][y] = MINIMUM(distance[x-1][y] + 1, distance[x][y-1] + 1,
																		 distance[x-1][y-1] + (str1[y-1] == str2[x-1] ? 0 : 1));

    return(distance[str2len][str1len]);



}





int _levenshtein(char *str1, char *str2)
{

    unsigned int x, y, str1len, str2len;
    str1len = strlen(str1);
    str2len = strlen(str2);

    unsigned int distance[str2len+1][str1len+1];
    distance[0][0] = 0;

    for (x = 1; x <= str2len; x++)
        distance[x][0] = distance[x-1][0] + 1;

    for (y = 1; y <= str1len; y++)
        distance[0][y] = distance[0][y-1] + 1;

    for (x = 1; x <= str2len; x++)
        for (y = 1; y <= str1len; y++)
            distance[x][y] = MINIMUM(distance[x-1][y] + 1, distance[x][y-1] + 1,
																		 distance[x-1][y-1] + (str1[y-1] == str2[x-1] ? 0 : 1));

    return(distance[str2len][str1len]);



}
