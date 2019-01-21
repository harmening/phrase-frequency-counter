//using namespace std;
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






int _wagner_fischer_word(const char *str1, int str1len, const char *str2, int str2len)
{

        int a, b, c;
 
        // if one string is empty, difference is length of second string
        if (!str1len) return str2len;
        if (!str2len) return str1len;

 
        /* if last letters are the same, the difference is whatever is
         * required to edit the rest of the strings */

        if (str1[str1len - 1] == str2[str2len - 1])
                return _wagner_fischer_word(str1, str1len - 1, str2, str2len - 1);


 
        /* else determine minimum by: */

        // changing last letter of str1 to that of str2
        a = _wagner_fischer_word(str1, str1len - 1, str2, str2len - 1);

        // remove last letter of str1
        b = _wagner_fischer_word(str1, str1len,     str2, str2len - 1);

        // remove last letter of str2
        c = _wagner_fischer_word(str1, str1len - 1, str2, str2len    );


				// and check for minimum 
        if (a > b) a = b;
        if (a > c) a = c;

 
        return a + 1;
}



